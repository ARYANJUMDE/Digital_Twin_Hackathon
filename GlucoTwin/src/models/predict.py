"""
Inference & Prediction Helper Module for GlucoTwin.
"""

import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Union

from src.utils.logger import get_logger
from src.utils.config_loader import load_config
from src.features.build_features import get_feature_column_names

logger = get_logger("ModelPredict")

class GlucoseSpikePredictor:
    """
    Wrapper class to load saved model and preprocessor and perform predictions.
    """
    def __init__(self, config_path: str = None):
        config = load_config(config_path)
        self.best_model_path = Path(config["paths"]["best_model_file"])
        self.preprocessor_path = Path(config["paths"]["preprocessor_file"])
        
        if not self.best_model_path.exists() or not self.preprocessor_path.exists():
            raise FileNotFoundError(
                f"Model or preprocessor artifact missing at {self.best_model_path}. Run training first!"
            )
            
        self.model = joblib.load(self.best_model_path)
        prep_data = joblib.load(self.preprocessor_path)
        
        self.scaler = prep_data["scaler"]
        self.feature_cols = prep_data["feature_cols"]
        self.best_model_name = prep_data["best_model_name"]
        
    def predict_proba(self, X: Union[pd.DataFrame, Dict[str, Any], np.ndarray]) -> float:
        """
        Returns probability of glucose spike (0.0 to 1.0) for a single sample or array.
        """
        if isinstance(X, dict):
            X_df = pd.DataFrame([X])
        elif isinstance(X, np.ndarray):
            if X.ndim == 1:
                X_df = pd.DataFrame([X], columns=self.feature_cols)
            else:
                X_df = pd.DataFrame(X, columns=self.feature_cols)
        else:
            X_df = X.copy()
            
        # Ensure all required features are present
        for col in self.feature_cols:
            if col not in X_df.columns:
                X_df[col] = 0.0
                
        X_df = X_df[self.feature_cols]
        
        if self.best_model_name == "Logistic Regression":
            X_prep = self.scaler.transform(X_df)
            prob = self.model.predict_proba(X_prep)[:, 1]
        else:
            prob = self.model.predict_proba(X_df)[:, 1]
            
        if len(prob) == 1:
            return float(prob[0])
        return prob
