"""
GlucoTwin — High-Performance Clinician Dashboard & Digital Twin Platform.

Interactive AI healthcare application for early prediction of glucose spikes.
"""

import sys
from pathlib import Path

# Add project root directory to python path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import json
import time
import pandas as pd
import numpy as np
import streamlit as st

from src.utils.config_loader import load_config
from src.data.generate_synthetic import generate_and_save_data
from src.data.process import process_and_save_data
from src.models.train import train_and_evaluate_models
from src.models.predict import GlucoseSpikePredictor
from src.explainability.explainer import GlucoExplainer
from src.twin.digital_twin import DigitalTwin

# Dashboard Components
from dashboard.components.patient_view import render_patient_profile
from dashboard.components.twin_view import render_twin_state
from dashboard.components.charts import render_timeseries_charts
from dashboard.components.prediction_view import render_prediction_view
from dashboard.components.explainer_view import render_shap_explanation
from dashboard.components.simulation_view import render_whatif_simulation
from dashboard.components.timeline import render_patient_timeline

# Set Page Config
st.set_page_config(
    page_title="GlucoTwin — AI Healthcare Digital Twin",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Ultra-Modern CSS Theme (Glassmorphism + Neon Accents + Custom Fonts)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #0d1527 50%, #08101d 100%);
        color: #f1f5f9;
    }

    /* Top Hero Header */
    .hero-container {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.5) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px 30px;
        backdrop-filter: blur(12px);
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-top: 6px;
        font-weight: 400;
    }

    /* Glass Cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .glass-card:hover {
        border-color: rgba(56, 189, 248, 0.3);
        box-shadow: 0 10px 35px -5px rgba(56, 189, 248, 0.15);
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 14px 18px;
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 700 !important;
        font-size: 1.6rem !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.8);
        padding: 8px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        border-radius: 10px;
        color: #94a3b8;
        font-weight: 600;
        font-size: 0.92rem;
        padding: 0 18px;
        border: none;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4);
    }

    /* Sidebar Styling */
    div[data-testid="stSidebar"] {
        background-color: #070c18 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    /* Disclaimer Banner */
    .disclaimer-banner {
        background: linear-gradient(90deg, rgba(239, 68, 68, 0.12) 0%, rgba(245, 158, 11, 0.12) 100%);
        border-left: 4px solid #ef4444;
        border-radius: 8px;
        padding: 10px 16px;
        color: #fca5a5;
        font-size: 0.85rem;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 10px 20px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #3b82f6 100%);
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.5);
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_datasets():
    """Loads EHR, Wearable time series, and Model metrics."""
    config = load_config()
    ehr_path = Path(config["paths"]["ehr_file"])
    wearable_path = Path(config["paths"]["wearable_file"])
    metrics_path = Path(config["paths"]["metrics_file"])
    
    if not ehr_path.exists() or not wearable_path.exists():
        generate_and_save_data()
        process_and_save_data()
        
    if not metrics_path.exists():
        train_and_evaluate_models()
        
    ehr_df = pd.read_csv(ehr_path)
    wearable_df = pd.read_csv(wearable_path)
    wearable_df["timestamp"] = pd.to_datetime(wearable_df["timestamp"])
    
    metrics = {}
    if metrics_path.exists():
        with open(metrics_path, "r", encoding="utf-8") as f:
            metrics = json.load(f)
            
    return ehr_df, wearable_df, metrics

def main():
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 class="hero-title">🧬 GlucoTwin</h1>
                <p class="hero-subtitle">Next-Generation AI Healthcare Digital Twin for Early Glucose Spike Prediction (2-Hour Horizon)</p>
            </div>
            <div style="text-align: right;">
                <span style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; color: #34d399; padding: 6px 14px; border-radius: 20px; font-size: 0.82rem; font-weight: 600;">
                    🟢 LIVE TWIN ENGINE ACTIVE
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Load Data
    try:
        ehr_df, wearable_df, metrics_data = load_datasets()
    except Exception as e:
        st.error(f"Initialization error: {e}")
        st.info("Generating synthetic data and training machine learning models...")
        generate_and_save_data()
        process_and_save_data()
        train_and_evaluate_models()
        ehr_df, wearable_df, metrics_data = load_datasets()
        
    # Sidebar Controls
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 10px 0;">
        <h2 style="font-size: 1.4rem; font-weight: 700; color: #38bdf8; margin: 0;">🎛️ Digital Twin Control</h2>
        <p style="font-size: 0.8rem; color: #64748b; margin-top: 4px;">Patient & Streaming Manager</p>
    </div>
    """, unsafe_allow_html=True)
    
    patient_list = ehr_df["patient_id"].unique().tolist()
    selected_patient_id = st.sidebar.selectbox("📋 Select Patient Profile", patient_list, index=0)
    
    patient_ehr = ehr_df[ehr_df["patient_id"] == selected_patient_id].iloc[0].to_dict()
    patient_wearables = wearable_df[wearable_df["patient_id"] == selected_patient_id].sort_values("timestamp").copy()
    
    # Streaming Index State
    sim_key = f"sim_index_{selected_patient_id}"
    if sim_key not in st.session_state:
        st.session_state[sim_key] = min(48, len(patient_wearables) - 1)
        
    curr_max_idx = st.session_state[sim_key]
    sliced_history = patient_wearables.iloc[:curr_max_idx + 1].copy()
    
    # Live Wearable Streaming Panel
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚡ Live Wearable Stream (15m Ticks)")
    
    col_s1, col_s2 = st.sidebar.columns(2)
    with col_s1:
        if st.button("⏩ +15m Tick", use_container_width=True):
            if curr_max_idx < len(patient_wearables) - 1:
                st.session_state[sim_key] += 1
                st.rerun()
            else:
                st.toast("Reached end of patient sensor history!", icon="ℹ️")
                
    with col_s2:
        if st.button("🔄 Reset Window", use_container_width=True):
            st.session_state[sim_key] = 24
            st.rerun()
            
    progress_pct = (curr_max_idx + 1) / len(patient_wearables)
    st.sidebar.progress(progress_pct)
    st.sidebar.caption(f"Stream Window: **{curr_max_idx + 1}** / {len(patient_wearables)} readings (15-min intervals)")
    
    # Sidebar Model Metrics
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🏆 Active ML Models")
    if metrics_data:
        for m_name, m_val in metrics_data.items():
            f1 = m_val.get("f1_score", 0.0)
            auc_val = m_val.get("roc_auc", 0.0)
            badge_color = "#38bdf8" if m_name == "XGBoost" else "#94a3b8"
            st.sidebar.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.6); padding: 8px 12px; border-radius: 8px; margin-bottom: 6px; border: 1px solid rgba(255,255,255,0.05);">
                <div style="font-weight: 600; font-size: 0.85rem; color: {badge_color};">{m_name}</div>
                <div style="font-size: 0.78rem; color: #cbd5e1;">F1: <strong>{f1:.3f}</strong> | ROC-AUC: <strong>{auc_val:.3f}</strong></div>
            </div>
            """, unsafe_allow_html=True)
            
    # Load Predictor and Explainer
    predictor = GlucoseSpikePredictor()
    explainer = GlucoExplainer(predictor)
    
    # Instantiate Digital Twin
    twin = DigitalTwin(
        patient_id=selected_patient_id,
        ehr_profile=patient_ehr,
        state_history=sliced_history,
        predictor=predictor,
        explainer=explainer
    )
    
    # Main Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Twin Dashboard",
        "📈 Time Series Signals",
        "🎯 Spike Prediction & SHAP",
        "🧪 What-If Simulator",
        "⏱️ Patient Timeline",
        "🤖 Model Benchmarks"
    ])
    
    with tab1:
        render_patient_profile(twin.ehr_profile)
        st.markdown("<br>", unsafe_allow_html=True)
        render_twin_state(twin.get_current_state())
        st.markdown("<br>", unsafe_allow_html=True)
        pred = twin.predict()
        render_prediction_view(pred)
        
    with tab2:
        render_timeseries_charts(sliced_history)
        
    with tab3:
        p_res = twin.predict()
        render_prediction_view(p_res)
        st.markdown("<br>", unsafe_allow_html=True)
        exp_res = twin.explain_prediction()
        render_shap_explanation(exp_res)
        
    with tab4:
        render_whatif_simulation(twin)
        
    with tab5:
        render_patient_timeline(sliced_history)
        
    with tab6:
        st.markdown("### 🤖 Machine Learning Model Benchmarks")
        st.caption("Comparative evaluation of candidate classifiers trained on historical wearable and EHR features.")
        
        if metrics_data:
            m_rows = []
            for name, m in metrics_data.items():
                m_rows.append({
                    "Model Name": name,
                    "Precision": f"{m['precision']:.4f}",
                    "Recall": f"{m['recall']:.4f}",
                    "F1 Score": f"{m['f1_score']:.4f}",
                    "ROC-AUC": f"{m['roc_auc']:.4f}",
                    "PR-AUC": f"{m['pr_auc']:.4f}"
                })
            m_df = pd.DataFrame(m_rows)
            st.dataframe(m_df, use_container_width=True, hide_index=True)
            
            st.markdown("#### Confusion Matrices")
            c_cols = st.columns(len(metrics_data))
            for idx, (name, m) in enumerate(metrics_data.items()):
                with c_cols[idx]:
                    st.markdown(f"**{name}**")
                    cm = np.array(m["confusion_matrix"])
                    cm_df = pd.DataFrame(cm, index=["Actual No Spike", "Actual Spike"], columns=["Pred No Spike", "Pred Spike"])
                    st.dataframe(cm_df, use_container_width=True)

if __name__ == "__main__":
    main()
