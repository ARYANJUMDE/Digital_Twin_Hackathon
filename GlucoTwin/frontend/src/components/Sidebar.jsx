import React from 'react';
import { Users, FastForward, RotateCcw, Cpu, Play, Pause } from 'lucide-react';

export default function Sidebar({
  patients,
  selectedPatientId,
  onSelectPatient,
  streamIndex,
  totalReadings,
  onNextTick,
  onResetStream,
  isAutoPlay,
  onToggleAutoPlay,
  metrics
}) {
  const progressPct = totalReadings > 0 ? Math.min(100, Math.round((streamIndex / totalReadings) * 100)) : 0;

  return (
    <div className="sidebar">
      <div style={{ textAlign: 'center', paddingBottom: '12px', borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
        <div style={{ display: 'inline-flex', padding: '12px', background: 'rgba(56, 189, 248, 0.1)', borderRadius: '16px', marginBottom: '8px' }}>
          <Cpu size={32} style={{ color: '#38bdf8' }} />
        </div>
        <h2 style={{ fontSize: '1.3rem', fontWeight: 700, color: '#38bdf8', margin: 0 }}>Digital Twin Control</h2>
        <p style={{ fontSize: '0.8rem', color: '#64748b', marginTop: '4px' }}>Patient & Wearable Telemetry Manager</p>
      </div>

      {/* Patient Selector */}
      <div>
        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.85rem', fontWeight: 600, color: '#cbd5e1', marginBottom: '8px' }}>
          <Users size={16} style={{ color: '#38bdf8' }} /> Select Patient Profile
        </label>
        <select
          value={selectedPatientId}
          onChange={(e) => onSelectPatient(e.target.value)}
          style={{
            width: '100%',
            background: 'rgba(15, 23, 42, 0.9)',
            border: '1px solid rgba(255, 255, 255, 0.15)',
            color: '#f8fafc',
            padding: '10px 14px',
            borderRadius: '10px',
            fontSize: '0.9rem',
            fontWeight: 600,
            outline: 'none',
            cursor: 'pointer'
          }}
        >
          {patients.map((p) => (
            <option key={p.patient_id} value={p.patient_id}>
              {p.patient_id} ({p.age}y {p.sex}, {p.diabetes_status})
            </option>
          ))}
        </select>
      </div>

      {/* Live Wearable Streaming Controls */}
      <div style={{ background: 'rgba(15, 23, 42, 0.6)', border: '1px solid rgba(255,255,255,0.06)', borderRadius: '12px', padding: '16px' }}>
        <h3 style={{ fontSize: '0.92rem', fontWeight: 700, color: '#f8fafc', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <FastForward size={16} style={{ color: '#f59e0b' }} /> Wearable Stream (15m Ticks)
        </h3>

        <div style={{ display: 'flex', gap: '8px', marginBottom: '12px' }}>
          <button className="btn-primary" onClick={onNextTick} style={{ flex: 1, padding: '8px 12px', fontSize: '0.82rem' }}>
            <FastForward size={14} /> +15m Tick
          </button>

          <button
            className="btn-secondary"
            onClick={onToggleAutoPlay}
            style={{
              padding: '8px 12px',
              fontSize: '0.82rem',
              borderColor: isAutoPlay ? '#10b981' : 'rgba(255,255,255,0.1)',
              background: isAutoPlay ? 'rgba(16, 185, 129, 0.2)' : 'rgba(30, 41, 59, 0.8)',
              color: isAutoPlay ? '#34d399' : '#f8fafc'
            }}
          >
            {isAutoPlay ? <Pause size={14} /> : <Play size={14} />} {isAutoPlay ? 'Stop' : 'Auto'}
          </button>
        </div>

        <button className="btn-secondary" onClick={onResetStream} style={{ width: '100%', padding: '8px 12px', fontSize: '0.82rem', display: 'flex', justifyContent: 'center', gap: '6px' }}>
          <RotateCcw size={14} /> Reset Window
        </button>

        <div style={{ marginTop: '14px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', color: '#94a3b8', marginBottom: '4px' }}>
            <span>Window Index</span>
            <span style={{ color: '#38bdf8', fontWeight: 600 }}>{streamIndex} / {totalReadings}</span>
          </div>
          <div style={{ width: '100%', height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', overflow: 'hidden' }}>
            <div style={{ width: `${progressPct}%`, height: '100%', background: 'linear-gradient(90deg, #38bdf8, #818cf8)', transition: 'width 0.3s ease' }}></div>
          </div>
        </div>
      </div>

      {/* Model Benchmark Badges */}
      <div style={{ marginTop: 'auto' }}>
        <h3 style={{ fontSize: '0.88rem', fontWeight: 700, color: '#cbd5e1', marginBottom: '10px' }}>Active ML Ensembles</h3>
        {metrics && Object.keys(metrics).map((mName) => {
          const m = metrics[mName];
          const isBest = mName === 'XGBoost';
          return (
            <div
              key={mName}
              style={{
                background: 'rgba(15, 23, 42, 0.6)',
                border: isBest ? '1px solid #38bdf8' : '1px solid rgba(255,255,255,0.05)',
                borderRadius: '8px',
                padding: '8px 12px',
                marginBottom: '6px'
              }}
            >
              <div style={{ fontSize: '0.82rem', fontWeight: 600, color: isBest ? '#38bdf8' : '#e2e8f0', display: 'flex', justifyContent: 'space-between' }}>
                <span>{mName}</span>
                {isBest && <span style={{ fontSize: '0.7rem', background: 'rgba(56, 189, 248, 0.2)', color: '#38bdf8', padding: '1px 6px', borderRadius: '4px' }}>CHAMPION</span>}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '2px' }}>
                F1: <strong style={{ color: '#f8fafc' }}>{m.f1_score.toFixed(3)}</strong> | ROC-AUC: <strong style={{ color: '#f8fafc' }}>{m.roc_auc.toFixed(3)}</strong>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
