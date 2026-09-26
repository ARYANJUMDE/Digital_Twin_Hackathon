import React from 'react';
import { Activity, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function Header({ patientId }) {
  return (
    <div style={{ marginBottom: '24px' }}>
      <div className="glass-panel" style={{ background: 'linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(30, 41, 59, 0.6) 100%)', padding: '24px 30px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <h1 className="title-gradient" style={{ fontSize: '2.2rem', margin: 0 }}>🧬 GlucoTwin</h1>
              <span style={{ background: 'rgba(56, 189, 248, 0.15)', border: '1px solid #38bdf8', color: '#38bdf8', padding: '3px 10px', borderRadius: '12px', fontSize: '0.78rem', fontWeight: 600 }}>
                React + FastAPI
              </span>
            </div>
            <p style={{ color: '#94a3b8', fontSize: '1rem', marginTop: '6px' }}>
              Next-Generation Healthcare Digital Twin for Early Glucose Spike Prediction (2-Hour Horizon)
            </p>
          </div>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', background: 'rgba(16, 185, 129, 0.12)', border: '1px solid #10b981', color: '#34d399', padding: '8px 16px', borderRadius: '20px', fontSize: '0.85rem', fontWeight: 600 }}>
              <span style={{ height: '8px', width: '8px', backgroundColor: '#10b981', borderRadius: '50%', boxShadow: '0 0 10px #10b981', animation: 'pulse 1.5s infinite' }}></span>
              DIGITAL TWIN ENGINE ACTIVE
            </div>
          </div>
        </div>
      </div>

      <div style={{ background: 'linear-gradient(90deg, rgba(239, 68, 68, 0.12) 0%, rgba(245, 158, 11, 0.12) 100%)', borderLeft: '4px solid #ef4444', borderRadius: '8px', padding: '10px 16px', color: '#fca5a5', fontSize: '0.85rem', marginTop: '16px', display: 'flex', alignItems: 'center', gap: '10px' }}>
        <AlertTriangle size={18} style={{ color: '#ef4444', flexShrink: 0 }} />
        <div>
          <strong>RESEARCH PROOF-OF-CONCEPT:</strong> GlucoTwin uses synthetic patient & wearable sensor telemetry for demonstration. This platform is not intended for clinical diagnosis, treatment, or direct medical decision-making.
        </div>
      </div>
    </div>
  );
}
