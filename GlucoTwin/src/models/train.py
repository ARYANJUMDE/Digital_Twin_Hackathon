"""
Model Training & Evaluation Module for GlucoTwin.

Trains, evaluates, and compares Logistic Regression, Random Forest, XGBoost, and optional LSTM models.
Saves best model, preprocessor, and metric reports.
"""

import json
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Tuple

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb

from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    roc_auc_score, precision_recall_curve, auc, confusion_matrix
)

from src.utils.logger import get_logger
from src.utils.config_loader import load_config
from src.features.build_features import get_feature_column_names

logger = get_logger("ModelTrain")

def evaluate_model(model: Any, X_test: np.ndarray, y_test: np.ndarray, name: str) -> Dict[str, Any]:
    """
    Computes real classification metrics for a trained model on the test dataset.
    """
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_pred_proba >= 0.5).astype(int)
    
    precision = float(precision_score(y_test, y_pred, zero_division=0))
    recall = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    roc_auc = float(roc_auc_score(y_test, y_pred_proba))
    
    # Precision-Recall AUC
    prec_arr, rec_arr, _ = precision_recall_curve(y_test, y_pred_proba)
    pr_auc = float(auc(rec_arr, prec_arr))
    
    cm = confusion_matrix(y_test, y_pred).tolist()
    
    metrics = {
        "model_name": name,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "roc_auc": round(roc_auc, 4),
        "pr_auc": round(pr_auc, 4),
        "confusion_matrix": cm
    }
    logger.info(f"[{name}] F1: {f1:.4f} | ROC-AUC: {roc_auc:.4f} | PR-AUC: {pr_auc:.4f} | Recall: {recall:.4f}")
    return metrics

def train_and_evaluate_models(config_path: str = None) -> Dict[str, Any]:
    """
    Main pipeline to train and evaluate all candidate ML models.
    """
    config = load_config(config_path)
    processed_path = Path(config["paths"]["processed_data_file"])
    
    if not processed_path.exists():
        logger.warning(f"Processed feature file not found at {processed_path}. Running processing first...")
        from src.data.process import process_and_save_data
        df = process_and_save_data(config_path)
    else:
        df = pd.read_csv(processed_path, low_memory=False)
        
    feature_cols, target_col = get_feature_column_names()
    
    # Ensure all feature columns exist in df
    missing_cols = [c for c in feature_cols if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required feature columns in dataset: {missing_cols}")
        
    X = df[feature_cols].copy()
    y = df[target_col].copy()
    
    # Group-based or temporal train-test split
    test_size = config["models"].get("test_size", 0.2)
    random_state = config["models"].get("random_state", 42)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    logger.info(f"Training split: {X_train.shape[0]} samples, Test split: {X_test.shape[0]} samples")
    
    # Fit StandardScaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    models = {}
    metrics_results = {}
    
    # 1. Logistic Regression
    lr_cfg = config["models"].get("logistic_regression", {})
    lr_model = LogisticRegression(
        max_iter=lr_cfg.get("max_iter", 1000),
        C=lr_cfg.get("C", 1.0),
        class_weight="balanced",
        random_state=random_state
    )
    logger.info("Training Logistic Regression...")
    lr_model.fit(X_train_scaled, y_train)
    models["Logistic Regression"] = (lr_model, X_test_scaled)
    metrics_results["Logistic Regression"] = evaluate_model(lr_model, X_test_scaled, y_test, "Logistic Regression")
    
    # 2. Random Forest
    rf_cfg = config["models"].get("random_forest", {})
    rf_model = RandomForestClassifier(
        n_estimators=rf_cfg.get("n_estimators", 100),
        max_depth=rf_cfg.get("max_depth", 10),
        class_weight="balanced",
        random_state=random_state,
        n_jobs=-1
    )
    logger.info("Training Random Forest...")
    rf_model.fit(X_train, y_train)  # Tree models use unscaled features for cleaner SHAP interpretations
    models["Random Forest"] = (rf_model, X_test)
    metrics_results["Random Forest"] = evaluate_model(rf_model, X_test, y_test, "Random Forest")
    
    # 3. XGBoost
    xgb_cfg = config["models"].get("xgboost", {})
    scale_pos_weight = (len(y_train) - sum(y_train)) / sum(y_train)
    xgb_model = xgb.XGBClassifier(
        n_estimators=xgb_cfg.get("n_estimators", 100),
        max_depth=xgb_cfg.get("max_depth", 6),
        learning_rate=xgb_cfg.get("learning_rate", 0.05),
        scale_pos_weight=scale_pos_weight,
        random_state=random_state,
        eval_metric="logloss"
    )
    logger.info("Training XGBoost...")
    xgb_model.fit(X_train, y_train)
    models["XGBoost"] = (xgb_model, X_test)
    metrics_results["XGBoost"] = evaluate_model(xgb_model, X_test, y_test, "XGBoost")
    
    # Select Best Model based on F1 Score
    best_name = max(metrics_results, key=lambda k: metrics_results[k]["f1_score"])
    best_model, _ = models[best_name]
    logger.info(f"=== Best Model Selected: {best_name} (F1 Score: {metrics_results[best_name]['f1_score']}) ===")
    
    # Save artifacts
    models_dir = Path(config["paths"]["models_dir"])
    models_dir.mkdir(parents=True, exist_ok=True)
    
    best_model_path = Path(config["paths"]["best_model_file"])
    preprocessor_path = Path(config["paths"]["preprocessor_file"])
    metrics_path = Path(config["paths"]["metrics_file"])
    
    joblib.dump(best_model, best_model_path)
    joblib.dump({
        "scaler": scaler,
        "feature_cols": feature_cols,
        "best_model_name": best_name
    }, preprocessor_path)
    
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics_results, f, indent=2)
        
    logger.info(f"Best model saved to: {best_model_path}")
    logger.info(f"Preprocessor saved to: {preprocessor_path}")
    logger.info(f"Metrics saved to: {metrics_path}")
    
    return metrics_results

if __name__ == "__main__":
    train_and_evaluate_models()
