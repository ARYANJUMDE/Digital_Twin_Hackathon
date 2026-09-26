"""
Data Processing Pipeline Module for GlucoTwin.

Reads synthetic raw datasets, constructs temporal and static features, encodes categoricals,
and saves the final preprocessed feature table.
"""

import pandas as pd
from pathlib import Path
from src.utils.logger import get_logger
from src.utils.config_loader import load_config
from src.features.build_features import build_features_dataset, get_feature_column_names

logger = get_logger("DataProcess")

def process_and_save_data(config_path: str = None) -> pd.DataFrame:
    """
    Loads raw synthetic EHR and wearable data, computes features, handles encoding, and saves output.
    """
    config = load_config(config_path)
    ehr_path = Path(config["paths"]["ehr_file"])
    wearable_path = Path(config["paths"]["wearable_file"])
    out_path = Path(config["paths"]["processed_data_file"])
    
    if not ehr_path.exists() or not wearable_path.exists():
        logger.warning("Raw synthetic files not found. Generating synthetic data first...")
        from src.data.generate_synthetic import generate_and_save_data
        generate_and_save_data(config_path)
        
    logger.info(f"Loading EHR from {ehr_path} and Wearable data from {wearable_path}...")
    ehr_df = pd.read_csv(ehr_path)
    wearable_df = pd.read_csv(wearable_path)
    
    pred_cfg = config["prediction"]
    horizon_steps = pred_cfg.get("prediction_horizon_steps", 8)
    spike_threshold = pred_cfg.get("spike_threshold_mgdl", 40.0)
    
    logger.info(f"Building feature dataset (Horizon steps: {horizon_steps}, Threshold: {spike_threshold} mg/dL)...")
    df = build_features_dataset(
        ehr_df=ehr_df,
        wearable_df=wearable_df,
        horizon_steps=horizon_steps,
        spike_threshold=spike_threshold
    )
    
    # Categorical one-hot encoding
    # Sex: sex_M
    df["sex_M"] = (df["sex"] == "M").astype(int)
    
    # Diabetes status: Pre-Diabetes, Type 1, Type 2 (No Diabetes as reference)
    df["diabetes_status_Pre-Diabetes"] = (df["diabetes_status"] == "Pre-Diabetes").astype(int)
    df["diabetes_status_Type 1"] = (df["diabetes_status"] == "Type 1").astype(int)
    df["diabetes_status_Type 2"] = (df["diabetes_status"] == "Type 2").astype(int)
    
    # Cholesterol: High
    df["cholesterol_High"] = (df["cholesterol"] == "High").astype(int)
    
    # Medication: Metformin, Metformin+DPP4, Insulin, Insulin+Metformin (None as reference)
    df["medication_Metformin"] = (df["medication"] == "Metformin").astype(int)
    df["medication_Metformin+DPP4"] = (df["medication"] == "Metformin+DPP4").astype(int)
    df["medication_Insulin"] = (df["medication"] == "Insulin").astype(int)
    df["medication_Insulin+Metformin"] = (df["medication"] == "Insulin+Metformin").astype(int)
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Saving preprocessed dataset to {out_path} (Shape: {df.shape})...")
    df.to_csv(out_path, index=False)
    
    return df

if __name__ == "__main__":
    process_and_save_data()
