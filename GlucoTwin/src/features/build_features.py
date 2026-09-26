"""
Feature Engineering Module for GlucoTwin.

Combines static EHR data and dynamic wearable sensor time-series to construct
predictive features without data leakage.
"""

import numpy as np
import pandas as pd
from typing import Tuple, List, Dict, Any

from src.utils.logger import get_logger
from src.utils.config_loader import load_config

logger = get_logger("FeatureEngineering")

def compute_timeseries_features_for_patient(
    df_patient: pd.DataFrame,
    horizon_steps: int = 8,
    spike_threshold: float = 40.0,
    is_training: bool = True
) -> pd.DataFrame:
    """
    Computes time-series lag, trend, rolling statistics, and future spike target
    for a single patient's wearable data sorted chronologically.
    
    If is_training is True, trims the final horizon_steps rows where target cannot be computed.
    If is_training is False, preserves the latest rows for real-time Digital Twin feature inference.
    """
    df = df_patient.sort_values("timestamp").copy()
    
    # 1. Target creation (Future horizon check)
    future_max_glucose = (
        df["glucose"]
        .iloc[::-1]  # reverse
        .rolling(window=horizon_steps, min_periods=1)
        .max()
        .iloc[::-1]  # restore order
        .shift(-1)  # exclude current timestamp
    )
    
    # Target: 1 if future max glucose - current glucose >= threshold, else 0
    df["target_max_future_glucose"] = future_max_glucose.fillna(df["glucose"])
    df["glucose_diff_future"] = (df["target_max_future_glucose"] - df["glucose"]).fillna(0.0)
    df["target_spike"] = (df["glucose_diff_future"] >= spike_threshold).astype(int)
    
    # 2. Glucose Trend & Rolling Statistics (Historical ONLY)
    g = df["glucose"]
    df["glucose_trend_15m"] = g.diff(1).fillna(0.0)
    df["glucose_trend_30m"] = (g - g.shift(2)).fillna(0.0) / 2.0
    df["glucose_trend_60m"] = (g - g.shift(4)).fillna(0.0) / 4.0
    
    df["glucose_mean_1h"] = g.rolling(window=4, min_periods=1).mean().fillna(g)
    df["glucose_mean_2h"] = g.rolling(window=8, min_periods=1).mean().fillna(g)
    df["glucose_mean_4h"] = g.rolling(window=16, min_periods=1).mean().fillna(g)
    
    df["glucose_std_2h"] = g.rolling(window=8, min_periods=1).std().fillna(0.0)
    df["glucose_std_4h"] = g.rolling(window=16, min_periods=1).std().fillna(0.0)
    df["glucose_min_2h"] = g.rolling(window=8, min_periods=1).min().fillna(g)
    df["glucose_max_2h"] = g.rolling(window=8, min_periods=1).max().fillna(g)
    
    # 3. Heart Rate & HRV Features
    hr = df["heart_rate"]
    df["heart_rate_mean_1h"] = hr.rolling(window=4, min_periods=1).mean().fillna(hr)
    df["heart_rate_trend_30m"] = (hr - hr.shift(2)).fillna(0.0)
    
    hrv = df["hrv"]
    df["hrv_mean_1h"] = hrv.rolling(window=4, min_periods=1).mean().fillna(hrv)
    df["hrv_change_1h"] = (hrv - hrv.shift(4)).fillna(0.0)
    
    # 4. Activity & Sleep Features
    steps = df["steps"]
    df["recent_steps_1h"] = steps.rolling(window=4, min_periods=1).sum().fillna(0.0)
    df["recent_steps_2h"] = steps.rolling(window=8, min_periods=1).sum().fillna(0.0)
    df["sleep_deficit"] = (8.0 - df["sleep_hours"]).clip(lower=0.0).fillna(0.0)
    
    # 5. Carbohydrate & Meal Features
    carbs = df["meal_carbs"]
    df["meal_carbs_last_30m"] = carbs.rolling(window=2, min_periods=1).sum().fillna(0.0)
    df["meal_carbs_last_1h"] = carbs.rolling(window=4, min_periods=1).sum().fillna(0.0)
    df["meal_carbs_last_2h"] = carbs.rolling(window=8, min_periods=1).sum().fillna(0.0)
    
    # Time since last meal calculation (in minutes)
    time_since_meal = []
    last_meal_ts = None
    for ts, carb in zip(df["timestamp"], df["meal_carbs"]):
        if carb > 0:
            last_meal_ts = ts
        if last_meal_ts is None:
            time_since_meal.append(240.0)  # Default 4 hours if no prior meal
        else:
            diff_mins = (ts - last_meal_ts).total_seconds() / 60.0
            time_since_meal.append(min(240.0, diff_mins))
    df["time_since_last_meal"] = time_since_meal
    
    # Drop rows at the end ONLY during dataset training processing
    if is_training and len(df) > horizon_steps:
        df = df.iloc[:-horizon_steps].copy()
        
    return df

def build_features_dataset(
    ehr_df: pd.DataFrame,
    wearable_df: pd.DataFrame,
    horizon_steps: int = 8,
    spike_threshold: float = 40.0
) -> pd.DataFrame:
    """
    Merges static EHR data with dynamic wearable time-series features.
    """
    wearable_df["timestamp"] = pd.to_datetime(wearable_df["timestamp"])
    
    patient_feature_dfs = []
    for pid, p_group in wearable_df.groupby("patient_id"):
        p_featured = compute_timeseries_features_for_patient(
            p_group, horizon_steps=horizon_steps, spike_threshold=spike_threshold, is_training=True
        )
        patient_feature_dfs.append(p_featured)
        
    all_wearable_featured = pd.concat(patient_feature_dfs, ignore_index=True)
    
    # Merge EHR profile
    full_df = pd.merge(all_wearable_featured, ehr_df, on="patient_id", how="left")
    
    # Clean up non-feature helper target columns
    target_col = full_df["target_spike"]
    
    logger.info(f"Feature dataset built. Total samples: {len(full_df)}, Spike class balance: {target_col.mean():.2%}")
    return full_df

def get_feature_column_names() -> Tuple[List[str], str]:
    """
    Returns the list of feature column names used for ML modeling and the target column name.
    """
    feature_cols = [
        # Current vitals
        "glucose", "heart_rate", "hrv", "steps", "sleep_hours", "meal_carbs",
        # Trends & Rolling vitals
        "glucose_trend_15m", "glucose_trend_30m", "glucose_trend_60m",
        "glucose_mean_1h", "glucose_mean_2h", "glucose_mean_4h",
        "glucose_std_2h", "glucose_std_4h", "glucose_min_2h", "glucose_max_2h",
        "heart_rate_mean_1h", "heart_rate_trend_30m",
        "hrv_mean_1h", "hrv_change_1h",
        # Activity & Sleep
        "recent_steps_1h", "recent_steps_2h", "sleep_deficit",
        # Carbs & Meals
        "meal_carbs_last_30m", "meal_carbs_last_1h", "meal_carbs_last_2h", "time_since_last_meal",
        # Static EHR
        "age", "bmi", "hba1c", "hypertension", "diabetes_duration_years", "family_risk_score",
        # Encoded categoricals
        "sex_M", "diabetes_status_Pre-Diabetes", "diabetes_status_Type 1", "diabetes_status_Type 2",
        "cholesterol_High", "medication_Metformin", "medication_Metformin+DPP4",
        "medication_Insulin", "medication_Insulin+Metformin"
    ]
    target_col = "target_spike"
    return feature_cols, target_col
