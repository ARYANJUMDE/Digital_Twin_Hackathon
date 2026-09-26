"""
Digital Twin Core Engine for GlucoTwin.

Maintains patient profile, real-time sensor history, physiological state, feature calculation,
spike risk prediction, SHAP explanation, and scenario simulation.
"""

import copy
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Optional

from src.utils.logger import get_logger
from src.features.build_features import compute_timeseries_features_for_patient, get_feature_column_names
from src.models.predict import GlucoseSpikePredictor
from src.explainability.explainer import GlucoExplainer

logger = get_logger("DigitalTwin")

class DigitalTwin:
    """
    Patient Digital Twin Class.
    Integrates static EHR data with dynamic wearable time-series inputs.
    """
    def __init__(
        self,
        patient_id: str,
        ehr_profile: Dict[str, Any],
        state_history: pd.DataFrame,
        predictor: Optional[GlucoseSpikePredictor] = None,
        explainer: Optional[GlucoExplainer] = None
    ):
        self.patient_id = patient_id
        self.ehr_profile = copy.deepcopy(ehr_profile)
        
        # Sort and copy initial state history dataframe
        if isinstance(state_history, pd.DataFrame) and not state_history.empty:
            self.state_history = state_history.sort_values("timestamp").copy()
        else:
            raise ValueError("State history DataFrame must not be empty.")
            
        self.predictor = predictor if predictor is not None else GlucoseSpikePredictor()
        self.explainer = explainer if explainer is not None else GlucoExplainer(self.predictor)
        
        self.current_state: Dict[str, Any] = {}
        self.derived_features: Dict[str, Any] = {}
        self.current_risk: float = 0.0
        self.risk_level: str = "LOW"
        self.last_prediction_time: Optional[datetime] = None
        
        # Perform initial state sync, feature calculation, and risk prediction
        self.update_state()
        self.calculate_features()
        self.predict()
        
    def update_sensor_data(self, new_reading: Dict[str, Any]) -> Dict[str, Any]:
        """
        Receives a new 15-minute wearable sensor reading, appends it to state history,
        updates state, recalculates features, and triggers a new prediction.
        """
        reading_dict = copy.deepcopy(new_reading)
        reading_dict["patient_id"] = self.patient_id
        if "timestamp" in reading_dict:
            reading_dict["timestamp"] = pd.to_datetime(reading_dict["timestamp"])
        else:
            reading_dict["timestamp"] = pd.to_datetime(datetime.now())
            
        new_row = pd.DataFrame([reading_dict])
        self.state_history = pd.concat([self.state_history, new_row], ignore_index=True)
        
        # Update state, calculate features, and predict
        self.update_state()
        self.calculate_features()
        pred_res = self.predict()
        
        logger.info(
            f"[Twin {self.patient_id}] Updated sensor reading at {reading_dict['timestamp']}. "
            f"New Risk: {self.current_risk:.1%} ({self.risk_level})"
        )
        return pred_res
        
    def update_state(self) -> None:
        """
        Updates the current physiological state from the latest row of state_history and EHR profile.
        """
        latest_row = self.state_history.iloc[-1].to_dict()
        self.current_state = {
            **self.ehr_profile,
            **latest_row
        }
        
    def calculate_features(self) -> Dict[str, Any]:
        """
        Computes dynamic rolling statistics and derived features for the Digital Twin state.
        """
        # Run patient-level feature engineering on state_history without trimming horizon
        featured_history = compute_timeseries_features_for_patient(
            self.state_history, horizon_steps=8, spike_threshold=40.0, is_training=False
        )
        
        # If dataset was too short to trim horizon steps, compute without horizon trimming
        if featured_history.empty:
            featured_history = self.state_history.copy()
            featured_history["glucose_trend_15m"] = 0.0
            featured_history["glucose_mean_1h"] = featured_history["glucose"]
            featured_history["glucose_mean_2h"] = featured_history["glucose"]
            featured_history["glucose_std_2h"] = 0.0
            featured_history["heart_rate_mean_1h"] = featured_history["heart_rate"]
            featured_history["hrv_mean_1h"] = featured_history["hrv"]
            featured_history["recent_steps_1h"] = featured_history["steps"]
            featured_history["sleep_deficit"] = max(0.0, 8.0 - featured_history["sleep_hours"].iloc[-1])
            featured_history["meal_carbs_last_1h"] = featured_history["meal_carbs"]
            featured_history["time_since_last_meal"] = 120.0
            
        latest_feat_row = featured_history.iloc[-1].to_dict()
        
        # Add categorical encodings matching model expectations
        latest_feat_row["sex_M"] = 1 if self.ehr_profile.get("sex") == "M" else 0
        latest_feat_row["diabetes_status_Pre-Diabetes"] = 1 if self.ehr_profile.get("diabetes_status") == "Pre-Diabetes" else 0
        latest_feat_row["diabetes_status_Type 1"] = 1 if self.ehr_profile.get("diabetes_status") == "Type 1" else 0
        latest_feat_row["diabetes_status_Type 2"] = 1 if self.ehr_profile.get("diabetes_status") == "Type 2" else 0
        latest_feat_row["cholesterol_High"] = 1 if self.ehr_profile.get("cholesterol") == "High" else 0
        
        med = self.ehr_profile.get("medication", "None")
        latest_feat_row["medication_Metformin"] = 1 if med == "Metformin" else 0
        latest_feat_row["medication_Metformin+DPP4"] = 1 if med == "Metformin+DPP4" else 0
        latest_feat_row["medication_Insulin"] = 1 if med == "Insulin" else 0
        latest_feat_row["medication_Insulin+Metformin"] = 1 if med == "Insulin+Metformin" else 0
        
        # Merge static EHR numerical features
        for key in ["age", "bmi", "hba1c", "hypertension", "diabetes_duration_years", "family_risk_score"]:
            latest_feat_row[key] = float(self.ehr_profile.get(key, 0.0))
            
        self.derived_features = latest_feat_row
        return self.derived_features

    def predict(self) -> Dict[str, Any]:
        """
        Runs model prediction using derived features and updates twin risk state.
        """
        feature_cols, _ = get_feature_column_names()
        input_dict = {col: self.derived_features.get(col, 0.0) for col in feature_cols}
        
        risk_prob = self.predictor.predict_proba(input_dict)
        self.current_risk = float(risk_prob)
        self.last_prediction_time = pd.to_datetime(self.current_state.get("timestamp", datetime.now()))
        
        if self.current_risk < 0.30:
            self.risk_level = "LOW"
        elif self.current_risk < 0.65:
            self.risk_level = "MODERATE"
        else:
            self.risk_level = "HIGH"
            
        return {
            "patient_id": self.patient_id,
            "prediction_timestamp": self.last_prediction_time,
            "glucose_spike_risk": self.current_risk,
            "risk_percentage": round(self.current_risk * 100, 1),
            "risk_level": self.risk_level,
            "prediction_horizon": "2 hours",
            "threshold_mgdl": 40.0
        }
        
    def explain_prediction(self) -> Dict[str, Any]:
        """
        Generates SHAP feature contribution explanation for current prediction.
        """
        feature_cols, _ = get_feature_column_names()
        input_dict = {col: self.derived_features.get(col, 0.0) for col in feature_cols}
        return self.explainer.explain_instance(input_dict)

    def simulate(self, modifications: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a simulated Digital Twin state with user modifications (e.g., carbs, steps, sleep, glucose),
        recalculates features and runs prediction to evaluate what-if impact.
        """
        # Create a deep copy of the twin state history
        sim_history = self.state_history.copy()
        latest_idx = sim_history.index[-1]
        
        # Apply parameter modifications to the latest row
        for key, val in modifications.items():
            if key in sim_history.columns:
                sim_history.loc[latest_idx, key] = val
                
        # Create simulated twin instance
        sim_twin = DigitalTwin(
            patient_id=f"{self.patient_id}_SIM",
            ehr_profile=self.ehr_profile,
            state_history=sim_history,
            predictor=self.predictor,
            explainer=self.explainer
        )
        
        sim_risk = sim_twin.current_risk
        risk_delta = sim_risk - self.current_risk
        percentage_point_change = round(risk_delta * 100, 1)
        
        return {
            "current_risk": round(self.current_risk * 100, 1),
            "current_risk_level": self.risk_level,
            "simulated_risk": round(sim_risk * 100, 1),
            "simulated_risk_level": sim_twin.risk_level,
            "risk_delta_percentage_points": percentage_point_change,
            "modifications": modifications,
            "disclaimer": "This is a model-based scenario simulation, not medical advice."
        }
        
    def get_current_state(self) -> Dict[str, Any]:
        """
        Returns full state representation of the Digital Twin.
        """
        return {
            "patient_id": self.patient_id,
            "profile": self.ehr_profile,
            "current_vitals": {
                "glucose": self.current_state.get("glucose"),
                "heart_rate": self.current_state.get("heart_rate"),
                "hrv": self.current_state.get("hrv"),
                "steps": self.current_state.get("steps"),
                "sleep_hours": self.current_state.get("sleep_hours"),
                "activity_level": self.current_state.get("activity_level"),
                "meal_carbs": self.current_state.get("meal_carbs"),
                "meal_type": self.current_state.get("meal_type"),
                "timestamp": str(self.current_state.get("timestamp"))
            },
            "risk_status": {
                "risk_probability": round(self.current_risk, 4),
                "risk_percentage": round(self.current_risk * 100, 1),
                "risk_level": self.risk_level,
                "last_prediction_time": str(self.last_prediction_time)
            }
        }
