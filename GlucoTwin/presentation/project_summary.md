# GlucoTwin — Executive Project Summary

## Executive Summary

**GlucoTwin** demonstrates a novel paradigm in proactive metabolic healthcare: combining static Electronic Health Record (EHR) profiles with continuous wearable time-series streams into a stateful **Digital Twin** to deliver **early predictions of significant glucose spikes (≥ 40 mg/dL increase)** within a **2-hour prediction horizon**.

---

## Key Achievements

1. **Synthetic Data Pipeline**:
   * Synthetic EHR profiles for 50 patients (Age, BMI, HbA1c, Diabetes Status, Medication).
   * 67,200 continuous 15-minute wearable sensor readings (Glucose, HR, HRV, Steps, Sleep, Carbohydrates).
   * Realistic physiological coupling (digestion dynamics, circadian rhythms, exercise clearance).

2. **Feature Engineering & Leakage Prevention**:
   * 35+ engineered features including rolling averages (1h, 2h, 4h), short-term trends, variability, sleep deficits, and meal proximity.
   * Zero data leakage: future glucose strictly used for target definition (`target_spike`).

3. **Machine Learning Model Benchmarks**:
   * Evaluated **Logistic Regression**, **Random Forest**, and **XGBoost**.
   * Selected **XGBoost** as the champion model (**ROC-AUC: 0.8716**, **Recall: 87.8%**, **PR-AUC: 0.5053**).

4. **Digital Twin Engine & Explainability**:
   * Complete `DigitalTwin` Python class with state tracking, sequential sensor updates (`update_sensor_data`), SHAP feature attribution (`explain_prediction`), and what-if scenario simulation (`simulate`).

5. **Interactive Clinician Dashboard**:
   * Built using React, Vite, and Recharts.
   * Features interactive signal charts, risk gauge, SHAP driver breakdown, What-if sliders, event timeline, and live sequential sensor streaming.

---

## Machine Learning Performance Summary

| Model | Precision | Recall | F1 Score | ROC-AUC | PR-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 0.2675 | 0.8380 | 0.4049 | 0.8324 | 0.4145 |
| **Random Forest** | 0.2810 | 0.8522 | 0.4226 | 0.8594 | 0.4748 |
| **XGBoost (Champion)** | **0.2831** | **0.8782** | **0.4272** | **0.8716** | **0.5053** |

---

## Clinical Workflow & What-If Simulation

The Digital Twin enables clinicians to ask hypothetical "What-If" questions:
* *What if the patient reduces meal carbs from 90g to 45g?*
* *What if the patient takes a 15-minute walk (1,500 steps) post-meal?*

The system recalculates the Digital Twin state, runs the underlying ML model, and displays side-by-side risk deltas in real-time.

---

## Disclaimer

> **Research Proof-of-Concept:** GlucoTwin is intended solely for research, academic, and demonstration purposes. Not for medical diagnosis or clinical treatment.
