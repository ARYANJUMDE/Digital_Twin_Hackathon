import React from 'react';
import {
  ResponsiveContainer,
  ComposedChart,
  LineChart,
  BarChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ReferenceLine,
  Legend
} from 'recharts';
import { TrendingUp } from 'lucide-react';

export default function TimeSeriesCharts({ wearables }) {
  if (!wearables || wearables.length === 0) {
    return <div className="glass-panel" style={{ color: '#94a3b8' }}>No time series data available for plotting.</div>;
  }

  // Format timestamp strings for chart axis (HH:mm)
  const chartData = wearables.map((w) => {
    const dt = new Date(w.timestamp);
    const timeLabel = isNaN(dt.getTime()) ? w.timestamp.slice(11, 16) : dt.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    return {
      ...w,
      timeLabel,
      cgmThreshold: 140
    };
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div className="glass-panel">
        <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
          <TrendingUp size={20} style={{ color: '#38bdf8' }} /> Continuous Glucose Monitoring (CGM) [mg/dL]
        </h3>
        <p style={{ color: '#94a3b8', fontSize: '0.85rem', marginBottom: '16px' }}>
          Real-time glucose telemetry with 140 mg/dL hyperglycemia target line and meal flags.
        </p>

        <div style={{ width: '100%', height: 260 }}>
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="timeLabel" stroke="#64748b" tick={{ fontSize: 11 }} />
              <YAxis domain={['dataMin - 10', 'dataMax + 20']} stroke="#64748b" tick={{ fontSize: 11 }} />
              <Tooltip
                contentStyle={{ background: '#0f172a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', color: '#f8fafc' }}
                formatter={(val, name) => [typeof val === 'number' ? val.toFixed(1) : val, name]}
              />
              <Legend verticalAlign="top" height={36} />
              <ReferenceLine y={140} label={{ value: '140 mg/dL Threshold', fill: '#f43f5e', fontSize: 11 }} stroke="#f43f5e" strokeDasharray="4 4" />
              <Line type="monotone" dataKey="glucose" name="Glucose (mg/dL)" stroke="#38bdf8" strokeWidth={2.5} dot={false} activeDot={{ r: 6 }} />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Autonomic Vitals (HR & HRV) */}
      <div className="glass-panel">
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc', marginBottom: '4px' }}>
          🫀 Heart Rate (bpm) & HRV RMSSD (ms)
        </h3>
        <p style={{ color: '#94a3b8', fontSize: '0.85rem', marginBottom: '16px' }}>
          Autonomic tone tracking sympathetic stress and recovery responses.
        </p>

        <div style={{ width: '100%', height: 220 }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="timeLabel" stroke="#64748b" tick={{ fontSize: 11 }} />
              <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
              <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', color: '#f8fafc' }} />
              <Legend verticalAlign="top" height={36} />
              <Line type="monotone" dataKey="heart_rate" name="Heart Rate (bpm)" stroke="#f43f5e" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="hrv" name="HRV (ms)" stroke="#10b981" strokeWidth={2} strokeDasharray="3 3" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Physical Activity & Carbs Ingestion */}
      <div className="glass-panel">
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc', marginBottom: '4px' }}>
          🏃 Physical Activity (Steps) & Dietary Carbs (g)
        </h3>
        <div style={{ width: '100%', height: 220, marginTop: '12px' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="timeLabel" stroke="#64748b" tick={{ fontSize: 11 }} />
              <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
              <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', color: '#f8fafc' }} />
              <Legend verticalAlign="top" height={36} />
              <Bar dataKey="steps" name="Steps" fill="#8b5cf6" opacity={0.8} />
              <Bar dataKey="meal_carbs" name="Carbs (g)" fill="#f59e0b" opacity={0.9} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
