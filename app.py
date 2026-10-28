import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, roc_auc_score
from src.aquantis import load_data, train_and_evaluate, FEATURES, TARGET

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="AQUANTIS | Water Intelligence Platform",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# Theme & Premium Styling (Midnight Navy & Rich Teal Design System)
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-base: #060d17;
    --bg-surface: #0c1827;
    --bg-card: #112238;
    --bg-card-hover: #162b45;
    --border-subtle: #1c3554;
    --border-accent: rgba(14, 212, 190, 0.35);
    --teal-primary: #0ed4be;
    --teal-glow: rgba(14, 212, 190, 0.15);
    --teal-dark: #098a7b;
    --cyan-accent: #38bdf8;
    --text-primary: #f1f7fc;
    --text-secondary: #94a9c4;
    --text-muted: #5e7694;
    --danger: #f87171;
    --success: #34d399;
}

/* Global resets & typography */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background-color: var(--bg-base);
    background-image: 
        radial-gradient(circle at 15% 0%, rgba(14, 212, 190, 0.08) 0%, transparent 35%),
        radial-gradient(circle at 85% 5%, rgba(56, 189, 248, 0.06) 0%, transparent 30%),
        radial-gradient(circle at 50% 100%, rgba(12, 24, 39, 0.8) 0%, transparent 60%);
    color: var(--text-primary);
}

.block-container {
    max-width: 1360px;
    padding-top: 5rem !important;
    padding-bottom: 3.5rem;
}

/* Header bar styling */
header[data-testid="stHeader"] {
    background: rgba(6, 13, 23, 0.85);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border-subtle);
}

/* Header Hero Banner */
.aq-header {
    background: linear-gradient(135deg, #091728 0%, #0d233c 45%, #083d47 100%);
    border: 1px solid var(--border-subtle);
    border-top: 1px solid rgba(14, 212, 190, 0.4);
    border-radius: 18px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.25rem;
    position: relative;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), 0 0 25px var(--teal-glow);
}

.aq-header-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.8rem;
    margin-bottom: 0.5rem;
}

.aq-brand-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    background: rgba(14, 212, 190, 0.12);
    border: 1px solid rgba(14, 212, 190, 0.3);
    border-radius: 9999px;
    padding: 0.28rem 0.85rem;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    font-weight: 700;
    color: var(--teal-primary);
    text-transform: uppercase;
}

.aq-status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.76rem;
    color: var(--text-secondary);
    background: rgba(28, 53, 84, 0.4);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 0.25rem 0.65rem;
}

.aq-status-dot {
    width: 7px;
    height: 7px;
    background: var(--teal-primary);
    border-radius: 50%;
    box-shadow: 0 0 8px var(--teal-primary);
}

.aq-title {
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: -0.035em;
    margin: 0;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.aq-title span {
    background: linear-gradient(135deg, #ffffff 40%, var(--teal-primary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.aq-tagline {
    font-size: 0.96rem;
    font-weight: 600;
    color: var(--cyan-accent);
    margin-top: 0.2rem;
    letter-spacing: -0.01em;
}

.aq-desc {
    font-size: 0.88rem;
    color: var(--text-secondary);
    margin-top: 0.35rem;
    max-width: 820px;
    line-height: 1.45;
}

/* Card wrappers */
.aq-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    padding: 1.3rem 1.4rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}

.aq-card-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.25rem;
}

.aq-card-subtitle {
    font-size: 0.82rem;
    color: var(--text-secondary);
    margin-bottom: 1rem;
}

/* Section Header Typography */
.section-header {
    margin-top: 0.4rem;
    margin-bottom: 1.1rem;
}

