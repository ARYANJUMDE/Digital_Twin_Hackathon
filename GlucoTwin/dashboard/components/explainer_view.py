"""
SHAP Explanation View Component for Streamlit Dashboard.
"""
import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any

def render_shap_explanation(explanation_dict: Dict[str, Any]):
    """
    Renders SHAP feature contribution bar chart and impact breakdown list.
    """
    st.markdown("""
    <h3 style="margin: 0 0 4px 0; font-size: 1.3rem; font-weight: 700; color: #f8fafc;">
        🔍 Explainable AI — SHAP Feature Contributions
    </h3>
    <p style="color: #94a3b8; font-size: 0.88rem; margin-bottom: 16px;">
        Quantifies the exact push/pull of each physiological and clinical factor on the model's spike risk output.
    </p>
    """, unsafe_allow_html=True)
    
    contributions = explanation_dict.get("top_features", [])
    if not contributions:
        st.info("No feature contributions available.")
        return
        
    names = [c["feature_name"] for c in reversed(contributions)]
    shap_vals = [c["shap_value"] for c in reversed(contributions)]
    colors = ["#f43f5e" if v > 0 else "#10b981" for v in shap_vals]
    
    fig = go.Figure(go.Bar(
        x=shap_vals,
        y=names,
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(color='rgba(255, 255, 255, 0.15)', width=1)
        ),
        text=[f"{'▲ +' if v > 0 else '▼ '}{v:.3f}" for v in shap_vals],
        textposition="outside",
        textfont=dict(size=12, color="#f8fafc")
    ))
    
    fig.update_layout(
        title="Top 10 SHAP Feature Contributions to Glucose Spike Risk",
        title_font=dict(size=14, color="#cbd5e1"),
        xaxis_title="SHAP Value (Impact on Log-Odds / Probability)",
        yaxis=dict(autorange="reversed"),
        height=390,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=40, t=40, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Feature drivers list
    st.markdown("#### ⚡ Primary Risk Drivers Breakdown")
    c1, c2 = st.columns(2)
    
    risk_increasers = [c for c in contributions if c["shap_value"] > 0][:4]
    risk_decreasers = [c for c in contributions if c["shap_value"] < 0][:4]
    
    with c1:
        st.markdown("""
        <div style="background: rgba(244, 63, 94, 0.08); border: 1px solid rgba(244, 63, 94, 0.2); border-radius: 10px; padding: 14px 18px;">
            <div style="font-weight: 700; color: #f43f5e; font-size: 0.95rem; margin-bottom: 8px;">
                🔴 Factors Increasing Risk (▲ Push Up)
            </div>
        """, unsafe_allow_html=True)
        for item in risk_increasers:
            st.markdown(f"""
            <div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 6px;">
                • <strong>{item['feature_name']}</strong> (<code style="color: #f8fafc;">{item['feature_value']:.1f}</code>) 
                <span style="color: #f43f5e; font-weight: 600; float: right;">+{item['shap_value']:.3f} SHAP</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
            
    with c2:
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 10px; padding: 14px 18px;">
            <div style="font-weight: 700; color: #10b981; font-size: 0.95rem; margin-bottom: 8px;">
                🟢 Factors Decreasing Risk (▼ Pull Down)
            </div>
        """, unsafe_allow_html=True)
        for item in risk_decreasers:
            st.markdown(f"""
            <div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 6px;">
                • <strong>{item['feature_name']}</strong> (<code style="color: #f8fafc;">{item['feature_value']:.1f}</code>) 
                <span style="color: #10b981; font-weight: 600; float: right;">{item['shap_value']:.3f} SHAP</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
