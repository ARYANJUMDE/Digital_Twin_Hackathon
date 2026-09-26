"""
What-If Scenario Simulation View Component for Streamlit Dashboard.
"""
import streamlit as st
from typing import Dict, Any
from src.twin.digital_twin import DigitalTwin

def render_whatif_simulation(twin: DigitalTwin):
    """
    Renders interactive sliders for physiological parameters, executes twin simulation,
    and displays side-by-side risk comparison.
    """
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(14, 165, 233, 0.1) 0%, rgba(99, 102, 241, 0.1) 100%); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 12px; padding: 18px 24px; margin-bottom: 20px;">
        <h3 style="margin: 0 0 6px 0; font-size: 1.35rem; font-weight: 800; color: #38bdf8;">
            🧪 Digital Twin What-If Scenario Simulator
        </h3>
        <p style="margin: 0; color: #cbd5e1; font-size: 0.9rem;">
            Test hypothetical interventions (e.g. reducing carbohydrate intake, taking a 15-minute post-meal walk, improving sleep) and observe the prospective risk recalculation in real-time.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    current_vitals = twin.current_state
    
    curr_g = float(current_vitals.get("glucose", 120.0))
    curr_carbs = float(current_vitals.get("meal_carbs", 0.0))
    curr_sleep = float(current_vitals.get("sleep_hours", 7.0))
    curr_steps = int(current_vitals.get("steps", 100))
    curr_hr = float(current_vitals.get("heart_rate", 72.0))
    curr_hrv = float(current_vitals.get("hrv", 45.0))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🩸 Glycemic & Diet Controls**")
        sim_glucose = st.slider("Simulated Glucose (mg/dL)", 60.0, 300.0, curr_g, step=5.0)
        sim_carbs = st.slider("Meal Carbs Intake (g)", 0.0, 150.0, curr_carbs, step=5.0)
        
    with col2:
        st.markdown("**🏃 Activity & Sleep Controls**")
        sim_steps = st.slider("Physical Steps (15m window)", 0, 3500, curr_steps, step=100)
        sim_sleep = st.slider("Sleep Last Night (hrs)", 3.0, 10.0, curr_sleep, step=0.5)
        
    with col3:
        st.markdown("**🫀 Autonomic Vitals**")
        sim_hr = st.slider("Heart Rate (bpm)", 50.0, 150.0, curr_hr, step=2.0)
        sim_hrv = st.slider("HRV RMSSD (ms)", 10.0, 100.0, curr_hrv, step=2.0)
        
    st.markdown("<br>", unsafe_allow_html=True)
    sim_button = st.button("⚡ RE-EVALUATE DIGITAL TWIN RISK", use_container_width=True, type="primary")
    
    if sim_button or "sim_result" in st.session_state:
        modifications = {
            "glucose": sim_glucose,
            "meal_carbs": sim_carbs,
            "sleep_hours": sim_sleep,
            "steps": sim_steps,
            "heart_rate": sim_hr,
            "hrv": sim_hrv
        }
        
        sim_res = twin.simulate(modifications)
        st.session_state["sim_result"] = sim_res
        
        curr_risk = sim_res["current_risk"]
        sim_risk = sim_res["simulated_risk"]
        delta = sim_res["risk_delta_percentage_points"]
        
        st.markdown("---")
        st.markdown("#### 📊 Simulation Risk Outcomes")
        
        r1, r2, r3 = st.columns(3)
        with r1:
            st.metric("Baseline Risk", f"{curr_risk:.1f}%", delta=sim_res["current_risk_level"])
        with r2:
            st.metric("Simulated Twin Risk", f"{sim_risk:.1f}%", delta=sim_res["simulated_risk_level"])
        with r3:
            delta_str = f"{delta:+.1f} percentage points"
            st.metric("Risk Delta", f"{delta:+.1f}%", delta=delta_str, delta_color="inverse" if delta > 0 else "normal")
            
        st.markdown(f"""
        <div style="background: rgba(245, 158, 11, 0.1); border-left: 4px solid #f59e0b; border-radius: 8px; padding: 12px 16px; margin-top: 14px; font-size: 0.85rem; color: #fbbf24;">
            ⚠️ <strong>Medical Disclaimer:</strong> {sim_res['disclaimer']}
        </div>
        """, unsafe_allow_html=True)
