"""
Plotly Time-Series Charts Component for Streamlit Dashboard.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_timeseries_charts(df_history: pd.DataFrame):
    """
    Renders multi-metric interactive Plotly time-series charts for wearable sensor signals.
    """
    st.markdown("""
    <h3 style="margin: 0 0 4px 0; font-size: 1.3rem; font-weight: 700; color: #f8fafc;">
        📈 Continuous Wearable Telemetry Streams
    </h3>
    <p style="color: #94a3b8; font-size: 0.88rem; margin-bottom: 16px;">
        15-minute resolution time-series tracking CGM glucose, HR/HRV autonomic tone, physical activity, and dietary ingestion.
    </p>
    """, unsafe_allow_html=True)
    
    if df_history.empty:
        st.info("No time series data available for plotting.")
        return
        
    df = df_history.sort_values("timestamp").copy()
    
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=(
            "Continuous Glucose Monitoring (CGM) [mg/dL]",
            "Heart Rate (bpm) & HRV RMSSD (ms)",
            "Physical Activity (Steps) & Carbohydrate Ingestion (g)"
        )
    )
    
    # 1. Glucose trace
    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["glucose"],
            mode="lines+markers",
            name="Glucose (mg/dL)",
            line=dict(color="#38bdf8", width=2.5, shape="spline"),
            marker=dict(size=4, color="#38bdf8"),
            fill="tozeroy",
            fillcolor="rgba(56, 189, 248, 0.05)",
            hovertemplate="Glucose: %{y:.1f} mg/dL<extra></extra>"
        ),
        row=1, col=1
    )
    
    # High glucose threshold line (140 mg/dL)
    fig.add_hline(
        y=140, line_dash="dash", line_color="#ef4444",
        annotation_text="Hyperglycemia Threshold (140 mg/dL)",
        annotation_position="top right",
        annotation_font_color="#fca5a5",
        row=1, col=1
    )
    
    # Highlight meal events on glucose chart
    meal_df = df[df["meal_carbs"] > 0]
    if not meal_df.empty:
        fig.add_trace(
            go.Scatter(
                x=meal_df["timestamp"],
                y=meal_df["glucose"] + 15,
                mode="markers+text",
                name="Meal Ingestion",
                marker=dict(symbol="triangle-down", size=13, color="#f59e0b", line=dict(color="#ffffff", width=1)),
                text=[f"{c:.0f}g ({m})" for c, m in zip(meal_df["meal_carbs"], meal_df["meal_type"])],
                textposition="top center",
                textfont=dict(color="#fbbf24", size=11),
                hovertemplate="Meal: %{text}<extra></extra>"
            ),
            row=1, col=1
        )
        
    # 2. HR & HRV traces
    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["heart_rate"],
            mode="lines",
            name="Heart Rate (bpm)",
            line=dict(color="#f43f5e", width=2, shape="spline"),
            hovertemplate="HR: %{y:.0f} bpm<extra></extra>"
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["hrv"],
            mode="lines",
            name="HRV (ms)",
            line=dict(color="#10b981", width=2, dash="dot", shape="spline"),
            hovertemplate="HRV: %{y:.1f} ms<extra></extra>"
        ),
        row=2, col=1
    )
    
    # 3. Steps & Carbs
    fig.add_trace(
        go.Bar(
            x=df["timestamp"],
            y=df["steps"],
            name="Steps",
            marker_color="#8b5cf6",
            opacity=0.75,
            hovertemplate="Steps: %{y}<extra></extra>"
        ),
        row=3, col=1
    )
    
    fig.add_trace(
        go.Bar(
            x=df["timestamp"],
            y=df["meal_carbs"],
            name="Carbs (g)",
            marker_color="#f59e0b",
            opacity=0.9,
            hovertemplate="Carbs: %{y}g<extra></extra>"
        ),
        row=3, col=1
    )
    
    fig.update_layout(
        height=760,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.5)",
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11, color="#cbd5e1")),
        hovermode="x unified"
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(255, 255, 255, 0.05)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(255, 255, 255, 0.05)")
    
    st.plotly_chart(fig, use_container_width=True)
