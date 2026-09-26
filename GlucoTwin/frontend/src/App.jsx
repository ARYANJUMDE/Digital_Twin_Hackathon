import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import TwinDashboard from './components/TwinDashboard';
import TimeSeriesCharts from './components/TimeSeriesCharts';
import PredictionView from './components/PredictionView';
import SHAPExplainer from './components/SHAPExplainer';
import WhatIfSimulator from './components/WhatIfSimulator';
import PatientTimeline from './components/PatientTimeline';
import ModelBenchmarks from './components/ModelBenchmarks';

import { Activity, TrendingUp, Target, FlaskConical, Clock, Cpu } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api';

export default function App() {
  const [patients, setPatients] = useState([]);
  const [selectedPatientId, setSelectedPatientId] = useState('');
  const [streamIndex, setStreamIndex] = useState(48);
  const [isAutoPlay, setIsAutoPlay] = useState(false);
  const [activeTab, setActiveTab] = useState('twin_dashboard');

  const [ehr, setEhr] = useState(null);
  const [wearables, setWearables] = useState([]);
  const [twinData, setTwinData] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  // 1. Fetch Patients & Model Benchmarks on mount
  useEffect(() => {
    async function initData() {
      try {
        const [resP, resM] = await Promise.all([
          fetch(`${API_BASE}/patients`),
          fetch(`${API_BASE}/models/metrics`)
        ]);

        const patientsList = await resP.json();
        const metricsData = await resM.json();

        setPatients(patientsList);
        setMetrics(metricsData);

        if (patientsList.length > 0) {
          setSelectedPatientId(patientsList[0].patient_id);
        }
      } catch (err) {
        console.error('Failed to initialize API data:', err);
      } finally {
        setLoading(false);
      }
    }
    initData();
  }, []);

  // 2. Fetch Patient Specific Data when patientId or streamIndex changes
  useEffect(() => {
    if (!selectedPatientId) return;

    async function fetchPatientTwin() {
      try {
        const [resEhr, resWear, resTwin] = await Promise.all([
          fetch(`${API_BASE}/patients/${selectedPatientId}/ehr`),
          fetch(`${API_BASE}/patients/${selectedPatientId}/wearables?stream_index=${streamIndex}`),
          fetch(`${API_BASE}/patients/${selectedPatientId}/twin?stream_index=${streamIndex}`)
        ]);

        const ehrData = await resEhr.json();
        const wearData = await resWear.json();
        const twinRes = await resTwin.json();

        setEhr(ehrData);
        setWearables(wearData);
        setTwinData(twinRes);
      } catch (err) {
        console.error('Error fetching twin data:', err);
      }
    }

    fetchPatientTwin();
  }, [selectedPatientId, streamIndex]);

  // 3. Auto-play effect for streaming
  useEffect(() => {
    let interval = null;
    if (isAutoPlay) {
      interval = setInterval(() => {
        setStreamIndex((prev) => prev + 1);
      }, 1500);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isAutoPlay]);

  const handleNextTick = () => {
    setStreamIndex((prev) => prev + 1);
  };

  const handleResetStream = () => {
    setStreamIndex(24);
  };

  const handleRunSimulation = async (modifications) => {
    const res = await fetch(`${API_BASE}/twin/simulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        patient_id: selectedPatientId,
        stream_index: streamIndex,
        modifications
      })
    });
    return await res.json();
  };

  const totalReadings = patients.find((p) => p.patient_id === selectedPatientId)?.total_sensor_readings || 1344;

  if (loading) {
    return (
      <div style={{ display: 'flex', height: '100vh', justifyContent: 'center', alignItems: 'center', background: '#070b14', color: '#38bdf8' }}>
        <h2>🧬 Initializing GlucoTwin Digital Twin Engine...</h2>
      </div>
    );
  }

  return (
    <div className="app-container">
      <Sidebar
        patients={patients}
        selectedPatientId={selectedPatientId}
        onSelectPatient={(id) => {
          setSelectedPatientId(id);
          setStreamIndex(48);
        }}
        streamIndex={streamIndex}
        totalReadings={totalReadings}
        onNextTick={handleNextTick}
        onResetStream={handleResetStream}
        isAutoPlay={isAutoPlay}
        onToggleAutoPlay={() => setIsAutoPlay(!isAutoPlay)}
        metrics={metrics}
      />

      <div className="main-content">
        <Header patientId={selectedPatientId} />

        {/* Tab Navigation */}
        <div className="tabs-container">
          <button
            className={`tab-button ${activeTab === 'twin_dashboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('twin_dashboard')}
          >
            <Activity size={16} /> Twin Dashboard
          </button>

          <button
            className={`tab-button ${activeTab === 'timeseries' ? 'active' : ''}`}
            onClick={() => setActiveTab('timeseries')}
          >
            <TrendingUp size={16} /> Time Series Signals
          </button>

          <button
            className={`tab-button ${activeTab === 'prediction_shap' ? 'active' : ''}`}
            onClick={() => setActiveTab('prediction_shap')}
          >
            <Target size={16} /> Spike Prediction & SHAP
          </button>

          <button
            className={`tab-button ${activeTab === 'whatif' ? 'active' : ''}`}
            onClick={() => setActiveTab('whatif')}
          >
            <FlaskConical size={16} /> What-If Simulator
          </button>

          <button
            className={`tab-button ${activeTab === 'timeline' ? 'active' : ''}`}
            onClick={() => setActiveTab('timeline')}
          >
            <Clock size={16} /> Patient Timeline
          </button>

          <button
            className={`tab-button ${activeTab === 'benchmarks' ? 'active' : ''}`}
            onClick={() => setActiveTab('benchmarks')}
          >
            <Cpu size={16} /> Model Benchmarks
          </button>
        </div>

        {/* Tab Contents */}
        {activeTab === 'twin_dashboard' && <TwinDashboard ehr={ehr} twinData={twinData} />}

        {activeTab === 'timeseries' && <TimeSeriesCharts wearables={wearables} />}

        {activeTab === 'prediction_shap' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <PredictionView prediction={twinData?.prediction} />
            <SHAPExplainer explanation={twinData?.explanation} />
          </div>
        )}

        {activeTab === 'whatif' && (
          <WhatIfSimulator
            patientId={selectedPatientId}
            streamIndex={streamIndex}
            currentVitals={twinData?.current_state?.current_vitals || {}}
            onRunSimulation={handleRunSimulation}
          />
        )}

        {activeTab === 'timeline' && <PatientTimeline wearables={wearables} />}

        {activeTab === 'benchmarks' && <ModelBenchmarks metrics={metrics} />}
      </div>
    </div>
  );
}
