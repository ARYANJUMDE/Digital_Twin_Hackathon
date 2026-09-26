"""
Patient EHR View Component for Streamlit Dashboard.
"""
import streamlit as st
from typing import Dict, Any

def render_patient_profile(ehr_profile: Dict[str, Any]):
    """
    Renders patient demographic and static clinical data in a clinician-grade card layout.
    """
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
        <h3 style="margin: 0; font-size: 1.3rem; font-weight: 700; color: #f8fafc;">
            👤 Patient Clinical Profile (EHR)
        </h3>
        <span style="background: rgba(56, 189, 248, 0.12); border: 1px solid #38bdf8; color: #38bdf8; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
            ID: {}
        </span>
    </div>
    """.format(ehr_profile.get("patient_id", "N/A")), unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        age = ehr_profile.get("age", "N/A")
        sex = ehr_profile.get("sex", "N/A")
        st.metric("Age / Sex", f"{age} yrs / {sex}")
        
    with col2:
        bmi = float(ehr_profile.get("bmi", 0.0))
        bmi_status = "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"
        st.metric("BMI", f"{bmi:.1f} kg/m²", delta=bmi_status, delta_color="inverse" if bmi >= 25 else "normal")
        
    with col3:
        hba1c = float(ehr_profile.get("hba1c", 0.0))
        hba_status = "Controlled" if hba1c < 6.5 else "Elevated" if hba1c < 8.0 else "High Risk"
        st.metric("HbA1c Level", f"{hba1c:.1f}%", delta=hba_status, delta_color="inverse" if hba1c >= 6.5 else "normal")
        
    with col4:
        status = ehr_profile.get("diabetes_status", "N/A")
        med = ehr_profile.get("medication", "None")
        st.metric("Diabetes Status", status)

    # Secondary details strip
    dur = float(ehr_profile.get("diabetes_duration_years", 0.0))
    htn = "Diagnosed" if ehr_profile.get("hypertension") == 1 else "None"
    chol = ehr_profile.get("cholesterol", "Normal")
    fam_score = float(ehr_profile.get("family_risk_score", 0.0))
    
    st.markdown(f"""
    <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.06); padding: 12px 18px; border-radius: 10px; margin-top: 10px; font-size: 0.88rem; color: #cbd5e1; display: flex; flex-wrap: wrap; gap: 24px;">
        <div>💊 <strong>Medication:</strong> <span style="color: #38bdf8;">{med}</span></div>
        <div>⏳ <strong>Duration:</strong> <span style="color: #f8fafc;">{dur:.1f} years</span></div>
        <div>🫀 <strong>Hypertension:</strong> <span style="color: {'#f43f5e' if htn == 'Diagnosed' else '#34d399'};">{htn}</span></div>
        <div>🩸 <strong>Cholesterol:</strong> <span style="color: {'#fbbf24' if chol == 'High' else '#34d399'};">{chol}</span></div>
        <div>🧬 <strong>Genetic Risk Score:</strong> <span style="color: #a78bfa;">{fam_score:.2f} / 1.0</span></div>
    </div>
    """, unsafe_allow_html=True)
