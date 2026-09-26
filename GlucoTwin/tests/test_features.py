"""
Tests for feature engineering module.
"""
import pytest
import pandas as pd
from src.data.generate_synthetic import generate_ehr_profiles, generate_wearable_timeseries
from src.features.build_features import build_features_dataset, get_feature_column_names

def test_build_features_dataset():
    ehr_df = generate_ehr_profiles(n_patients=2, seed=42)
    wearable_df = generate_wearable_timeseries(ehr_df, days=2, interval_minutes=15, seed=42)
    
    featured_df = build_features_dataset(ehr_df, wearable_df, horizon_steps=8, spike_threshold=40.0)
    assert isinstance(featured_df, pd.DataFrame)
    assert "target_spike" in featured_df.columns
    
    feature_cols, target_col = get_feature_column_names()
    assert target_col == "target_spike"
    assert len(feature_cols) > 20
