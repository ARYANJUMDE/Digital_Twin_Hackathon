"""
Patient Timeline View Component for Streamlit Dashboard.
"""
import streamlit as st
import pandas as pd

def render_patient_timeline(df_history: pd.DataFrame):
    """
    Renders chronological event timeline including meals, activity, and high risk readings.
    """
    st.markdown("""
    <h3 style="margin: 0 0 4px 0; font-size: 1.3rem; font-weight: 700; color: #f8fafc;">
        ⏱️ Patient Chronological Event Log
    </h3>
    <p style="color: #94a3b8; font-size: 0.88rem; margin-bottom: 16px;">
        Audit trail of dietary ingestion, physical activity bursts, and hyperglycemia alerts.
    </p>
    """, unsafe_allow_html=True)
    
    if df_history.empty:
        st.info("No event history available.")
        return
        
    df = df_history.sort_values("timestamp", ascending=False).copy()
    
    events = []
    for _, row in df.iterrows():
        ts_str = str(row["timestamp"])
        g = float(row["glucose"])
        carbs = float(row["meal_carbs"])
        mtype = row["meal_type"]
        steps = int(row["steps"])
        
        if carbs > 0:
            events.append({
                "Timestamp": ts_str,
                "Event Type": "🍽️ Meal Ingestion",
                "Details": f"{carbs:.0f}g carbs ({mtype})",
                "Glucose Level": f"{g:.1f} mg/dL",
                "Clinical Impact": "🟡 Moderate (Digestion)"
            })
        if g >= 160:
            events.append({
                "Timestamp": ts_str,
                "Event Type": "⚠️ Hyperglycemia Alert",
                "Details": f"Glucose elevated to {g:.1f} mg/dL",
                "Glucose Level": f"{g:.1f} mg/dL",
                "Clinical Impact": "🔴 High (Hyperglycemia)"
            })
        if steps >= 1000:
            events.append({
                "Timestamp": ts_str,
                "Event Type": "🏃 Physical Activity",
                "Details": f"{steps} steps recorded",
                "Glucose Level": f"{g:.1f} mg/dL",
                "Clinical Impact": "🟢 Positive (Clearance)"
            })
            
    if not events:
        st.write("No major physiological events recorded in recent history.")
        return
        
    events_df = pd.DataFrame(events[:20])
    
    st.dataframe(
        events_df,
        use_container_width=True,
        hide_index=True
    )
