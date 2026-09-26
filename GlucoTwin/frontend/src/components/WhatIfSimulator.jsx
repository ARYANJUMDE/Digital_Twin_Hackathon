import React, { useState } from 'react';
import { FlaskConical, Zap, AlertTriangle, ArrowRight } from 'lucide-react';

export default function WhatIfSimulator({ patientId, streamIndex, currentVitals, onRunSimulation }) {
  const [glucose, setGlucose] = useState(currentVitals.glucose || 120);
  const [carbs, setCarbs] = useState(currentVitals.meal_carbs || 0);
  const [sleep, setSleep] = useState(currentVitals.sleep_hours || 7);
  const [steps, setSteps] = useState(currentVitals.steps || 100);
  const [hr, setHr] = useState(currentVitals.heart_rate || 72);
  const [hrv, setHrv] = useState(currentVitals.hrv || 45);

  const [simResult, setSimResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSimulate = async () => {
    setLoading(true);
    const modifications = {
      glucose: parseFloat(glucose),
      meal_carbs: parseFloat(carbs),
      sleep_hours: parseFloat(sleep),
      steps: parseInt(steps),
      heart_rate: parseFloat(hr),
      hrv: parseFloat(hrv)
    };

    try {
      const res = await onRunSimulation(modifications);
      setSimResult(res);
    } catch (err) {
      console.error('Simulation error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div className="glass-panel" style={{ background: 'linear-gradient(135deg, rgba(14, 165, 233, 0.1) 0%, rgba(99, 102, 241, 0.1) 100%)', border: '1px solid rgba(56, 189, 248, 0.2)' }}>
        <h3 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#38bdf8', display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
          <FlaskConical size={22} /> Digital Twin What-If Scenario Simulator
        </h3>
        <p style={{ color: '#cbd5e1', fontSize: '0.9rem' }}>
          Interactively alter the patient's physiological parameters (e.g. reducing carbohydrate intake, adding post-meal activity) to model prospective risk changes.
        </p>
      </div>

      <div className="glass-panel">
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '24px' }}>
          {/* Glycemic Controls */}
          <div>
            <h4 style={{ color: '#f8fafc', fontSize: '0.92rem', fontWeight: 700, marginBottom: '14px' }}>🩸 Glycemic & Diet Controls</h4>
            <div style={{ marginBottom: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#cbd5e1', marginBottom: '4px' }}>
                <span>Simulated Glucose</span>
                <strong style={{ color: '#38bdf8' }}>{glucose} mg/dL</strong>
              </div>
              <input type="range" min="60" max="300" step="5" value={glucose} onChange={(e) => setGlucose(e.target.value)} />
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#cbd5e1', marginBottom: '4px' }}>
                <span>Meal Carbs Intake</span>
                <strong style={{ color: '#f59e0b' }}>{carbs}g</strong>
              </div>
              <input type="range" min="0" max="150" step="5" value={carbs} onChange={(e) => setCarbs(e.target.value)} />
            </div>
          </div>

          {/* Activity & Sleep Controls */}
          <div>
            <h4 style={{ color: '#f8fafc', fontSize: '0.92rem', fontWeight: 700, marginBottom: '14px' }}>🏃 Activity & Sleep Controls</h4>
            <div style={{ marginBottom: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#cbd5e1', marginBottom: '4px' }}>
                <span>Physical Steps (15m)</span>
                <strong style={{ color: '#c084fc' }}>{steps}</strong>
              </div>
              <input type="range" min="0" max="3500" step="100" value={steps} onChange={(e) => setSteps(e.target.value)} />
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#cbd5e1', marginBottom: '4px' }}>
                <span>Sleep Last Night</span>
                <strong style={{ color: '#34d399' }}>{sleep} hrs</strong>
              </div>
              <input type="range" min="3" max="10" step="0.5" value={sleep} onChange={(e) => setSleep(e.target.value)} />
            </div>
          </div>

          {/* Autonomic Vitals */}
          <div>
            <h4 style={{ color: '#f8fafc', fontSize: '0.92rem', fontWeight: 700, marginBottom: '14px' }}>🫀 Autonomic Vitals</h4>
            <div style={{ marginBottom: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#cbd5e1', marginBottom: '4px' }}>
                <span>Heart Rate</span>
                <strong style={{ color: '#f43f5e' }}>{hr} bpm</strong>
              </div>
              <input type="range" min="50" max="150" step="2" value={hr} onChange={(e) => setHr(e.target.value)} />
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#cbd5e1', marginBottom: '4px' }}>
                <span>HRV RMSSD</span>
                <strong style={{ color: '#10b981' }}>{hrv} ms</strong>
              </div>
              <input type="range" min="10" max="100" step="2" value={hrv} onChange={(e) => setHrv(e.target.value)} />
            </div>
          </div>
        </div>

        <button className="btn-primary" onClick={handleSimulate} disabled={loading} style={{ width: '100%', marginTop: '24px', padding: '14px' }}>
          <Zap size={18} /> {loading ? 'Computing Digital Twin Simulation...' : '⚡ RE-EVALUATE DIGITAL TWIN RISK'}
        </button>
      </div>

      {/* Simulation Outcomes Card */}
      {simResult && (
        <div className="glass-panel" style={{ borderLeft: '4px solid #38bdf8' }}>
          <h4 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc', marginBottom: '16px' }}>📊 Scenario Simulation Risk Outcomes</h4>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
            <div className="metric-box">
              <span className="metric-label">Baseline Risk</span>
              <span className="metric-value">{simResult.current_risk.toFixed(1)}%</span>
              <span className="metric-delta" style={{ background: 'rgba(255,255,255,0.1)' }}>{simResult.current_risk_level}</span>
            </div>

            <div className="metric-box">
              <span className="metric-label">Simulated Twin Risk</span>
              <span className="metric-value">{simResult.simulated_risk.toFixed(1)}%</span>
              <span className="metric-delta" style={{ background: 'rgba(56, 189, 248, 0.2)', color: '#38bdf8' }}>{simResult.simulated_risk_level}</span>
            </div>

            <div className="metric-box">
              <span className="metric-label">Risk Delta</span>
              <span className="metric-value" style={{ color: simResult.risk_delta_percentage_points > 0 ? '#f43f5e' : '#34d399' }}>
                {simResult.risk_delta_percentage_points > 0 ? `+${simResult.risk_delta_percentage_points.toFixed(1)}%` : `${simResult.risk_delta_percentage_points.toFixed(1)}%`}
              </span>
              <span className="metric-delta" style={{ background: simResult.risk_delta_percentage_points > 0 ? 'rgba(244, 63, 94, 0.2)' : 'rgba(16, 185, 129, 0.2)', color: simResult.risk_delta_percentage_points > 0 ? '#f43f5e' : '#34d399' }}>
                {simResult.risk_delta_percentage_points > 0 ? 'Increased Spike Risk' : 'Reduced Spike Risk'}
              </span>
            </div>
          </div>

          <div style={{ background: 'rgba(245, 158, 11, 0.1)', borderLeft: '4px solid #f59e0b', borderRadius: '8px', padding: '12px 16px', marginTop: '16px', fontSize: '0.85rem', color: '#fbbf24', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <AlertTriangle size={16} /> <strong>Medical Disclaimer:</strong> {simResult.disclaimer}
          </div>
        </div>
      )}
    </div>
  );
}
