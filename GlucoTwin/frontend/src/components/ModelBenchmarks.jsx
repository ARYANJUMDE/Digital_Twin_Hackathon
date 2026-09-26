import React from 'react';
import { Award, Cpu, ShieldCheck } from 'lucide-react';

export default function ModelBenchmarks({ metrics }) {
  if (!metrics) {
    return <div className="glass-panel" style={{ color: '#94a3b8' }}>Loading Model Benchmark Metrics...</div>;
  }

  const modelNames = Object.keys(metrics);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div className="glass-panel">
        <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
          <Cpu size={20} style={{ color: '#38bdf8' }} /> Machine Learning Model Benchmarks
        </h3>
        <p style={{ color: '#94a3b8', fontSize: '0.85rem', marginBottom: '20px' }}>
          Comparative evaluation of candidate classifiers trained on historical wearable and EHR features.
        </p>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.9rem' }}>
            <thead>
              <tr style={{ background: 'rgba(15, 23, 42, 0.9)', borderBottom: '1px solid rgba(255,255,255,0.1)', color: '#94a3b8' }}>
                <th style={{ padding: '12px 16px' }}>Model Name</th>
                <th style={{ padding: '12px 16px' }}>Precision</th>
                <th style={{ padding: '12px 16px' }}>Recall</th>
                <th style={{ padding: '12px 16px' }}>F1 Score</th>
                <th style={{ padding: '12px 16px' }}>ROC-AUC</th>
                <th style={{ padding: '12px 16px' }}>PR-AUC</th>
              </tr>
            </thead>
            <tbody>
              {modelNames.map((name) => {
                const m = metrics[name];
                const isBest = name === 'XGBoost';
                return (
                  <tr
                    key={name}
                    style={{
                      borderBottom: '1px solid rgba(255,255,255,0.05)',
                      background: isBest ? 'rgba(56, 189, 248, 0.05)' : 'transparent'
                    }}
                  >
                    <td style={{ padding: '14px 16px', fontWeight: 700, color: isBest ? '#38bdf8' : '#f8fafc' }}>
                      {name} {isBest && <span style={{ fontSize: '0.72rem', background: 'rgba(56, 189, 248, 0.2)', color: '#38bdf8', padding: '2px 8px', borderRadius: '4px', marginLeft: '8px' }}>CHAMPION</span>}
                    </td>
                    <td style={{ padding: '14px 16px', color: '#cbd5e1' }}>{m.precision.toFixed(4)}</td>
                    <td style={{ padding: '14px 16px', color: '#cbd5e1' }}>{m.recall.toFixed(4)}</td>
                    <td style={{ padding: '14px 16px', fontWeight: 700, color: '#f8fafc' }}>{m.f1_score.toFixed(4)}</td>
                    <td style={{ padding: '14px 16px', fontWeight: 700, color: '#38bdf8' }}>{m.roc_auc.toFixed(4)}</td>
                    <td style={{ padding: '14px 16px', color: '#cbd5e1' }}>{m.pr_auc.toFixed(4)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Confusion Matrices Grid */}
      <div className="glass-panel">
        <h4 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#f8fafc', marginBottom: '16px' }}>Confusion Matrices</h4>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '20px' }}>
          {modelNames.map((name) => {
            const cm = metrics[name].confusion_matrix;
            return (
              <div key={name} style={{ background: 'rgba(15, 23, 42, 0.6)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '12px', padding: '16px' }}>
                <h5 style={{ color: '#38bdf8', fontSize: '0.9rem', fontWeight: 700, marginBottom: '12px' }}>{name}</h5>

                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem', textAlign: 'center' }}>
                  <thead>
                    <tr style={{ color: '#94a3b8' }}>
                      <th></th>
                      <th style={{ padding: '6px' }}>Pred No Spike</th>
                      <th style={{ padding: '6px' }}>Pred Spike</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td style={{ fontWeight: 600, color: '#94a3b8', padding: '6px' }}>Actual No Spike</td>
                      <td style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34d399', fontWeight: 700, padding: '8px' }}>{cm[0][0]}</td>
                      <td style={{ background: 'rgba(244, 63, 94, 0.15)', color: '#f43f5e', padding: '8px' }}>{cm[0][1]}</td>
                    </tr>
                    <tr>
                      <td style={{ fontWeight: 600, color: '#94a3b8', padding: '6px' }}>Actual Spike</td>
                      <td style={{ background: 'rgba(244, 63, 94, 0.15)', color: '#f43f5e', padding: '8px' }}>{cm[1][0]}</td>
                      <td style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34d399', fontWeight: 700, padding: '8px' }}>{cm[1][1]}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
