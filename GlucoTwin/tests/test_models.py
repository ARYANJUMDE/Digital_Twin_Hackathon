"""
Tests for ML predictor and model loading.
"""
import pytest
from src.models.predict import GlucoseSpikePredictor

def test_glucose_spike_predictor():
    predictor = GlucoseSpikePredictor()
    assert predictor.model is not None
    assert predictor.best_model_name in ["XGBoost", "Random Forest", "Logistic Regression"]
    
    # Test dummy sample prediction
    dummy_sample = {col: 0.5 for col in predictor.feature_cols}
    dummy_sample["glucose"] = 120.0
    dummy_sample["hba1c"] = 6.5
    dummy_sample["bmi"] = 26.0
    
    prob = predictor.predict_proba(dummy_sample)
    assert isinstance(prob, float)
    assert 0.0 <= prob <= 1.0
