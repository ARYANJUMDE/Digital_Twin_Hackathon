import React from 'react';
import { Target, AlertCircle, CheckCircle, Clock } from 'lucide-react';

export default function PredictionView({ prediction }) {
  if (!prediction) return null;

  const riskPct = prediction.risk_percentage || 0;
  const riskLevel = prediction.risk_level || 'LOW';
  const horizon = prediction.prediction_horizon || '2 hours';
  const threshold = prediction.threshold_mgdl || 40;

  const borderC = riskLevel === 'HIGH' ? '#f43f5e' : riskLevel === 'MODERATE' ? '#f59e0b' : '#10b981';
  const bgC = riskLevel === 'HIGH' ? 'rgba(244, 63, 94, 0.1)' : riskLevel === 'MODERATE' ? 'rgba(245, 158, 11, 0.1)' : 'rgba(16, 185, 129, 0.1)';
  const badgeT = riskLevel === 'HIGH' ? '🔴 CRITICAL FORECAST: HIGH RISK' : riskLevel === 'MODERATE' ? '🟡 ELEVATED FORECAST: MODERATE RISK' : '🟢 STABLE FORECAST: LOW RISK';
  
  const msg = riskLevel === 'HIGH'
    ? `The Digital Twin forecasts a high likelihood (${riskPct.toFixed(1)}%) of a significant glucose spike (≥ ${threshold} mg/dL) in the next ${horizon}.`
    : riskLevel === 'MODERATE'
    ? `The Digital Twin detects moderate glucose elevation risk (${riskPct.toFixed(1)}%) over the next ${horizon}.`
    : `The Digital Twin predicts a stable glycemic trajectory (${riskPct.toFixed(1)}%) for the next ${horizon}.`;

  const recommendation = riskLevel === 'HIGH'
    ? '💡 Recommended Action: Consider immediate light physical activity (walking) or reviewing rapid-acting insulin protocols as per physician guidance.'
    : riskLevel === 'MODERATE'
    ? '💡 Recommended Action: Monitor continuous glucose sensor trend lines closely and avoid high-glycemic snacks.'
    : '💡 Recommended Action: Maintain current physical activity and nutrition schedule.';

  return (
    <div className="glass-panel">
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '8px', margin: 0 }}>
          <Target size={20} style={{ color: borderC }} /> Early Spike Risk Prediction ({horizon})
        </h3>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', alignItems: 'center' }}>
        {/* Risk Probability Arc Card */}
        <div style={{ background: 'rgba(15, 23, 42, 0.8)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '16px', padding: '24px', textAlign: 'center' }}>
          <span style={{ fontSize: '0.85rem', color: '#94a3b8', fontWeight: 600, textTransform: 'uppercase' }}>Spike Risk Probability</span>
          <div style={{ fontSize: '3.6rem', fontWeight: 800, color: borderC, lineHeight: 1.1, margin: '8px 0' }}>
            {riskPct.toFixed(1)}<span style={{ fontSize: '1.8rem' }}>%</span>
          </div>
          <div style={{ display: 'inline-block', background: bgC, border: `1px solid ${borderC}`, color: borderC, padding: '4px 14px', borderRadius: '12px', fontSize: '0.85rem', fontWeight: 700 }}>
            {riskLevel} RISK LEVEL
          </div>

          <div style={{ width: '100%', height: '8px', background: 'rgba(255, 255, 255, 0.1)', borderRadius: '4px', marginTop: '16px', overflow: 'hidden' }}>
            <div style={{ width: `${Math.min(100, riskPct)}%`, height: '100%', background: borderC, transition: 'width 0.4s ease' }}></div>
          </div>
        </div>

        {/* Clinical Alert Card */}
        <div style={{ background: bgC, borderLeft: `4px solid ${borderC}`, borderRadius: '12px', padding: '20px' }}>
          <div style={{ fontWeight: 800, fontSize: '1.05rem', color: borderC, marginBottom: '8px' }}>
            {badgeT}
          </div>
          <p style={{ color: '#cbd5e1', fontSize: '0.92rem', marginBottom: '12px', lineHeight: 1.5 }}>
            {msg}
          </p>
          <div style={{ fontSize: '0.85rem', color: '#f8fafc', background: 'rgba(0,0,0,0.3)', padding: '10px 14px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
            {recommendation}
          </div>

          <div style={{ display: 'flex', gap: '20px', marginTop: '16px', fontSize: '0.82rem', color: '#94a3b8', flexWrap: 'wrap' }}>
            <div>🎯 <strong>Target Event:</strong> Δ Glucose ≥ {threshold} mg/dL</div>
            <div>⏱️ <strong>Horizon:</strong> {horizon} (8x 15m)</div>
          </div>
        </div>
      </div>
    </div>
  );
}
