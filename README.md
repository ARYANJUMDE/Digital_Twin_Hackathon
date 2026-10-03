# 🧬 GlucoTwin — Healthcare Digital Twin for Glucose Spike Prediction

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#-open-source-license)
[![React](https://img.shields.io/badge/Frontend-React%2018-61dafb.svg)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![XGBoost](https://img.shields.io/badge/ML-XGBoost-orange.svg)](https://xgboost.readthedocs.io/)
[![SHAP](https://img.shields.io/badge/Explainability-SHAP-purple.svg)](https://shap.readthedocs.io/)

> **Medical & Research Disclaimer:** GlucoTwin is a research proof-of-concept and simulation platform. It is designed purely for academic, research, and hackathon demonstration purposes and is not intended for real-world medical diagnosis, treatment, or clinical decision-making.

---

## 👥 Team Details & Institutional Information

### 🧑‍💻 Team Information

- **Team Name:** TwinPulse AI
- **Team Leader:** Aryan Jumde _(Role: Project Lead & Full-Stack / ML Developer)_
- **Contact Email:** jumdearyan7@gmail.com
- **GitHub Repository:** [https://github.com/ARYANJUMDE/Digital_Twin_Hackathon]

### 🏫 College / Incubator Information

- **Institution / College Name:** Ramdeobaba University, Nagpur
- **Department:** Department of Computer Science & Engineering
- **Location:** Nagpur, Maharashtra, India

---

## 📹 15–20 Minute Demo Video Walkthrough

> 🔗 **Unlisted YouTube Demo Link:** [**👉 CLICK HERE TO WATCH THE UNLISTED DEMO VIDEO (Paste YouTube Link Here)**](https://www.youtube.com/watch?v=YOUR_UNLISTED_VIDEO_ID)

### Video Walkthrough Agenda:

1. **00:00 – 03:00:** Problem Statement, Clinical Urgency & Glycemic Spikes Overview.
2. **03:00 – 06:00:** Healthcare Digital Twin Concept & Multi-Modal Sensor Dynamics.
3. **06:00 – 09:30:** Data Pipeline, Zero-Leakage Feature Engineering & XGBoost Model Benchmarks.
4. **09:30 – 13:00:** Live Clinician Dashboard Demonstration (Gauges, Signals & SHAP Explanations).
5. **13:00 – 16:30:** Interactive What-If Scenario Simulations & Risk Delta Validation.
6. **16:30 – 19:00:** Architecture, Codebase Walkthrough, Project Outcomes & Future Roadmap.

---

## 📊 Presentation & Architecture Deliverables

All presentation decks and architectural diagrams are available in both **PDF** and **PPTX** formats within the repository:

| Deliverable                        |  Format  | Repository File Link                                                                                                                                                               |
| ---------------------------------- | :------: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GlucoTwin Project Presentation** | **PDF**  | [GlucoTwin/presentations_and_architecture/GlucoTwin.pdf](GlucoTwin/presentations_and_architecture/GlucoTwin.pdf)                                                                   |
| **GlucoTwin Project Presentation** | **PPTX** | [GlucoTwin/presentations_and_architecture/GlucoTwin.pptx](GlucoTwin/presentations_and_architecture/GlucoTwin.pptx)                                                                 |
| **System Architecture Diagram**    | **PDF**  | [GlucoTwin/presentations_and_architecture/Gluco Twin System Architecture.pdf](GlucoTwin/presentations_and_architecture/Gluco%20Twin%20System%20Architecture.pdf)                 |
| **System Architecture Diagram**    | **PPTX** | [GlucoTwin/presentations_and_architecture/Gluco Twin System Architecture.pptx](GlucoTwin/presentations_and_architecture/Gluco%20Twin%20System%20Architecture.pptx)               |

---

## 🎯 Problem Statement & Healthcare Use Case

### 🚨 Problem Statement

Managing blood glucose variability is one of the greatest clinical challenges for over **537 million adults** living with pre-diabetes, Type 1, and Type 2 diabetes. Sudden, unpredicted postprandial glucose spikes lead to acute glycemic instability and compound long-term microvascular and macrovascular complications (retinopathy, nephropathy, neuropathy, and cardiovascular disease).

Traditional machine learning methods rely on static electronic health snapshots captured once every 3 to 6 months or analyze isolated point readings without temporal memory, failing to capture continuous physiological kinetics (digestion delays, sleep debt, exercise clearance).

### 🩺 Healthcare Use Case

**GlucoTwin** introduces a stateful **Healthcare Digital Twin** that continuously integrates static Electronic Health Record (EHR) profiles with high-frequency dynamic wearable sensor streams (Continuous Glucose Monitors, Smartwatches at 15-minute intervals).

- **Prediction Task:** Binary classification predicting whether an individual will experience a **significant glucose spike (≥ 40 mg/dL increase)** within the next **2 hours**.
- **Clinical Goal:** Provide a proactive 2-hour early warning window allowing clinicians and patients to execute micro-interventions (e.g., a 15-minute post-meal walk, meal portion adjustment) to mitigate hyperglycemia before it occurs.

---

## 💻 Technical Stack

| Tier                          | Technologies & Frameworks                           | Purpose                                                                                                |
| ----------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Backend API**               | Python 3.10+, FastAPI, Uvicorn, Pydantic            | High-performance asynchronous REST API serving `/predict`, `/simulate`, `/explain`, and `/benchmarks`. |
| **Machine Learning**          | XGBoost, Scikit-Learn, NumPy, Pandas, Joblib        | Champion gradient-boosted decision trees, feature pipelines, and StandardScaler normalization.         |
| **Explainable AI (XAI)**      | SHAP (SHapley Additive exPlanations)                | Game-theoretic local feature attribution for clinician transparency.                                   |
| **Frontend UI**               | React 18, Vite, Recharts, Lucide Icons, Vanilla CSS | Interactive clinician dashboard with real-time gauges, time-series charts, and simulation sliders.     |
| **Simulation & State Engine** | Python OOP (`DigitalTwin` Class)                    | Stateful temporal buffer maintaining continuous physiological state and What-If cloning.               |
| **Testing & Quality**         | Pytest, ReportLab, python-pptx                      | Comprehensive unit test suite and automated presentation generators.                                   |

---

## 🧬 Digital Twin Concept & Physiological Modeling

A **Digital Twin** is a dynamic, continuously updated virtual representation of a physical patient. In GlucoTwin, the twin maintains:

```text
Patient Static Profile (EHR Baseline)
                   +
Dynamic Wearable Sensor Stream (15-min ticks: CGM, HR, HRV, Steps, Sleep, Carbs)
                   ↓
Updated Digital Twin State (Trends, Rolling Averages, Digestion Decay, Sleep Deficit)
                   ↓
Real-Time ML Prediction & SHAP Feature Attributions
                   ↓
Interactive Clinician Dashboard & In-Silico What-If Simulation
```

### Realistic Physiological Dynamics:

1. **Carbohydrate Digestion Kinetics:** 30–90 minute absorption curves based on meal carbs and timing.
2. **Physical Activity Clearance:** Step accumulation actively clears circulating glucose and sensitizes insulin receptors.
3. **Sleep Deficit Compounding:** Sleep debt increases baseline insulin resistance and morning fasting drift.
4. **Autonomic Stress Coupling:** Elevated heart rate and suppressed HRV correlate with acute stress-induced glycemic spikes.

---

## 🏗️ System Architecture

```text
GlucoTwin/
├── README.md
├── requirements.txt
├── LICENSE
├── config/
│   └── config.yaml
├── data/
│   ├── raw/
│   ├── processed/
│   └── synthetic/
├── models/
│   ├── best_model.pkl
│   ├── preprocessor.pkl
│   └── metrics.json
├── presentations_and_architecture/
│   ├── GlucoTwin.pdf
│   ├── GlucoTwin.pptx
│   ├── Gluco Twin System Architecture.pdf
│   ├── Gluco Twin System Architecture.pptx
│   ├── project_summary.md
│   └── system_architecture.md
├── src/
│   ├── api/
│   │   └── main.py
│   ├── data/
│   │   ├── generate_synthetic.py
│   │   └── process.py
│   ├── twin/
│   │   └── digital_twin.py
│   ├── features/
│   │   └── build_features.py
│   ├── models/
│   │   ├── train.py
│   │   └── predict.py
│   ├── explainability/
│   │   └── explainer.py
│   └── utils/
│       ├── logger.py
│       └── config_loader.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── TwinDashboard.jsx
│   │   │   ├── SignalCharts.jsx
│   │   │   ├── PredictionView.jsx
│   │   │   ├── WhatIfSimulator.jsx
│   │   │   ├── PatientTimeline.jsx
│   │   │   └── ModelBenchmarks.jsx
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
├── notebooks/
│   └── exploratory_analysis.ipynb
└── tests/
    ├── test_data.py
    ├── test_features.py
    ├── test_models.py
    └── test_twin.py
```

---

## 🤖 AI/ML Model & Framework Details

### 1. Target Definition & Zero Data-Leakage Guard

- **Target Formula:**
  $$\text{Target} = 1 \quad \text{IF} \quad \left( \max_{t' \in [t+15\text{m}, t+2\text{h}]} \text{Glucose}(t') - \text{Glucose}(t) \ge 40 \text{ mg/dL} \right) \quad \text{ELSE} \quad 0$$
- **Zero Data-Leakage Safeguard:** Future readings in the $[t+15\text{m}, t+2\text{h}]$ prediction horizon are strictly used to compute the binary label `target_spike` and are **completely purged from the feature input matrix**.

### 2. Feature Engineering (35+ Variables)

- **Vitals & Trends:** Current glucose, 15m/30m/60m trend deltas, 1h/2h/4h rolling mean, std, min, and max.
- **Autonomic & Heart:** Heart rate, 1h HR rolling mean, HRV (SDNN), 1h HRV mean, 1h HRV delta.
- **Lifestyle & Sleep:** Step count, 1h/2h rolling steps, sleep hours, accumulated sleep deficit.
- **Nutrition:** Recent meal carbs (1h/2h), time elapsed since last meal.
- **EHR Profile:** Age, BMI, HbA1c, hypertension, diabetes duration, family risk score.

### 3. Machine Learning Benchmark Results

All candidate classification models were trained and evaluated on a holdout test split (80% train / 20% test):

| Candidate Model         | Precision  |   Recall   |  F1 Score  |  ROC-AUC   |   PR-AUC   | Selection Rationale                                                        |
| :---------------------- | :--------: | :--------: | :--------: | :--------: | :--------: | :------------------------------------------------------------------------- |
| **Logistic Regression** |   0.2675   |   0.8380   |   0.4049   |   0.8324   |   0.4145   | Baseline linear benchmark.                                                 |
| **Random Forest**       |   0.2810   |   0.8522   |   0.4226   |   0.8594   |   0.4748   | Non-linear ensemble model.                                                 |
| **XGBoost (Champion)**  | **0.2831** | **0.8782** | **0.4272** | **0.8716** | **0.5053** | **Champion Model:** Highest clinical Recall (87.82%) and ROC-AUC (0.8716). |

> 🏆 **Why XGBoost Won:** In proactive healthcare alerting, minimizing False Negatives (missing a real glucose spike) is paramount. XGBoost captures nearly 9 out of 10 oncoming spikes while maintaining superior area under the precision-recall curve under significant class imbalance (~12% positive spike frequency).

---

## 🔍 SHAP Explainability (XAI)

Using **TreeSHAP**, GlucoTwin computes exact additive feature attributions for every prediction, rendering the model completely transparent to clinicians:

```text
Current Glucose (168 mg/dL)    ↑ (+0.84 SHAP Impact) -> Driving Spike Risk
Meal Carbs 1h (85g)            ↑ (+0.62 SHAP Impact) -> Driving Spike Risk
Glucose Trend 30m (+18 mg/dL)  ↑ (+0.41 SHAP Impact) -> Driving Spike Risk
Sleep Deficit (3.2 hrs debt)   ↑ (+0.25 SHAP Impact) -> Driving Spike Risk
Recent Steps 1h (2,100 steps)  ↓ (-0.38 SHAP Impact) -> Mitigating Risk
HRV Recovery (+12 ms)          ↓ (-0.18 SHAP Impact) -> Mitigating Risk
```

---

## 🧪 Interactive What-If Scenario Simulation

Clinicians and patients can simulate prospective counterfactual interventions in real-time:

1. Adjust sliders for **Meal Carbs**, **Post-Meal Steps**, **Sleep Hours**, or **Current Glucose**.
2. Click **SIMULATE**.
3. GlucoTwin creates a clone of the digital twin, updates its physiological state, recalculates 35+ features, and re-evaluates the ML model.
4. Outputs real-time side-by-side risk metric deltas:

```text
Current State:    Meal Carbs: 85g | Steps: 200    -> Predicted Risk: 78.4% (HIGH)
Simulated State:  Meal Carbs: 45g | Steps: 2,500  -> Simulated Risk: 24.1% (LOW)
────────────────────────────────────────────────────────────────────────────────
Risk Delta:       -54.3 percentage points (Spike Successfully Averted!)
```

---

## 🖥️ Clinician Dashboard

Built with **React 18**, **Vite**, and **Recharts**, featuring 6 interactive tabs:

1. **Twin Dashboard:** Patient EHR metrics, Digital Twin state gauges, real-time risk banner.
2. **Time Series Signals:** Synchronized Recharts multi-sensor streams (CGM, HR, HRV, Steps, Carbs).
3. **Spike Prediction & SHAP:** Probability radial dial + SHAP waterfall feature impact chart.
4. **What-If Simulation:** Interactive parameter controls + instant risk differential display.
5. **Patient Timeline:** Chronological clinical events (meals, workouts, alerts).
6. **ML Model Benchmarks:** Live comparative metrics table and ROC evaluation plots.

---

## ⚙️ Installation & Running Guide

### Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- Git

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/ARYANJUMDE/Digital_Twin_Hackathon
cd GlucoTwin
pip install -r requirements.txt
```

### 2. Run Data & ML Pipelines

```bash
# 1. Generate synthetic EHR and wearable datasets (50 patients, 67,200 ticks)
python -m src.data.generate_synthetic

# 2. Build 35+ engineered features with zero-leakage preprocessing
python -m src.data.process

# 3. Train and benchmark candidate ML models (XGBoost, Random Forest, Logistic Regression)
python -m src.models.train
```

### 3. Launch Backend API & React Frontend

```bash
# Terminal 1: Start FastAPI backend (port 8000)
python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000

# Terminal 2: Start Vite React frontend (port 5173)
cd frontend
npm install
npm run dev
```

### 4. Run Unit Tests

```bash
pytest
```

---

## 📄 Open-Source License

This project is licensed under the **MIT Open Source License**. See the [GlucoTwin/LICENSE](GlucoTwin/LICENSE) file for full details.

```text
MIT License

Copyright (c) 2026 TwinPulse AI (Lead: Aryan Jumde)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🌐 Public Accessibility & Compliance Checklist

- [x] **Team details:** Included with Team Name (`TwinPulse AI`) and Team Lead (`Aryan Jumde`).
- [x] **College / Incubator Information:** Included with institutional details (`Ramdeobaba University, Nagpur`).
- [x] **Project Title:** Clearly stated (`GlucoTwin — Healthcare Digital Twin for Glucose Spike Prediction`).
- [x] **Problem Statement:** Documented under the Problem Statement section.
- [x] **Healthcare Use Case:** Detailed for continuous glucose monitoring & 2h spike prediction.
- [x] **Technical Stack:** Full breakdown of backend, frontend, ML, XAI, and simulation libraries.
- [x] **AI/ML Model & Framework Details:** Full benchmark matrix, zero-leakage guard, and SHAP XAI included.
- [x] **15-20 min Demo Video:** Section added with Unlisted YouTube link placeholder and video agenda.
- [x] **Open-source License Details:** Complete MIT license terms and file link provided.
- [x] **Architecture Diagram (PDF/PPT):** Available and linked directly in [`presentations_and_architecture/`](GlucoTwin/presentations_and_architecture/).
- [x] **Presentation (PDF/PPT):** Available and linked directly in [`presentations_and_architecture/`](GlucoTwin/presentations_and_architecture/).
- [x] **Public Accessibility:** All repository code, presentations, PDFs, and links are configured for public evaluation access without permission barriers.
