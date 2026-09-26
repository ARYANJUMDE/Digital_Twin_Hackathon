# 🧬 GlucoTwin — Healthcare Digital Twin for Glucose Spike Prediction
---

## 🎯 Problem Statement & Healthcare Use Case

Managing blood glucose variability is a critical challenge for individuals with pre-diabetes, Type 1, and Type 2 diabetes. Unpredicted postprandial glucose spikes lead to long-term vascular complications, fatigue, and glycemic instability.

Standard machine learning approaches predict static risk from isolated readings. **GlucoTwin** introduces a stateful **Healthcare Digital Twin** paradigm that combines static Electronic Health Record (EHR) profiles with dynamic 15-minute wearable sensor streams (Continuous Glucose Monitors, Smartwatches) to predict whether a patient will experience a **significant glucose spike (≥ 40 mg/dL increase)** in the next **2 hours**.

---

## 🧬 Digital Twin Concept

A **Digital Twin** is a dynamic, continuously updated virtual representation of a physical entity. In GlucoTwin, the twin maintains:

```text
Patient Static Profile (EHR)
           +
Dynamic Wearable Sensor Stream (15-min ticks)
           ↓
Updated Digital Twin State (Trends, Rolling Averages, Sleep Deficits)
           ↓
Real-Time ML Prediction & SHAP Explanation
           ↓
Interactive Clinician Dashboard & What-If Simulation
```

The Digital Twin updates its state every time a new sensor reading arrives, enabling proactive interventions before hyperglycemia occurs.

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
├── src/
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
├── dashboard/
│   ├── app.py
│   └── components/
│       ├── patient_view.py
│       ├── twin_view.py
│       ├── charts.py
│       ├── prediction_view.py
│       ├── explainer_view.py
│       ├── simulation_view.py
│       └── timeline.py
├── notebooks/
│   └── exploratory_analysis.ipynb
├── tests/
│   ├── test_data.py
│   ├── test_features.py
│   ├── test_models.py
│   └── test_twin.py
├── architecture/
│   └── system_architecture.md
└── presentation/
    └── project_summary.md
```

---

## 📊 Data Pipeline & Synthetic Data Disclaimer

To ensure 100% reproducibility without privacy risks, GlucoTwin uses a realistic synthetic data pipeline. **No real patient PII is used.**

### 1. Static EHR Data (per patient)
* `patient_id`, `age`, `sex`, `bmi`, `hba1c`, `diabetes_status`, `hypertension`, `cholesterol`, `medication`, `diabetes_duration_years`, `family_risk_score`.

### 2. Dynamic Wearable Data (15-minute resolution)
* `timestamp`, `glucose`, `heart_rate`, `hrv`, `steps`, `sleep_hours`, `activity_level`, `meal_carbs`, `meal_type`.

### Realistic Physiological Coupling
* Digestive delays (carbohydrate absorption over 30–90 minutes).
* Basal drift influenced by HbA1c and BMI.
* Exercise glucose clearance (steps reduce glucose).
* Sleep deficit (increases insulin resistance and glucose baseline).
* Stress effects on HRV and heart rate.

---

## ⚡ Target Definition & Feature Engineering

### Prediction Task
Predict if:
$$\text{max}(\text{future glucose in next 2h}) - \text{current glucose} \ge 40 \text{ mg/dL}$$

### Zero Data-Leakage Guard
Future glucose readings (\(t + 15\text{m}\) through \(t + 2\text{h}\)) are strictly restricted to target generation (`target_spike`) and completely omitted from input features!

### Input Features (35+ engineered variables)
* **Vitals & Trends:** `glucose`, `glucose_trend_15m`, `glucose_trend_30m`, `glucose_trend_60m`, `glucose_mean_1h`, `glucose_mean_2h`, `glucose_std_2h`, `glucose_min_2h`, `glucose_max_2h`.
* **Autonomic & Heart:** `heart_rate`, `heart_rate_mean_1h`, `hrv`, `hrv_mean_1h`, `hrv_change_1h`.
* **Lifestyle & Sleep:** `steps`, `recent_steps_1h`, `recent_steps_2h`, `sleep_hours`, `sleep_deficit`.
* **Nutrition:** `meal_carbs`, `meal_carbs_last_1h`, `meal_carbs_last_2h`, `time_since_last_meal`.
* **Clinical Profile:** `age`, `bmi`, `hba1c`, `hypertension`, `diabetes_duration_years`, `family_risk_score`, and one-hot encoded statuses.

---

## 🤖 Machine Learning Benchmark

Three candidate classification models were implemented and evaluated on a holdout test set:

| Model | Precision | Recall | F1 Score | ROC-AUC | PR-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 0.2675 | 0.8380 | 0.4049 | 0.8324 | 0.4145 |
| **Random Forest** | 0.2810 | 0.8522 | 0.4226 | 0.8594 | 0.4748 |
| **XGBoost (Champion)** | **0.2831** | **0.8782** | **0.4272** | **0.8716** | **0.5053** |

*The best model (**XGBoost**) and StandardScaler preprocessor are saved to `models/`.*

---

## 🔍 SHAP Explainability

Using **SHAP (SHapley Additive exPlanations)**, GlucoTwin explains *why* a specific prediction was made by computing exact feature attributions:

```text
Current Glucose (165 mg/dL)    ↑ (+0.84 SHAP)
Meal Carbs 1h (80g)            ↑ (+0.62 SHAP)
Glucose Trend 30m (+15 mg/dL)  ↑ (+0.41 SHAP)
Sleep Deficit (3.0 hrs)        ↑ (+0.25 SHAP)
Recent Steps 1h (1,800 steps)  ↓ (-0.32 SHAP)
```

---

## 🧪 What-If Scenario Simulation

Clinicians and patients can simulate prospective interventions interactively:
1. Adjust sliders for **Glucose**, **Meal Carbs**, **Sleep**, **Steps**, **Heart Rate**, or **HRV**.
2. Click **SIMULATE**.
3. GlucoTwin creates a clone of the digital twin, updates its physiological state, recalculates features, and re-evaluates the ML model.
4. Outputs real-time side-by-side risk metric deltas:

```text
Current Risk: 28.1% (LOW)
Simulated Risk: 76.4% (HIGH)
Risk Delta: +48.3 percentage points
```

---

## 🖥️ Clinician Dashboard

Built with **Streamlit** and **Plotly**, featuring 6 interactive tabs:
1. **Twin Dashboard**: Patient EHR metrics, Digital Twin state gauges, Risk banner.
2. **Time Series Signals**: Interactive Plotly multi-sensor streams.
3. **Spike Prediction & SHAP**: Risk probability dial + SHAP waterfall chart.
4. **What-If Simulation**: Parameter controls + side-by-side risk comparison.
5. **Patient Timeline**: Chronological clinical events (meals, exercise, alerts).
6. **ML Model Benchmarks**: Comparative metrics table & confusion matrices.

---

## ⚙️ Installation & Running

### Prerequisites
* Python 3.10+
* pip

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/your-username/GlucoTwin.git
cd GlucoTwin
pip install -r requirements.txt
```

### 2. Run Data & ML Pipelines
```bash
# Generate synthetic EHR and wearable datasets
python -m src.data.generate_synthetic

# Build features and preprocess data
python -m src.data.process

# Train and evaluate candidate ML models
python -m src.models.train
```

### 3. Launch Streamlit Dashboard
```bash
streamlit run dashboard/app.py
```

### 4. Run Unit Tests
```bash
pytest
```

---
