# AQUANTIS: Application Evidence & Screenshot Guide

This guide provides a structured checklist for capturing screenshots of the live AQUANTIS Streamlit application (`http://localhost:8501`) and describes exactly where each visual evidence figure belongs in presentations, demonstrations, or project submissions.

---

## 1. How to Launch the Application for Evidence Capture

In your project directory terminal (`AQUANTIS_r`):

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

Open your browser to: `http://localhost:8501`

---

## 2. Screenshot Checklist & Section Mapping

### Screenshot 1: Executive Telemetry & Landing Dashboard
* **Application Tab:** `Overview`
* **Elements to Capture:**
  * Top branding banner: `💧 AQUANTIS · WATER INTELLIGENCE PLATFORM` with green pulse indicator and tagline *"Intelligence for Every Drop."*
  * 5 KPI Metric Cards: `Dataset Records (3,276)`, `Input Indicators (9)`, `Trained Models (4)`, `Top Model (F1) (Support Vector Machine)`, `Peak ROC-AUC (0.660)`.
  * Grouped horizontal benchmark chart comparing Accuracy vs. F1-Score across all 4 models.
  * Potability label balance distribution chart.
* **Report Placement:** Section 17 (*Streamlit Application Architecture & User Interface*) – Figure 7.

---

### Screenshot 2: Water Sample Analysis Workspace
* **Application Tab:** `Analyze Sample`
* **Elements to Capture:**
  * 3-column categorized input parameter layout:
    * *Acidity & Disinfection:* pH, Chloramines, Trihalomethanes
    * *Mineral & Carbon Content:* Hardness, Sulfate, Organic Carbon
    * *Physical & Clarity Metrics:* Conductivity, Turbidity, Solids
  * Model Selection Dropdown: (e.g., `Random Forest` or `Support Vector Machine`).
  * Click **"⚡ Analyze Sample"** to generate the diagnostic output card.
  * Diagnostic Result Card: `💧 POTABLE` or `⚠️ NON-POTABLE` badge, model confidence percentage, and horizontal probability distribution bar chart.
* **Report Placement:** Section 17 (*Streamlit Application Architecture & User Interface*) – Figure 8.

---

### Screenshot 3: Model Diagnostics Laboratory
* **Application Tab:** `Model Lab`
* **Elements to Capture:**
  * Leaderboard cards highlighting top Accuracy, F1-Score, and ROC-AUC.
  * Benchmark leaderboard table formatted with highlighted maximum scores.
  * Side-by-side interactive confusion matrix heatmap and metric comparison chart.
  * Multi-model ROC curves plotting all four classifiers against the random baseline.
  * Expandable Scikit-Learn classification report code block.
* **Report Placement:** Section 18 (*Confusion Matrix and ROC Curve Analysis*) – Figure 9.

---

### Screenshot 4: Exploratory Dataset Analysis Workspace
* **Application Tab:** `Data Explorer`
* **Elements to Capture:**
  * Dataset telemetry metrics: Total Records (3,276), Total Features (9), Missing Value Cells (1,434).
  * Feature selector dropdown (e.g., `ph` or `Sulfate`).
  * Kernel density distribution chart showing class overlap.
  * Missing observations summary bar chart.
  * Expandable Pearson correlation matrix heatmap and dataset preview table.
* **Report Placement:** Section 9 (*Exploratory Data Analysis*) – Figure 10.

---

### Screenshot 5: Session Prediction Audit Log
* **Application Tab:** `Prediction History`
* **Elements to Capture:**
  * Summary metrics: Total Session Predictions, Potable vs. Non-Potable Classified count, Most Recent Sample telemetry card.
  * Tabular history audit log displaying Timestamp, Model used, Predicted Classification, Probability, and all 9 recorded input values.
  * **"📥 Export History as CSV"** and **"🗑️ Clear Session History"** action buttons.
* **Report Placement:** Section 17 (*Streamlit Application Architecture & User Interface*) – Figure 11.

---

## 3. Important Academic Verification & Defense Reminders

* **Empirical Fidelity:** All four models execute on real test partitions (N = 656 held-out samples). Never claim an accuracy of 99% or 100%—real-world environmental data has inherent noise and class overlap.
* **Safety Boundaries:** If asked during viva: *"Does this application certify drinking water?"*
  * **Answer:** *"No, sir/ma'am. AQUANTIS is an educational and decision-support prototype. Machine learning classifies statistical patterns within historical benchmark datasets. Real-world potability certification legally requires certified biological and chemical laboratory assays (e.g., EPA/WHO bacteriological testing) which cannot be replaced by algorithmic estimates alone."*
