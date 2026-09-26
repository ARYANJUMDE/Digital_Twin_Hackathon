"""
Prediction & Risk Level View Component for Streamlit Dashboard.
"""
import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any

def render_prediction_view(pred_dict: Dict[str, Any]):
    """
    Renders risk prediction gauge, risk level hero card, and target horizon details.
    """
    st.markdown("""
    <h3 style="margin: 0 0 12px 0; font-size: 1.3rem; font-weight: 700; color: #f8fafc;">
        🎯 Early Spike Prediction (2-Hour Horizon)
    </h3>
    """, unsafe_allow_html=True)
    
    risk_pct = float(pred_dict.get("risk_percentage", 0.0))
    risk_level = pred_dict.get("risk_level", "LOW")
    horizon = pred_dict.get("prediction_horizon", "2 hours")
    threshold = float(pred_dict.get("threshold_mgdl", 40.0))
    ts = pred_dict.get("prediction_timestamp", "N/A")
    
    col1, col2 = st.columns([1.1, 1.2])
    
    with col1:
        # High-impact Gauge Chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_pct,
            number={'suffix': "%", 'font': {'size': 46, 'color': '#f8fafc', 'family': 'Plus Jakarta Sans'}},
            title={'text': f"Spike Risk Probability (Next {horizon})", 'font': {'size': 15, 'color': '#94a3b8'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
                'bar': {'color': "#f43f5e" if risk_level == "HIGH" else "#f59e0b" if risk_level == "MODERATE" else "#10b981", 'thickness': 0.3},
                'bgcolor': "rgba(15, 23, 42, 0.8)",
                'borderwidth': 1,
                'bordercolor': "rgba(255, 255, 255, 0.1)",
                'steps': [
                    {'range': [0, 30], 'color': 'rgba(16, 185, 129, 0.15)'},
                    {'range': [30, 65], 'color': 'rgba(245, 158, 11, 0.15)'},
                    {'range': [65, 100], 'color': 'rgba(244, 63, 94, 0.15)'}
                ],
                'threshold': {
                    'line': {'color': "#ffffff", 'width': 4},
                    'thickness': 0.75,
                    'value': risk_pct
                }
            }
        ))
        fig.update_layout(
            height=260,
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=30, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        if risk_level == "HIGH":
            border_c = "#f43f5e"
            bg_c = "rgba(244, 63, 94, 0.1)"
            badge_t = "🔴 CRITICAL FORECAST: HIGH RISK"
            msg = f"The Digital Twin forecasts a **high likelihood ({risk_pct:.1f}%)** of a significant glucose spike (**≥ {threshold:.0f} mg/dL**) in the next **{horizon}**."
            recommendation = "💡 **Recommended Action:** Consider immediate light activity (walking) or reviewing rapid-acting insulin protocols as per physician guidance."
        elif risk_level == "MODERATE":
            border_c = "#f59e0b"
            bg_c = "rgba(245, 158, 11, 0.1)"
            badge_t = "🟡 ELEVATED FORECAST: MODERATE RISK"
            msg = f"The Digital Twin detects **moderate glucose elevation risk ({risk_pct:.1f}%)** over the next **{horizon}**."
            recommendation = "💡 **Recommended Action:** Monitor continuous glucose sensor trend lines closely and avoid high-glycemic snacks."
        else:
            border_c = "#10b981"
            bg_c = "rgba(16, 185, 129, 0.1)"
            badge_t = "🟢 STABLE FORECAST: LOW RISK"
            msg = f"The Digital Twin predicts a **stable glycemic trajectory ({risk_pct:.1f}%)** for the next **{horizon}**."
            recommendation = "💡 **Recommended Action:** Maintain current activity and nutrition schedule."
            
        st.markdown(f"""
        <div style="background: {bg_c}; border-left: 4px solid {border_c}; border-radius: 10px; padding: 16px 20px;">
            <div style="font-weight: 800; font-size: 1.1rem; color: {border_c}; margin-bottom: 6px;">{badge_t}</div>
            <p style="color: #cbd5e1; font-size: 0.92rem; margin: 0 0 10px 0;">{msg}</p>
            <div style="font-size: 0.85rem; color: #f8fafc; background: rgba(0,0,0,0.25); padding: 8px 12px; border-radius: 6px;">{recommendation}</div>
        </div>
        
        <div style="display: flex; gap: 20px; margin-top: 14px; font-size: 0.82rem; color: #94a3b8;">
            <div>🎯 <strong>Target Event:</strong> Δ Glucose ≥ {threshold:.0f} mg/dL</div>
            <div>⏱️ <strong>Horizon:</strong> {horizon} (8x 15m)</div>
            <div>📅 <strong>Last Prediction:</strong> <code style="color: #38bdf8;">{ts}</code></div>
        </div>
        """, unsafe_allow_html=True)
