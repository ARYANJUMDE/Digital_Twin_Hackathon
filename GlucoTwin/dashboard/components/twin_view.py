"""
Digital Twin Current State View Component for Streamlit Dashboard.
"""
import streamlit as st
from typing import Dict, Any

def render_twin_state(twin_state: Dict[str, Any]):
    """
    Renders physiological vitals maintained by the Digital Twin instance.
    """
    vitals = twin_state.get("current_vitals", {})
    ts = vitals.get("timestamp", "N/A")
    
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
        <h3 style="margin: 0; font-size: 1.3rem; font-weight: 700; color: #f8fafc;">
            🧬 Digital Twin State Monitor
        </h3>
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="height: 8px; width: 8px; background-color: #10b981; border-radius: 50%; display: inline-block; box-shadow: 0 0 10px #10b981;"></span>
            <span style="color: #94a3b8; font-size: 0.82rem; font-weight: 500;">Last Sensor Sync: <code style="color: #38bdf8;">{}</code></span>
        </div>
    </div>
    """.format(ts), unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    g_val = float(vitals.get("glucose", 0.0))
    g_status = "Normal" if g_val < 140 else "Elevated" if g_val < 180 else "Hyperglycemic"
    g_color = "normal" if g_val < 140 else "inverse"
    with col1:
        st.metric("Continuous Glucose", f"{g_val:.1f} mg/dL", delta=g_status, delta_color=g_color)
        
    hr_val = float(vitals.get("heart_rate", 0.0))
    hr_status = "Resting" if hr_val < 75 else "Active" if hr_val < 110 else "Elevated"
    with col2:
        st.metric("Heart Rate", f"{hr_val:.0f} bpm", delta=hr_status)
        
    hrv_val = float(vitals.get("hrv", 0.0))
    hrv_status = "Optimal" if hrv_val >= 45 else "Moderate Stress" if hrv_val >= 25 else "High Fatigue"
    with col3:
        st.metric("HRV (RMSSD)", f"{hrv_val:.1f} ms", delta=hrv_status, delta_color="normal" if hrv_val >= 35 else "inverse")
        
    steps_val = int(vitals.get("steps", 0))
    act_level = vitals.get("activity_level", "Sedentary")
    with col4:
        st.metric("Steps (15m)", f"{steps_val}", delta=act_level)
        
    sleep_val = float(vitals.get("sleep_hours", 0.0))
    sleep_status = "Sufficient" if sleep_val >= 7.0 else "Sleep Deficit"
    with col5:
        st.metric("Sleep Last Night", f"{sleep_val:.1f} hrs", delta=sleep_status, delta_color="normal" if sleep_val >= 7.0 else "inverse")
        
    # Recent Meal Banner
    carbs = float(vitals.get("meal_carbs", 0.0))
    meal_type = vitals.get("meal_type", "None")
    
    if carbs > 0:
        st.markdown(f"""
        <div style="background: rgba(245, 158, 11, 0.12); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 10px; padding: 10px 16px; margin-top: 10px; color: #fbbf24; font-size: 0.88rem; display: flex; align-items: center; justify-content: space-between;">
            <div>🍽️ <strong>Recent Meal Ingestion Detected:</strong> {carbs:.0f}g Carbohydrates ({meal_type})</div>
            <div style="font-size: 0.8rem; color: #f59e0b; background: rgba(0,0,0,0.3); padding: 3px 10px; border-radius: 6px;">Digestive Phase Active</div>
        </div>
        """, unsafe_allow_html=True)
