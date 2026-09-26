"""
FastAPI REST API Backend for GlucoTwin React Frontend.
"""

import sys
from pathlib import Path

# Add project root directory to python path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import math
import numpy as np
import json
import pandas as pd
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.utils.config_loader import load_config
from src.data.generate_synthetic import generate_and_save_data
from src.data.process import process_and_save_data
from src.models.train import train_and_evaluate_models
from src.models.predict import GlucoseSpikePredictor
from src.explainability.explainer import GlucoExplainer
from src.twin.digital_twin import DigitalTwin

app = FastAPI(
    title="GlucoTwin REST API",
    description="FastAPI Backend for GlucoTwin Healthcare Digital Twin",
    version="1.0.0"
)

# Enable CORS for React Frontend (vite default port 5173 / localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def clean_for_json(data):
    """Recursively cleans objects, replacing NaN/inf with None and converting numpy types."""
    if isinstance(data, dict):
        return {k: clean_for_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_for_json(v) for v in data]
    elif isinstance(data, (np.floating, float)):
        if np.isnan(data) or math.isnan(data) or np.isinf(data) or math.isinf(data):
            return None
        return float(data)
    elif isinstance(data, (np.integer, int)):
        return int(data)
    elif isinstance(data, np.ndarray):
        return clean_for_json(data.tolist())
    elif isinstance(data, (np.bool_, bool)):
        return bool(data)
    elif pd.isna(data):
        return None
    return data

# Global caches for dataset and models
EHR_DF = None
WEARABLE_DF = None
METRICS_DATA = None
PREDICTOR = None
EXPLAINER = None

@app.on_event("startup")
def startup_event():
    global EHR_DF, WEARABLE_DF, METRICS_DATA, PREDICTOR, EXPLAINER
    config = load_config()
    ehr_path = Path(config["paths"]["ehr_file"])
    wearable_path = Path(config["paths"]["wearable_file"])
    metrics_path = Path(config["paths"]["metrics_file"])
    
    if not ehr_path.exists() or not wearable_path.exists():
        generate_and_save_data()
        process_and_save_data()
        
    if not metrics_path.exists():
        train_and_evaluate_models()
        
    EHR_DF = pd.read_csv(ehr_path)
    WEARABLE_DF = pd.read_csv(wearable_path)
    WEARABLE_DF["timestamp"] = pd.to_datetime(WEARABLE_DF["timestamp"])
    
    if metrics_path.exists():
        with open(metrics_path, "r", encoding="utf-8") as f:
            METRICS_DATA = json.load(f)
            
    PREDICTOR = GlucoseSpikePredictor()
    EXPLAINER = GlucoExplainer(PREDICTOR)

class SimulationRequest(BaseModel):
    patient_id: str
    stream_index: Optional[int] = None
    modifications: Dict[str, Any]

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "GlucoTwin API", "version": "1.0.0"}

@app.get("/api/patients")
def get_patients():
    if EHR_DF is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    patients = []
    for _, row in EHR_DF.iterrows():
        p_wearables = WEARABLE_DF[WEARABLE_DF["patient_id"] == row["patient_id"]]
        med = None if pd.isna(row.get("medication")) else str(row["medication"])
        patients.append({
            "patient_id": str(row["patient_id"]),
            "age": int(row["age"]),
            "sex": str(row["sex"]),
            "bmi": float(row["bmi"]),
            "hba1c": float(row["hba1c"]),
            "diabetes_status": str(row["diabetes_status"]),
            "medication": med,
            "total_sensor_readings": len(p_wearables)
        })
    return clean_for_json(patients)

@app.get("/api/patients/{patient_id}/ehr")
def get_patient_ehr(patient_id: str):
    p_df = EHR_DF[EHR_DF["patient_id"] == patient_id]
    if p_df.empty:
        raise HTTPException(status_code=404, detail="Patient not found")
    ehr_dict = p_df.iloc[0].to_dict()
    return clean_for_json(ehr_dict)

@app.get("/api/patients/{patient_id}/wearables")
def get_patient_wearables(patient_id: str, stream_index: Optional[int] = Query(None)):
    p_df = WEARABLE_DF[WEARABLE_DF["patient_id"] == patient_id].sort_values("timestamp")
    if p_df.empty:
        raise HTTPException(status_code=404, detail="Wearable data not found")
        
    if stream_index is not None and stream_index > 0:
        p_df = p_df.iloc[:stream_index]
        
    records = []
    for _, row in p_df.iterrows():
        meal_t = None if pd.isna(row.get("meal_type")) else str(row["meal_type"])
        act_l = None if pd.isna(row.get("activity_level")) else str(row["activity_level"])
        records.append({
            "timestamp": str(row["timestamp"]),
            "glucose": float(row["glucose"]),
            "heart_rate": float(row["heart_rate"]),
            "hrv": float(row["hrv"]),
            "steps": int(row["steps"]),
            "sleep_hours": float(row["sleep_hours"]),
            "activity_level": act_l,
            "meal_carbs": float(row["meal_carbs"]),
            "meal_type": meal_t
        })
    return clean_for_json(records)

@app.get("/api/patients/{patient_id}/twin")
def get_patient_twin(patient_id: str, stream_index: Optional[int] = Query(None)):
    p_ehr_df = EHR_DF[EHR_DF["patient_id"] == patient_id]
    if p_ehr_df.empty:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    p_ehr = p_ehr_df.iloc[0].to_dict()
    
    p_wearables = WEARABLE_DF[WEARABLE_DF["patient_id"] == patient_id].sort_values("timestamp")
    if p_wearables.empty:
        raise HTTPException(status_code=404, detail="Patient wearable data not found")
        
    if stream_index is not None and stream_index > 0:
        p_wearables = p_wearables.iloc[:stream_index]
        
    twin = DigitalTwin(
        patient_id=patient_id,
        ehr_profile=p_ehr,
        state_history=p_wearables,
        predictor=PREDICTOR,
        explainer=EXPLAINER
    )
    
    current_state = twin.get_current_state()
    prediction = twin.predict()
    explanation = twin.explain_prediction()
    
    return clean_for_json({
        "current_state": current_state,
        "prediction": prediction,
        "explanation": explanation
    })

@app.post("/api/twin/simulate")
def simulate_twin_scenario(req: SimulationRequest):
    p_ehr_df = EHR_DF[EHR_DF["patient_id"] == req.patient_id]
    if p_ehr_df.empty:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    p_ehr = p_ehr_df.iloc[0].to_dict()
    
    p_wearables = WEARABLE_DF[WEARABLE_DF["patient_id"] == req.patient_id].sort_values("timestamp")
    if req.stream_index is not None and req.stream_index > 0:
        p_wearables = p_wearables.iloc[:req.stream_index]
        
    twin = DigitalTwin(
        patient_id=req.patient_id,
        ehr_profile=p_ehr,
        state_history=p_wearables,
        predictor=PREDICTOR,
        explainer=EXPLAINER
    )
    
    sim_res = twin.simulate(req.modifications)
    return clean_for_json(sim_res)

@app.get("/api/models/metrics")
def get_model_metrics():
    if METRICS_DATA is None:
        raise HTTPException(status_code=404, detail="Metrics not available")
    return clean_for_json(METRICS_DATA)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