.section-title {
    font-size: 1.42rem;
    font-weight: 800;
    letter-spacing: -0.025em;
    color: #ffffff;
    margin: 0 0 0.2rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.section-sub {
    font-size: 0.88rem;
    color: var(--text-secondary);
    margin: 0;
}

/* Metrics Styling */
div[data-testid="stMetric"] {
    background: linear-gradient(180deg, #0d1e32 0%, #0a1727 100%) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 14px !important;
    padding: 1rem 1.15rem !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25) !important;
    transition: transform 0.2s ease, border-color 0.2s ease;
}

div[data-testid="stMetric"]:hover {
    border-color: var(--border-accent) !important;
    transform: translateY(-2px);
}

div[data-testid="stMetricLabel"] p {
    color: var(--text-secondary) !important;
    font-size: 0.74rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    margin-bottom: 0.2rem !important;
}

div[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1.65rem !important;
}

/* Tab Navigation Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.4rem;
    background: #091524;
    border: 1px solid var(--border-subtle);
    padding: 0.4rem 0.5rem;
    border-radius: 12px;
    margin-bottom: 1.4rem;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 0.55rem 1.1rem;
    color: var(--text-secondary);
    font-weight: 600;
    font-size: 0.88rem;
    transition: all 0.2s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-primary);
    background: rgba(28, 53, 84, 0.4);
}

.stTabs [aria-selected="true"] {
    color: #ffffff !important;
    background: linear-gradient(135deg, rgba(14, 212, 190, 0.2) 0%, rgba(12, 36, 56, 0.9) 100%) !important;
    border: 1px solid rgba(14, 212, 190, 0.5) !important;
    box-shadow: 0 2px 10px rgba(14, 212, 190, 0.15) !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    display: none;
}

/* Form and Inputs */
label[data-testid="stWidgetLabel"] p {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: -0.01em !important;
}

div[data-baseweb="input"], div[data-baseweb="select"] {
    background-color: #0b192b !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    transition: all 0.2s ease;
}

div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within {
    border-color: var(--teal-primary) !important;
    box-shadow: 0 0 0 1px var(--teal-primary), 0 0 12px var(--teal-glow) !important;
}

input[type="number"], input[type="text"] {
    color: #ffffff !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}

/* Select dropdown text */
div[data-baseweb="select"] span {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
}

/* Buttons */
.stButton>button, .stFormSubmitButton>button {
    background: linear-gradient(135deg, #0ed4be 0%, #089785 100%) !important;
    color: #04121a !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.01em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.4rem !important;
    box-shadow: 0 4px 15px rgba(14, 212, 190, 0.25) !important;
    transition: all 0.2s ease !important;
}

.stButton>button:hover, .stFormSubmitButton>button:hover {
    background: linear-gradient(135deg, #2ae0cb 0%, #0aa390 100%) !important;
    box-shadow: 0 6px 20px rgba(14, 212, 190, 0.4) !important;
    transform: translateY(-1px);
    color: #02090e !important;
}

/* Secondary Button styling */
button[kind="secondary"] {
    background: #0d1e32 !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-subtle) !important;
    box-shadow: none !important;
}
button[kind="secondary"]:hover {
    background: #132a45 !important;
    border-color: var(--border-accent) !important;
    color: #ffffff !important;
}

/* Download buttons */
.stDownloadButton>button {
    background: #0c1c2e !important;
    color: var(--teal-primary) !important;
    border: 1px solid rgba(14, 212, 190, 0.3) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
    padding: 0.45rem 1rem !important;
    transition: all 0.2s ease !important;
}

.stDownloadButton>button:hover {
    background: rgba(14, 212, 190, 0.12) !important;
    border-color: var(--teal-primary) !important;
    color: #ffffff !important;
}

/* Expanders */
div[data-testid="stExpander"] {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    margin-bottom: 0.8rem !important;
}

div[data-testid="stExpander"] summary {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
}

div[data-testid="stExpander"] summary:hover {
    color: var(--teal-primary) !important;
}

/* Alert callouts */
div[data-testid="stAlert"] {
    background: rgba(12, 28, 48, 0.7) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

/* Code block */
div[data-testid="stCodeBlock"] {
    background: #08121f !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
}

/* Prediction Output Badge */
.potable-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(52, 211, 153, 0.15);
    border: 1px solid rgba(52, 211, 153, 0.4);
    color: #6ee7b7;
    padding: 0.4rem 1rem;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 1.05rem;
}

.non-potable-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(248, 113, 113, 0.15);
    border: 1px solid rgba(248, 113, 113, 0.4);
    color: #fca5a5;
    padding: 0.4rem 1rem;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 1.05rem;
}

/* Footer */
.aq-footer {
    border-top: 1px solid var(--border-subtle);
    padding: 1.8rem 0 1rem 0;
    margin-top: 3rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
    color: var(--text-muted);
    font-size: 0.8rem;
}

.aq-footer a {
    color: var(--teal-primary);
    text-decoration: none;
}

.aq-disclaimer-card {
    background: rgba(14, 212, 190, 0.04);
    border: 1px solid rgba(14, 212, 190, 0.18);
    border-left: 3px solid var(--teal-primary);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-top: 0.8rem;
    font-size: 0.82rem;
    color: var(--text-secondary);
    line-height: 1.45;
}
</style>

<div class="aq-header">
  <div class="aq-header-top">
    <div class="aq-brand-badge">💧 AQUANTIS · WATER INTELLIGENCE PLATFORM</div>
    <div class="aq-status-indicator"><span class="aq-status-dot"></span> ML Inference Engine Active</div>
  </div>
  <div class="aq-title"><span>AQUANTIS</span></div>
  <div class="aq-tagline">Intelligence for Every Drop.</div>
  <div class="aq-desc">Advanced machine learning system evaluating chemical, physical, and biological water quality indicators to predict potability metrics across four validated predictive architectures.</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Data & Model Pipeline with Streamlit Caching
# ---------------------------------------------------------
@st.cache_data
def get_data():
    return load_data()

@st.cache_resource
def get_models():
    return train_and_evaluate(get_data())

try:
    df = get_data()
except Exception as e:
    st.error(f"Error loading water potability dataset: {e}")
    st.stop()

# ---------------------------------------------------------
# Matplotlib & Seaborn Chart Styling Configuration
# ---------------------------------------------------------
sns.set_theme(style="white", rc={
    "axes.facecolor": "#0d1b2a",
    "figure.facecolor": "#0d1b2a",
    "axes.edgecolor": "#1c3554",
    "grid.color": "#152a42",
    "axes.labelcolor": "#94a9c4",
    "xtick.color": "#94a9c4",
    "ytick.color": "#94a9c4",
    "text.color": "#f1f7fc",
    "font.family": "sans-serif"
})

def style_chart(fig, ax, grid=True):
    fig.patch.set_facecolor("#0d1b2a")
    ax.set_facecolor("#0d1b2a")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#1c3554")
    ax.spines["bottom"].set_color("#1c3554")
    ax.spines["left"].set_linewidth(1.0)
    ax.spines["bottom"].set_linewidth(1.0)
    if grid:
        ax.grid(True, linestyle="--", alpha=0.35, color="#1c3554")
    else:
        ax.grid(False)
    ax.title.set_fontweight("bold")
    ax.title.set_color("#ffffff")
    fig.tight_layout(pad=1.4)
    return fig

# ---------------------------------------------------------
# Tabs Navigation
# ---------------------------------------------------------
tabs = st.tabs([
    "Overview",
    "Analyze Sample",
    "Model Lab",
    "Data Explorer",
    "Prediction History"
])

# =========================================================
# TAB 1: OVERVIEW
# =========================================================
with tabs[0]:
    st.markdown("""
    <div class="section-header">
        <div class="section-title">📊 Executive Water Intelligence Overview</div>
        <div class="section-sub">High-level architecture, dataset volume, and benchmark performance across four machine learning classifiers.</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.spinner("Analyzing model evaluation benchmarks..."):
        results, models, details, split = get_models()
    
    best_model_row = results.iloc[0]
    best_model_name = str(best_model_row["Model"])
    best_f1 = float(best_model_row["F1-score"])
    best_roc_auc = float(results["ROC-AUC"].max())
    total_missing = int(df[FEATURES].isna().sum().sum())
    
    # KPI Metric Cards
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("Dataset Records", f"{len(df):,}", help="Total curated water samples in dataset")
    with m2:
        st.metric("Input Indicators", f"{len(FEATURES)}", help="Chemical, physical, and mineral parameters")
    with m3:
        st.metric("Trained Models", f"{len(models)}", help="Classifiers in the ensemble benchmark")
    with m4:
        st.metric("Top Model (F1)", best_model_name.replace(" Classifier", ""), help=f"Highest F1 score on hold-out set ({best_f1:.3f})")
    with m5:
        st.metric("Peak ROC-AUC", f"{best_roc_auc:.3f}", help="Maximum area under the ROC curve observed")
    
    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.1, 0.9])
    
    with col_left:
        st.markdown("""
        <div class="aq-card">
            <div class="aq-card-title">⚡ Benchmark Model Performance (Hold-Out Test Set)</div>
            <div class="aq-card-subtitle">Direct comparison across 20% stratified test split. Measured results from pipeline.</div>
        </div>
        """, unsafe_allow_html=True)
        
        fig, ax = plt.subplots(figsize=(7.0, 3.6))
        sorted_results = results.sort_values("F1-score", ascending=True)
        models_list = sorted_results["Model"].tolist()
        acc_scores = sorted_results["Accuracy"].tolist()
        f1_scores = sorted_results["F1-score"].tolist()
        
        y_pos = np.arange(len(models_list))
        bar_height = 0.36
        
        # Coordinated dark-navy & futuristic teal/cyan color pairing
        bars_acc = ax.barh(y_pos - bar_height/2, acc_scores, height=bar_height, color="#38bdf8", label="Accuracy", edgecolor="#060d17", linewidth=0.8, alpha=0.92)
        bars_f1 = ax.barh(y_pos + bar_height/2, f1_scores, height=bar_height, color="#0ed4be", label="F1-score", edgecolor="#060d17", linewidth=0.8, alpha=0.92)
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(models_list, fontsize=9.5, fontweight="600", color="#f1f7fc")
        ax.set_xlim(0, 1.0)
        ax.set_xlabel("Score (0.0 – 1.0)", fontsize=8.5, color="#94a9c4")
        ax.legend(loc="lower right", facecolor="#0c1827", edgecolor="#1c3554", fontsize=8.5, labelcolor="#f1f7fc")
        
        # Add concise value labels to bars
        for bar in bars_acc:
            w = bar.get_width()
            ax.text(w + 0.015, bar.get_y() + bar.get_height()/2, f"{w:.3f}", 
                    va='center', ha='left', color="#94a9c4", fontsize=7.8, fontweight="600")
        for bar in bars_f1:
            w = bar.get_width()
            ax.text(w + 0.015, bar.get_y() + bar.get_height()/2, f"{w:.3f}", 
                    va='center', ha='left', color="#ffffff", fontsize=7.8, fontweight="700")
        
        st.pyplot(style_chart(fig, ax), clear_figure=True)
    
    with col_right:
        st.markdown("""
        <div class="aq-card">
            <div class="aq-card-title">🎯 Potability Class Distribution</div>
            <div class="aq-card-subtitle">Balance between potable (safe) and non-potable samples in source data.</div>
        </div>
        """, unsafe_allow_html=True)
        
        counts = df[TARGET].value_counts().reindex([0, 1], fill_value=0)
        pcts = [counts[0]/len(df)*100, counts[1]/len(df)*100]
        
        fig, ax = plt.subplots(figsize=(5.8, 3.4))
        categories = ["Non-Potable (0)", "Potable (1)"]
        colors = ["#475569", "#0ed4be"]
        bars = ax.bar(categories, counts.values, color=colors, width=0.48, edgecolor=["#64748b", "#2ae0cb"], linewidth=1.2)
        ax.set_ylim(0, max(counts.values) * 1.25)
        ax.set_ylabel("Sample Count", fontsize=8.5, color="#94a9c4")
        
        for i, bar in enumerate(bars):
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 35, f"{int(h):,} ({pcts[i]:.1f}%)",
                    ha='center', va='bottom', color="#ffffff", fontsize=9, fontweight="700")
            
        st.pyplot(style_chart(fig, ax), clear_figure=True)
        
    st.markdown("""
    <div class="aq-disclaimer-card">
        <strong>Workflow & Pipeline Notice:</strong> Data undergoes median imputation and standard scaling inside isolated scikit-learn Pipelines to avoid data leakage. The classification outputs are derived from empirical patterns in the Kaggle Water Potability dataset. This educational prototype does not constitute physical certification or EPA standard validation.
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# TAB 2: ANALYZE SAMPLE
# =========================================================
with tabs[1]:
    st.markdown("""
    <div class="section-header">
        <div class="section-title">🧪 Water Quality Sample Analysis Workspace</div>
        <div class="section-sub">Configure water quality measurements across chemical, physical, and mineral categories to generate an instant prediction.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature configurations with verified domains, units, and medians
    feature_config = {
        "ph": {
            "group": "Chemical", "label": "pH Level", "unit": "pH (0–14)",
            "help": "Acidity or alkalinity measure (WHO recommended potable range: 6.5–8.5)",
            "default": 7.0, "step": 0.1, "format": "%.2f"
        },
        "Hardness": {
            "group": "Chemical", "label": "Hardness", "unit": "mg/L",
            "help": "Capacity of water to precipitate soap; caused primarily by Calcium and Magnesium salts",
            "default": 196.0, "step": 1.0, "format": "%.1f"
        },
        "Chloramines": {
            "group": "Chemical", "label": "Chloramines", "unit": "ppm / mg/L",
            "help": "Major disinfectants formed when ammonia is added to chlorine (EPA limit: up to 4 mg/L)",
            "default": 7.1, "step": 0.1, "format": "%.2f"
        },
        "Sulfate": {
            "group": "Chemical", "label": "Sulfate", "unit": "mg/L",
            "help": "Naturally occurring mineral salts dissolved from minerals (typically < 250 mg/L in freshwater)",
            "default": 333.0, "step": 1.0, "format": "%.1f"
        },
        "Organic_carbon": {
            "group": "Chemical", "label": "Total Organic Carbon (TOC)", "unit": "ppm / mg/L",
            "help": "Measure of total organic matter in water (EPA drinking standard typically < 2 mg/L)",
            "default": 14.2, "step": 0.1, "format": "%.2f"
        },
        "Trihalomethanes": {
            "group": "Chemical", "label": "Trihalomethanes (THMs)", "unit": "µg/L",
            "help": "Byproducts of chlorine disinfection; regulated by EPA due to carcinogenic risk (< 80 µg/L)",
            "default": 66.4, "step": 0.5, "format": "%.1f"
        },
        "Conductivity": {
            "group": "Physical", "label": "Electrical Conductivity", "unit": "µS/cm",
            "help": "Water's electrical conductivity indicating dissolved mineral ion concentration (WHO < 400 µS/cm)",
            "default": 425.0, "step": 2.0, "format": "%.1f"
        },
        "Turbidity": {
            "group": "Physical", "label": "Turbidity", "unit": "NTU",
            "help": "Measure of water clarity and suspended particulate matter (WHO target: < 5.0 NTU)",
            "default": 3.95, "step": 0.05, "format": "%.2f"
        },
        "Solids": {
            "group": "Physical", "label": "Total Dissolved Solids (TDS)", "unit": "ppm / mg/L",
            "help": "Total mineral, salt, and organic solids dissolved in water (desirable < 500 ppm)",
            "default": 22000.0, "step": 100.0, "format": "%.0f"
        }
    }
    
    with st.form("water_sample_form"):
        st.markdown("<h4 style='color:#f1f7fc; margin-bottom:0.8rem; font-size:1rem;'>Sample Indicator Inputs</h4>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        input_values = {}
        
        # Categorized 3-column layout
        with col1:
            st.markdown("<div style='color:#0ed4be; font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem;'>🧪 Acidity & Disinfection</div>", unsafe_allow_html=True)
            for feat in ["ph", "Chloramines", "Trihalomethanes"]:
                cfg = feature_config[feat]
                series = pd.to_numeric(df[feat], errors="coerce").dropna()
                lo = float(series.min())
                hi = float(series.max())
                val = float(min(max(cfg["default"], lo), hi))
                input_values[feat] = st.number_input(
                    f"{cfg['label']} ({cfg['unit']})",
                    min_value=lo,
                    max_value=hi,
                    value=val,
                    step=cfg["step"],
                    format=cfg["format"],
                    help=f"{cfg['help']} | Obs. Range: {lo:.1f} – {hi:.1f}"
                )
                
        with col2:
            st.markdown("<div style='color:#38bdf8; font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem;'>🔬 Mineral & Carbon Content</div>", unsafe_allow_html=True)
            for feat in ["Hardness", "Sulfate", "Organic_carbon"]:
                cfg = feature_config[feat]
                series = pd.to_numeric(df[feat], errors="coerce").dropna()
                lo = float(series.min())
                hi = float(series.max())
                val = float(min(max(cfg["default"], lo), hi))
                input_values[feat] = st.number_input(
                    f"{cfg['label']} ({cfg['unit']})",
                    min_value=lo,
                    max_value=hi,
                    value=val,
                    step=cfg["step"],
                    format=cfg["format"],
                    help=f"{cfg['help']} | Obs. Range: {lo:.1f} – {hi:.1f}"
                )
                
        with col3:
            st.markdown("<div style='color:#a78bfa; font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem;'>🌊 Physical & Clarity Metrics</div>", unsafe_allow_html=True)
            for feat in ["Conductivity", "Turbidity", "Solids"]:
                cfg = feature_config[feat]
                series = pd.to_numeric(df[feat], errors="coerce").dropna()
                lo = float(series.min())
                hi = float(series.max())
                val = float(min(max(cfg["default"], lo), hi))
                input_values[feat] = st.number_input(
                    f"{cfg['label']} ({cfg['unit']})",
                    min_value=lo,
                    max_value=hi,
                    value=val,
                    step=cfg["step"],
                    format=cfg["format"],
                    help=f"{cfg['help']} | Obs. Range: {lo:.1f} – {hi:.1f}"
                )
        
        st.markdown("<div style='height: 0.6rem;'></div>", unsafe_allow_html=True)
        col_m_select, col_submit = st.columns([2, 1])
        with col_m_select:
            model_options = ["Random Forest", "Support Vector Machine", "Logistic Regression", "K-Nearest Neighbors"]
            selected_model = st.selectbox(
                "Inference Model",
                options=model_options,
                index=0,
                help="Select which pre-trained classifier pipeline to execute for this sample"
            )
        with col_submit:
            st.markdown("<div style='height: 1.7rem;'></div>", unsafe_allow_html=True)
            submit_btn = st.form_submit_button("⚡ Analyze Sample", type="primary", use_container_width=True)

    if submit_btn:
        with st.spinner("Processing feature pipeline & executing inference..."):
            _, trained_models, _, _ = get_models()
            model_instance = trained_models[selected_model]
            sample_df = pd.DataFrame([input_values], columns=FEATURES)
            
            prediction = int(model_instance.predict(sample_df)[0])
            has_proba = hasattr(model_instance, "predict_proba")
            if has_proba:
                probabilities = model_instance.predict_proba(sample_df)[0]
                p0, p1 = float(probabilities[0]), float(probabilities[1])
                confidence = max(p0, p1)
            else:
                p0, p1 = (0.0, 1.0) if prediction == 1 else (1.0, 0.0)
                confidence = 1.0
                
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        st.markdown("### 📋 Prediction Diagnostic Result")
        
        res_col1, res_col2 = st.columns([1, 1.3])
        
        with res_col1:
            st.markdown("<div class='aq-card' style='height:100%;'>", unsafe_allow_html=True)
            if prediction == 1:
                st.markdown("""
                <div style='margin-bottom:0.8rem;'>
                    <span class='potable-badge'>💧 POTABLE (Safe for Drinking)</span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"**Selected Model:** `{selected_model}`")
                st.markdown(f"**Classification Confidence:** `{confidence:.1%}`")
                st.markdown(f"**Potability Probability:** `{p1:.1%}`")
                st.markdown("""
                <div style='color:#94a9c4; font-size:0.82rem; margin-top:0.6rem; border-top:1px solid #1c3554; padding-top:0.6rem;'>
                    Water parameters fall within statistical boundaries typical of potable water samples according to this model.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='margin-bottom:0.8rem;'>
                    <span class='non-potable-badge'>⚠️ NON-POTABLE (Unsafe / Requires Treatment)</span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"**Selected Model:** `{selected_model}`")
                st.markdown(f"**Classification Confidence:** `{confidence:.1%}`")
                st.markdown(f"**Potability Probability:** `{p1:.1%}`")
                st.markdown("""
                <div style='color:#94a9c4; font-size:0.82rem; margin-top:0.6rem; border-top:1px solid #1c3554; padding-top:0.6rem;'>
                    One or more indicators deviate from safe potability clusters. Treatment and filtration recommended.
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with res_col2:
            st.markdown("<div class='aq-card' style='height:100%;'>", unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(6.2, 2.5))
            labels = ["Non-Potable (0)", "Potable (1)"]
            vals = [p0, p1]
            bar_colors = ["#f87171" if prediction == 0 else "#475569", 
                          "#0ed4be" if prediction == 1 else "#164e63"]
            
            bars = ax.barh(labels, vals, color=bar_colors, height=0.45, edgecolor="#ffffff", linewidth=0.5)
            ax.set_xlim(0, 1.0)
            ax.set_xlabel("Predicted Probability", fontsize=8.5, color="#94a9c4")
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0%}"))
            
            for bar in bars:
                w = bar.get_width()
                ax.text(w + 0.02, bar.get_y() + bar.get_height()/2, f"{w:.1%}",
                        va='center', ha='left', color="#ffffff", fontsize=9, fontweight="bold")
                
            st.pyplot(style_chart(fig, ax), clear_figure=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Record into session state history
        if "history" not in st.session_state:
            st.session_state.history = []
            
        record = {
            "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Model": selected_model,
            "Predicted Label": "Potable" if prediction == 1 else "Non-Potable",
            "Probability": round(p1, 4),
            **input_values
        }
        st.session_state.history.insert(0, record)
        st.success("✅ Sample inference recorded in session history.")
        
        st.markdown("""
        <div class="aq-disclaimer-card" style="margin-top:0.8rem;">
            <strong>Important Prototype Disclaimer:</strong> This prediction is generated by a mathematical model trained on historical data. It does not replace comprehensive microbial, heavy metal, or certified EPA/WHO laboratory testing. Never consume untreated water based solely on automated prediction.
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# TAB 3: MODEL LAB
# =========================================================
with tabs[2]:
    st.markdown("""
    <div class="section-header">
        <div class="section-title">🔬 Machine Learning Model Laboratory & Diagnostics</div>
        <div class="section-sub">Comprehensive multi-model benchmarking, confusion matrices, ROC curves, and classification diagnostics.</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_rt, col_fill = st.columns([1.5, 4])
    with col_rt:
        if st.button("🔄 Retrain All Models", type="secondary", help="Clears cached pipelines and refits all four models on the dataset"):
            st.cache_resource.clear()
            st.rerun()
            
    with st.spinner("Compiling cross-model diagnostic results..."):
        results, models, details, (X_train, X_test, y_train, y_test) = get_models()
        
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    
    # Leaderboard Cards
    b_acc = results.loc[results['Accuracy'].idxmax()]
    b_f1 = results.loc[results['F1-score'].idxmax()]
    b_auc = results.loc[results['ROC-AUC'].idxmax()]
    
    lead1, lead2, lead3 = st.columns(3)
    lead1.metric("Highest F1-Score", f"{b_f1['Model']}", f"{b_f1['F1-score']:.3f} F1")
    lead2.metric("Highest Accuracy", f"{b_acc['Model']}", f"{b_acc['Accuracy']:.1%}")
    lead3.metric("Highest ROC-AUC", f"{b_auc['Model']}", f"{b_auc['ROC-AUC']:.3f} AUC")
    
    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    
    # Detailed Benchmark Dataframe
    st.markdown("#### 🏆 Benchmark Metrics Leaderboard")
    display_df = results.copy()
    numeric_cols = [c for c in display_df.columns if c != "Model"]
    
    formatted_df = display_df.style.format({c: "{:.4f}" for c in numeric_cols})\
        .highlight_max(subset=numeric_cols, color="#0b404d")
    st.dataframe(formatted_df, use_container_width=True, hide_index=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Charts: Multi-metric bar chart & Model Deep-dive
    chart_col1, chart_col2 = st.columns([1.1, 0.9])
    
    with chart_col1:
        st.markdown("#### 📊 Metric Comparison Across Architectures")
        metric_cols = ["Accuracy", "Precision", "Recall", "F1-score", "ROC-AUC"]
        plot_df = results.set_index("Model")[metric_cols]
        
        fig, ax = plt.subplots(figsize=(7.5, 4.4))
        colors = ["#38bdf8", "#0ed4be", "#f59e0b", "#a855f7", "#ec4899"]
        plot_df.plot(kind="bar", ax=ax, color=colors, width=0.75, edgecolor="#060d17", linewidth=0.8)
        ax.set_ylim(0, 1.0)
        ax.set_ylabel("Metric Score", fontsize=8.5, color="#94a9c4")
        ax.set_xlabel("")
        ax.tick_params(axis="x", rotation=0, labelsize=9)
        ax.legend(frameon=True, facecolor="#0c1827", edgecolor="#1c3554", ncol=3, loc="upper right", fontsize=8, labelcolor="#f1f7fc")
        st.pyplot(style_chart(fig, ax), clear_figure=True)
        
    with chart_col2:
        st.markdown("#### 🎯 Model Confusion Matrix")
        model_choice = st.selectbox("Inspect Classifier Details", list(details.keys()), index=0)
        cm = details[model_choice]["confusion_matrix"]
        
        fig, ax = plt.subplots(figsize=(5.4, 4.2))
        sns.heatmap(
            cm, annot=True, fmt="d", cmap=sns.color_palette(["#091829", "#0ed4be"], as_cmap=True),
            cbar=False, square=True,
            xticklabels=["Pred 0 (Non-Pot)", "Pred 1 (Potable)"],
            yticklabels=["True 0 (Non-Pot)", "True 1 (Potable)"],
            annot_kws={"size": 13, "weight": "bold", "color": "#ffffff"},
            linewidths=1.5, linecolor="#060d17",
            ax=ax
        )
        ax.set_xlabel("Predicted Class", fontsize=9, color="#94a9c4")
        ax.set_ylabel("True Class", fontsize=9, color="#94a9c4")
        st.pyplot(style_chart(fig, ax, grid=False), clear_figure=True)

    # ROC Curves & Classification Report
    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    roc_col, report_col = st.columns([1.1, 0.9])
    
    with roc_col:
        st.markdown("#### 📈 Multi-Model ROC Curves")
        fig, ax = plt.subplots(figsize=(7.2, 4.2))
        curve_colors = {
            "Random Forest": "#0ed4be",
            "Support Vector Machine": "#38bdf8",
            "Logistic Regression": "#f59e0b",
            "K-Nearest Neighbors": "#a855f7"
        }
        
        for name, detail in details.items():
            if detail["probabilities"] is not None:
                fpr, tpr, _ = roc_curve(detail["y_test"], detail["probabilities"])
                auc_val = roc_auc_score(detail["y_test"], detail["probabilities"])
                ax.plot(fpr, tpr, label=f"{name} (AUC = {auc_val:.3f})", 
                        color=curve_colors.get(name, "#0ed4be"), linewidth=2.0)
                
        ax.plot([0, 1], [0, 1], linestyle="--", color="#64748b", label="Random Classifier (0.500)", linewidth=1.2)
        ax.set_xlabel("False Positive Rate (1 - Specificity)", fontsize=8.5, color="#94a9c4")
        ax.set_ylabel("True Positive Rate (Sensitivity / Recall)", fontsize=8.5, color="#94a9c4")
        ax.legend(loc="lower right", facecolor="#0c1827", edgecolor="#1c3554", fontsize=8.5, labelcolor="#f1f7fc")
        st.pyplot(style_chart(fig, ax), clear_figure=True)
        
    with report_col:
        st.markdown("#### 📄 Detailed Classification Report")
        st.code(details[model_choice]["report"], language="text")
        st.download_button(
            "📥 Download Model Benchmark CSV",
            results.to_csv(index=False).encode("utf-8"),
            file_name="aquantis_model_comparison.csv",
            mime="text/csv",
            use_container_width=True
        )

# =========================================================
# TAB 4: DATA EXPLORER
# =========================================================
with tabs[3]:
    st.markdown("""
    <div class="section-header">
        <div class="section-title">🔍 Water Quality Dataset Exploration & Feature Analysis</div>
        <div class="section-sub">Inspect distributions, missing value incidence, and statistical correlations across all monitored parameters.</div>
    </div>
    """, unsafe_allow_html=True)
    
    e1, e2, e3, e4 = st.columns(4)
    with e1:
        st.metric("Total Records", f"{df.shape[0]:,}")
    with e2:
        st.metric("Total Features", f"{df.shape[1] - 1}")
    with e3:
        st.metric("Missing Value Cells", f"{int(df[FEATURES].isna().sum().sum()):,}")
    with e4:
        missing_feats = (df[FEATURES].isna().sum() > 0).sum()
        st.metric("Features with Missing Values", f"{missing_feats} of {len(FEATURES)}")
        
    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    
    # Missing Value Chart & Feature Selector
    col_feat, col_missing = st.columns([1.2, 0.8])
    
    with col_feat:
        st.markdown("#### 📊 Feature Density Distribution by Potability")
        selected_feat = st.selectbox(
            "Select Water Indicator for Density Analysis",
            options=FEATURES,
            format_func=lambda x: f"{x.replace('_', ' ')}",
            index=0
        )
        
        fig, ax = plt.subplots(figsize=(7.5, 3.8))
        palette = {0: "#475569", 1: "#0ed4be"}
        sns.histplot(
            data=df, x=selected_feat, hue=TARGET,
            kde=True, element="step", stat="density", common_norm=False,
            palette=palette, alpha=0.4, linewidth=1.5, ax=ax
        )
        ax.set_xlabel(f"{selected_feat.replace('_', ' ')}", fontsize=9, color="#94a9c4")
        ax.set_ylabel("Kernel Density", fontsize=9, color="#94a9c4")
        ax.legend(labels=["Potable (1)", "Non-Potable (0)"], facecolor="#0c1827", edgecolor="#1c3554", fontsize=8.5, labelcolor="#f1f7fc")
        st.pyplot(style_chart(fig, ax), clear_figure=True)
        
    with col_missing:
        st.markdown("#### ⚠️ Missing Value Summary")
        missing_s = df[FEATURES].isna().sum().sort_values(ascending=True)
        missing_s = missing_s[missing_s > 0]
        
        if not missing_s.empty:
            fig, ax = plt.subplots(figsize=(5.5, 3.8))
            bars = ax.barh(missing_s.index.str.replace("_", " "), missing_s.values, color="#38bdf8", height=0.45, alpha=0.85)
            ax.set_xlabel("Missing Observations", fontsize=8.5, color="#94a9c4")
            ax.set_xlim(0, max(missing_s.values) * 1.25)
            for bar in bars:
                w = bar.get_width()
                pct = (w / len(df)) * 100
                ax.text(w + 15, bar.get_y() + bar.get_height()/2, f"{int(w)} ({pct:.1f}%)",
                        va='center', ha='left', color="#ffffff", fontsize=8.5, fontweight="600")
            st.pyplot(style_chart(fig, ax), clear_figure=True)
        else:
            st.success("No missing values in features.")
            
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Expanders for Correlation and Dataset Preview
    with st.expander("📌 Feature Correlation Heatmap (Inter-indicator relationships)", expanded=False):
        fig_corr, ax_corr = plt.subplots(figsize=(9.5, 5.8))
        corr_matrix = df[FEATURES + [TARGET]].corr(numeric_only=True)
        
        # Teal to midnight diverging palette
        cmap = sns.diverging_palette(210, 170, s=80, l=45, as_cmap=True)
        sns.heatmap(
            corr_matrix, cmap=cmap, center=0, vmin=-0.2, vmax=0.2,
            annot=True, fmt=".2f", annot_kws={"size": 8.5, "weight": "bold"},
            linewidths=0.75, linecolor="#060d17", cbar=True, ax=ax_corr
        )
        ax_corr.set_xticklabels([c.replace("_", " ") for c in corr_matrix.columns], rotation=30, ha="right", fontsize=8.5)
        ax_corr.set_yticklabels([c.replace("_", " ") for c in corr_matrix.columns], rotation=0, fontsize=8.5)
        st.pyplot(style_chart(fig_corr, ax_corr, grid=False), clear_figure=True)
        st.caption("Notice: Most water quality predictors demonstrate low linear correlation with one another and the target, highlighting the need for non-linear models like Random Forest and SVM.")

    with st.expander("📋 Source Dataset Preview & Raw Data Download", expanded=False):
        st.dataframe(df.head(25), use_container_width=True, hide_index=True)
        st.download_button(
            "📥 Download Full Dataset (CSV)",
            df.to_csv(index=False).encode("utf-8"),
            file_name="aquantis_water_quality_dataset.csv",
            mime="text/csv"
        )

# =========================================================
# TAB 5: PREDICTION HISTORY
# =========================================================
with tabs[4]:
    st.markdown("""
    <div class="section-header">
        <div class="section-title">📜 Session Prediction History & Audit Log</div>
        <div class="section-sub">Detailed audit log of sample evaluations conducted during this active browser session.</div>
    </div>
    """, unsafe_allow_html=True)
    
    history_records = st.session_state.get("history", [])
    
    hist_count = len(history_records)
    h_col1, h_col2, h_col3 = st.columns([1, 1, 2])
    
    with h_col1:
        st.metric("Session Predictions", f"{hist_count}")
    with h_col2:
        if hist_count > 0:
            potable_count = sum(1 for r in history_records if r.get("Predicted Label") == "Potable")
            st.metric("Potable Classified", f"{potable_count} / {hist_count}")
        else:
            st.metric("Potable Classified", "0 / 0")
    with h_col3:
        if hist_count > 0:
            latest = history_records[0]
            st.markdown(f"""
            <div style='background:rgba(28, 53, 84, 0.4); border:1px solid #1c3554; border-radius:10px; padding:0.6rem 0.9rem;'>
                <div style='font-size:0.75rem; color:#94a9c4; font-weight:700; text-transform:uppercase;'>Most Recent Sample</div>
                <div style='font-size:0.95rem; color:#ffffff; font-weight:600;'>{latest['Model']} ➔ <span style='color:{"#34d399" if latest["Predicted Label"] == "Potable" else "#f87171"}'>{latest['Predicted Label']}</span> ({latest['Probability']:.1%})</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    
    if history_records:
        hist_df = pd.DataFrame(history_records)
        
        # Display clean dataframe
        st.dataframe(hist_df, use_container_width=True, hide_index=True)
        
        btn_col1, btn_col2, _ = st.columns([1.5, 1.5, 3])
        with btn_col1:
            st.download_button(
                "📥 Export History as CSV",
                hist_df.to_csv(index=False).encode("utf-8"),
                file_name="aquantis_prediction_history.csv",
                mime="text/csv",
                use_container_width=True
            )
        with btn_col2:
            if st.button("🗑️ Clear Session History", type="secondary", use_container_width=True):
                st.session_state.history = []
                st.rerun()
    else:
        st.markdown("""
        <div class="aq-card" style="text-align:center; padding:2.5rem 1rem;">
            <div style="font-size:2.2rem; margin-bottom:0.5rem;">💧</div>
            <div style="font-weight:700; font-size:1.1rem; color:#f1f7fc;">No Predictions Recorded Yet</div>
            <div style="font-size:0.86rem; color:#94a9c4; max-width:480px; margin:0.4rem auto 1rem auto;">
                Configure water measurements in the <strong>Analyze Sample</strong> workspace and run inference to populate this audit log.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("""
<div class="aq-footer">
    <div>
        <strong>AQUANTIS</strong> · Water Intelligence Platform · Machine Learning Lab Project
    </div>
    <div style="max-width: 600px; text-align: right;">
        <em>Disclaimer:</em> Research and educational prototype only. Predictions are derived from statistical patterns in the Water Potability benchmark and must not be used as a certified drinking-water safety indicator.
    </div>
</div>
""", unsafe_allow_html=True)
