"""
Tests for synthetic data generation module.
"""
import pytest
import pandas as pd
from src.data.generate_synthetic import generate_ehr_profiles, generate_wearable_timeseries

def test_generate_ehr_profiles():
    n_patients = 10
    df = generate_ehr_profiles(n_patients=n_patients, seed=42)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == n_patients
    expected_cols = [
        "patient_id", "age", "sex", "bmi", "hba1c", "diabetes_status",
        "hypertension", "cholesterol", "medication", "diabetes_duration_years", "family_risk_score"
    ]
    for col in expected_cols:
        assert col in df.columns

def test_generate_wearable_timeseries():
    ehr_df = generate_ehr_profiles(n_patients=2, seed=42)
    wearable_df = generate_wearable_timeseries(ehr_df, days=1, interval_minutes=15, seed=42)
    assert isinstance(wearable_df, pd.DataFrame)
    # 1 day = 96 readings per patient -> 2 * 96 = 192
    assert len(wearable_df) == 192
    expected_cols = [
        "patient_id", "timestamp", "glucose", "heart_rate", "hrv", "steps",
        "sleep_hours", "activity_level", "meal_carbs", "meal_type"
    ]
    for col in expected_cols:
        assert col in wearable_df.columns
