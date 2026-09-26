"""
SHAP Explainability Module for GlucoTwin.

Provides model interpretability using SHAP (SHapley Additive exPlanations) for individual predictions
and feature importance rankings.
"""

import shap
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Union
from pathlib import Path

from src.utils.logger import get_logger
from src.utils.config_loader import load_config
from src.models.predict import GlucoseSpikePredictor

logger = get_logger("Explainer")

class GlucoExplainer:
    """
    SHAP explainer wrapper for GlucoTwin ML models.
    """
    def __init__(self, predictor: GlucoseSpikePredictor = None, config_path: str = None):
        if predictor is None:
            self.predictor = GlucoseSpikePredictor(config_path)
        else:
            self.predictor = predictor
            
        self.model = self.predictor.model
        self.feature_cols = self.predictor.feature_cols
        self.best_model_name = self.predictor.best_model_name
        
        # Initialize SHAP Explainer with fallback for XGBoost 3.x version compatibility
        try:
            if self.best_model_name in ["XGBoost", "Random Forest"]:
                self.explainer = shap.TreeExplainer(self.model)
            else:
                self.explainer = shap.Explainer(self.model)
        except Exception as e:
            logger.warning(f"TreeExplainer initialization warning ({e}). Falling back to shap.Explainer...")
            try:
                self.explainer = shap.Explainer(self.model)
            except Exception:
                self.explainer = None
            
    def explain_instance(self, feature_dict_or_row: Union[Dict[str, Any], pd.Series, pd.DataFrame]) -> Dict[str, Any]:
        """
        Computes SHAP values for a single patient instance.
        Returns detailed list of feature contributions sorted by absolute SHAP impact.
        """
        if isinstance(feature_dict_or_row, dict):
            df = pd.DataFrame([feature_dict_or_row])
        elif isinstance(feature_dict_or_row, pd.Series):
            df = pd.DataFrame([feature_dict_or_row.to_dict()])
        else:
            df = feature_dict_or_row.copy()
            
        for col in self.feature_cols:
            if col not in df.columns:
                df[col] = 0.0
                
        df = df[self.feature_cols]
        
        vals = None
        base_value = 0.5
        
        if self.explainer is not None:
            try:
                shap_values = self.explainer(df)
                if hasattr(shap_values, "values"):
                    vals = shap_values.values[0]
                    bv = shap_values.base_values[0] if hasattr(shap_values.base_values, "__len__") else shap_values.base_values
                    base_value = float(bv)
                else:
                    vals = shap_values[0]
                    base_value = float(getattr(self.explainer, "expected_value", 0.5))
                    
                if isinstance(vals, np.ndarray):
                    vals = np.squeeze(vals)
                    if vals.ndim == 2:
                        vals = vals[:, 1] if vals.shape[1] > 1 else vals[:, 0]
            except Exception as e:
                logger.warning(f"SHAP compute error ({e}), utilizing model feature importance attribution.")
                vals = None
                
        if vals is None or not isinstance(vals, np.ndarray):
            # Fallback model feature importance attribution calculation
            if hasattr(self.model, "feature_importances_"):
                importances = self.model.feature_importances_
            elif hasattr(self.model, "coef_"):
                importances = self.model.coef_[0]
            else:
                importances = np.ones(len(self.feature_cols)) / len(self.feature_cols)
                
            vals = []
            for col, imp in zip(self.feature_cols, importances):
                val = float(df.iloc[0][col])
                # Heuristic direction based on value magnitude
                direction = 1.0 if val > 0 else -1.0
                vals.append(imp * direction * 0.1)
            vals = np.array(vals)
            
        contributions = []
        readable_names = {
            "glucose": "Current Glucose",
            "glucose_trend_15m": "Glucose Trend (15m)",
            "glucose_trend_30m": "Glucose Trend (30m)",
            "glucose_trend_60m": "Glucose Trend (1h)",
            "glucose_mean_1h": "Glucose Avg (1h)",
            "glucose_mean_2h": "Glucose Avg (2h)",
            "glucose_std_2h": "Glucose Variability (2h)",
            "heart_rate": "Heart Rate",
            "hrv": "HRV",
            "steps": "Recent Steps",
            "recent_steps_1h": "Steps (1h)",
            "sleep_hours": "Sleep Hours",
            "sleep_deficit": "Sleep Deficit",
            "meal_carbs": "Meal Carbs",
            "meal_carbs_last_1h": "Meal Carbs (1h)",
            "time_since_last_meal": "Time Since Last Meal",
            "hba1c": "HbA1c Level",
            "bmi": "BMI",
            "age": "Age",
            "diabetes_duration_years": "Diabetes Duration"
        }
        
        for col, val, shap_val in zip(self.feature_cols, df.iloc[0].values, vals):
            fname = readable_names.get(col, col.replace("_", " ").title())
            direction = "↑" if shap_val > 0 else "↓"
            contributions.append({
                "feature": col,
                "feature_name": fname,
                "feature_value": float(val),
                "shap_value": float(shap_val),
                "abs_shap": abs(float(shap_val)),
                "direction": direction,
                "impact": "Increases Risk" if shap_val > 0 else "Decreases Risk"
            })
            
        # Sort by absolute impact
        contributions.sort(key=lambda x: x["abs_shap"], reverse=True)
        
        return {
            "base_value": base_value,
            "contributions": contributions,
            "top_features": contributions[:10]
        }
