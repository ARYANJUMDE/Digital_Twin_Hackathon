"""
Tests for Digital Twin engine methods.
"""
import pytest
import pandas as pd
from datetime import datetime
from src.data.generate_synthetic import generate_ehr_profiles, generate_wearable_timeseries
from src.twin.digital_twin import DigitalTwin

def test_digital_twin_lifecycle():
    ehr_df = generate_ehr_profiles(n_patients=1, seed=42)
    wearable_df = generate_wearable_timeseries(ehr_df, days=2, interval_minutes=15, seed=42)
    
    patient_id = ehr_df.iloc[0]["patient_id"]
    ehr_profile = ehr_df.iloc[0].to_dict()
    
    twin = DigitalTwin(
        patient_id=patient_id,
        ehr_profile=ehr_profile,
        state_history=wearable_df
    )
    
    state = twin.get_current_state()
    assert state["patient_id"] == patient_id
    assert 0.0 <= twin.current_risk <= 1.0
    assert twin.risk_level in ["LOW", "MODERATE", "HIGH"]
    
    # Test sensor update
    new_reading = {
        "timestamp": datetime.now(),
        "glucose": 175.0,
        "heart_rate": 88.0,
        "hrv": 35.0,
        "steps": 250,
        "sleep_hours": 6.5,
        "activity_level": "Light",
        "meal_carbs": 60.0,
        "meal_type": "Snack"
    }
    pred_res = twin.update_sensor_data(new_reading)
    assert "glucose_spike_risk" in pred_res
    
    # Test SHAP explanation
    explanation = twin.explain_prediction()
    assert "contributions" in explanation
    assert len(explanation["contributions"]) > 0
    
    # Test what-if simulation
    sim_res = twin.simulate({"meal_carbs": 100.0, "steps": 0})
    assert "simulated_risk" in sim_res
    assert "risk_delta_percentage_points" in sim_res
    assert "disclaimer" in sim_res

def test_digital_twin_short_history():
    ehr_df = generate_ehr_profiles(n_patients=1, seed=42)
    wearable_df = generate_wearable_timeseries(ehr_df, days=1, interval_minutes=15, seed=42)
    
    patient_id = ehr_df.iloc[0]["patient_id"]
    ehr_profile = ehr_df.iloc[0].to_dict()
    
    # Test with short history window (only 2 rows)
    short_history = wearable_df.iloc[:2].copy()
    twin = DigitalTwin(
        patient_id=patient_id,
        ehr_profile=ehr_profile,
        state_history=short_history
    )
    assert 0.0 <= twin.current_risk <= 1.0
    pred_res = twin.predict()
    assert "glucose_spike_risk" in pred_res
    
    # Simulate on short history
    sim_res = twin.simulate({"glucose": 180.0, "meal_carbs": 50.0})
    assert "simulated_risk" in sim_res
