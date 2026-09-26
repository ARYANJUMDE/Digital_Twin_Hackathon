import React from 'react';
import { User, Activity, Heart, Zap, Moon, Utensils, Award } from 'lucide-react';
import PredictionView from './PredictionView';

export default function TwinDashboard({ ehr, twinData }) {
  if (!ehr || !twinData) {
    return <div style={{ color: '#94a3b8' }}>Loading Digital Twin State...</div>;
  }

  const { current_state, prediction } = twinData;
  const vitals = current_state?.current_vitals || {};
  const profile = current_state?.profile || ehr;

  const bmi = profile.bmi || 0;
  const bmiStatus = bmi < 25 ? 'Normal' : bmi < 30 ? 'Overweight' : 'Obese';
  const hba1c = profile.hba1c || 0;
  const hbaStatus = hba1c < 6.5 ? 'Controlled' : hba1c < 8.0 ? 'Elevated' : 'High Risk';

  const gVal = vitals.glucose || 0;
  const gStatus = gVal < 140 ? 'Normal' : gVal < 180 ? 'Elevated' : 'Hyperglycemic';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* EHR Profile Card */}
      <div className="glass-panel">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '8px', margin: 0 }}>
            <User size={20} style={{ color: '#38bdf8' }} /> Patient Clinical Profile (EHR)
          </h3>
          <span style={{ background: 'rgba(56, 189, 248, 0.12)', border: '1px solid #38bdf8', color: '#38bdf8', padding: '4px 12px', borderRadius: '16px', fontSize: '0.82rem', fontWeight: 600 }}>
            ID: {profile.patient_id}
          </span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '14px' }}>
          <div className="metric-box">
            <span className="metric-label">Age / Sex</span>
            <span className="metric-value">{profile.age} yrs / {profile.sex}</span>
          </div>

          <div className="metric-box">
            <span className="metric-label">BMI</span>
            <span className="metric-value">{bmi.toFixed(1)} kg/m²</span>
            <span className="metric-delta" style={{ background: bmi < 25 ? 'rgba(16, 185, 129, 0.2)' : 'rgba(244, 63, 94, 0.2)', color: bmi < 25 ? '#34d399' : '#f43f5e' }}>
              {bmiStatus}
            </span>
          </div>

          <div className="metric-box">
            <span className="metric-label">HbA1c Level</span>
            <span className="metric-value">{hba1c.toFixed(1)}%</span>
            <span className="metric-delta" style={{ background: hba1c < 6.5 ? 'rgba(16, 185, 129, 0.2)' : 'rgba(245, 158, 11, 0.2)', color: hba1c < 6.5 ? '#34d399' : '#fbbf24' }}>
              {hbaStatus}
            </span>
          </div>

          <div className="metric-box">
            <span className="metric-label">Diabetes Status</span>
            <span className="metric-value" style={{ fontSize: '1.25rem' }}>{profile.diabetes_status}</span>
          </div>
        </div>

        <div style={{ background: 'rgba(15, 23, 42, 0.6)', border: '1px solid rgba(255, 255, 255, 0.06)', padding: '12px 18px', borderRadius: '10px', marginTop: '14px', fontSize: '0.88rem', color: '#cbd5e1', display: 'flex', flexWrap: 'wrap', gap: '24px' }}>
          <div>💊 <strong>Medication:</strong> <span style={{ color: '#38bdf8' }}>{profile.medication || 'None'}</span></div>
          <div>⏳ <strong>Duration:</strong> <span style={{ color: '#f8fafc' }}>{typeof profile.diabetes_duration_years === 'number' ? profile.diabetes_duration_years.toFixed(1) : profile.diabetes_duration_years} yrs</span></div>
          <div>🫀 <strong>Hypertension:</strong> <span style={{ color: profile.hypertension === 1 ? '#f43f5e' : '#34d399' }}>{profile.hypertension === 1 ? 'Diagnosed' : 'None'}</span></div>
          <div>🧬 <strong>Genetic Risk Score:</strong> <span style={{ color: '#a78bfa' }}>{typeof profile.family_risk_score === 'number' ? profile.family_risk_score.toFixed(2) : profile.family_risk_score} / 1.0</span></div>
        </div>
      </div>

      {/* Digital Twin Vitals Telemetry Monitor */}
      <div className="glass-panel">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '8px', margin: 0 }}>
            <Activity size={20} style={{ color: '#10b981' }} /> Digital Twin Vitals Telemetry Monitor
          </h3>
          <span style={{ fontSize: '0.82rem', color: '#94a3b8' }}>
            Sync Timestamp: <code style={{ color: '#38bdf8' }}>{vitals.timestamp}</code>
          </span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(170px, 1fr))', gap: '14px' }}>
          <div className="metric-box">
            <span className="metric-label">Continuous Glucose</span>
            <span className="metric-value">{gVal.toFixed(1)} <span style={{ fontSize: '0.9rem', color: '#94a3b8' }}>mg/dL</span></span>
            <span className="metric-delta" style={{ background: gVal < 140 ? 'rgba(16, 185, 129, 0.2)' : 'rgba(244, 63, 94, 0.2)', color: gVal < 140 ? '#34d399' : '#f43f5e' }}>
              {gStatus}
            </span>
          </div>

          <div className="metric-box">
            <span className="metric-label">Heart Rate</span>
            <span className="metric-value">{vitals.heart_rate?.toFixed(0)} <span style={{ fontSize: '0.9rem', color: '#94a3b8' }}>bpm</span></span>
          </div>

          <div className="metric-box">
            <span className="metric-label">HRV (RMSSD)</span>
            <span className="metric-value">{vitals.hrv?.toFixed(1)} <span style={{ fontSize: '0.9rem', color: '#94a3b8' }}>ms</span></span>
          </div>

          <div className="metric-box">
            <span className="metric-label">Steps (15m)</span>
            <span className="metric-value">{vitals.steps}</span>
            <span className="metric-delta" style={{ background: 'rgba(139, 92, 246, 0.2)', color: '#c084fc' }}>
              {vitals.activity_level}
            </span>
          </div>

          <div className="metric-box">
            <span className="metric-label">Sleep Duration</span>
            <span className="metric-value">{vitals.sleep_hours?.toFixed(1)} <span style={{ fontSize: '0.9rem', color: '#94a3b8' }}>hrs</span></span>
          </div>
        </div>

        {vitals.meal_carbs > 0 && (
          <div style={{ background: 'rgba(245, 158, 11, 0.12)', border: '1px solid rgba(245, 158, 11, 0.3)', borderRadius: '10px', padding: '12px 18px', marginTop: '14px', color: '#fbbf24', fontSize: '0.88rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Utensils size={18} /> <strong>Recent Dietary Ingestion:</strong> {vitals.meal_carbs.toFixed(0)}g Carbs ({vitals.meal_type})
            </div>
            <span style={{ fontSize: '0.78rem', background: 'rgba(0,0,0,0.3)', padding: '4px 10px', borderRadius: '6px' }}>
              Digestive Absorption Active
            </span>
          </div>
        )}
      </div>

      {/* Spike Risk Prediction View */}
      <PredictionView prediction={prediction} />
    </div>
  );
}
