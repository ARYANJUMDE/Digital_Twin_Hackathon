import React from 'react';
import { Clock, Utensils, AlertCircle, Activity } from 'lucide-react';

export default function PatientTimeline({ wearables }) {
  if (!wearables || wearables.length === 0) {
    return <div className="glass-panel" style={{ color: '#94a3b8' }}>No event history available.</div>;
  }

  // Filter key events: Meals > 0, High Glucose >= 160, High Steps > 1000
  const events = [];
  [...wearables].reverse().forEach((w) => {
    const ts = w.timestamp;
    const g = w.glucose;
    const carbs = w.meal_carbs;
    const mtype = w.meal_type;
    const steps = w.steps;

    if (carbs > 0) {
      events.push({
        id: `meal-${ts}`,
        timestamp: ts,
        icon: <Utensils size={16} style={{ color: '#fbbf24' }} />,
        type: 'Meal Ingestion',
        details: `${carbs.toFixed(0)}g carbs (${mtype})`,
        glucose: `${g.toFixed(1)} mg/dL`,
        severity: '🟡 Moderate',
        color: '#fbbf24'
      });
    }
    if (g >= 160) {
      events.push({
        id: `high-${ts}`,
        timestamp: ts,
        icon: <AlertCircle size={16} style={{ color: '#f43f5e' }} />,
        type: 'Hyperglycemia Alert',
        details: `Glucose elevated to ${g.toFixed(1)} mg/dL`,
        glucose: `${g.toFixed(1)} mg/dL`,
        severity: '🔴 High',
        color: '#f43f5e'
      });
    }
    if (steps >= 1000) {
      events.push({
        id: `steps-${ts}`,
        timestamp: ts,
        icon: <Activity size={16} style={{ color: '#34d399' }} />,
        type: 'Physical Activity',
        details: `${steps} steps recorded`,
        glucose: `${g.toFixed(1)} mg/dL`,
        severity: '🟢 Positive',
        color: '#34d399'
      });
    }
  });

  return (
    <div className="glass-panel">
      <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
        <Clock size={20} style={{ color: '#38bdf8' }} /> Patient Chronological Event Log
      </h3>
      <p style={{ color: '#94a3b8', fontSize: '0.85rem', marginBottom: '20px' }}>
        Audit trail of dietary ingestion, physical activity bursts, and hyperglycemia alerts.
      </p>

      {events.length === 0 ? (
        <div style={{ color: '#94a3b8' }}>No major physiological events recorded in recent history.</div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {events.slice(0, 15).map((evt) => (
            <div
              key={evt.id}
              style={{
                background: 'rgba(15, 23, 42, 0.6)',
                border: '1px solid rgba(255, 255, 255, 0.06)',
                borderRadius: '10px',
                padding: '12px 16px',
                display: 'flex',
                justifyDimension: 'space-between',
                alignItems: 'center',
                flexWrap: 'wrap',
                gap: '12px'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div style={{ padding: '8px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px' }}>
                  {evt.icon}
                </div>
                <div>
                  <div style={{ fontWeight: 700, fontSize: '0.9rem', color: '#f8fafc' }}>{evt.type}</div>
                  <div style={{ fontSize: '0.82rem', color: '#cbd5e1' }}>{evt.details}</div>
                </div>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '20px', marginLeft: 'auto', fontSize: '0.82rem' }}>
                <div>Glucose: <strong style={{ color: '#38bdf8' }}>{evt.glucose}</strong></div>
                <div style={{ color: evt.color, fontWeight: 600 }}>{evt.severity}</div>
                <div style={{ color: '#64748b' }}>{evt.timestamp.slice(0, 16)}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
