import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

FIG_DIR = Path("report") / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Set high DPI and aesthetic styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

def generate_system_workflow():
    fig, ax = plt.subplots(figsize=(12, 4.4), dpi=300)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#FFFFFF')
    ax.axis('off')
    
    stages = [
        {"title": "1. Data Acquisition", "desc": "Kaggle Benchmark\n(3,276 samples, 9 features)\nWater Potability CSV", "color": "#0B2E3C", "border": "#087F8C"},
        {"title": "2. Data Split", "desc": "Integrity Check\nStratified 80/20 Hold-Out\nTrain: 2,620 | Test: 656", "color": "#0F4C5C", "border": "#0EA5E9"},
        {"title": "3. Preprocessing", "desc": "SimpleImputer (median)\nStandardScaler (z-score)\nFitted strictly on X_train", "color": "#136F63", "border": "#10B981"},
        {"title": "4. Benchmarking", "desc": "SVM (RBF), Random Forest,\nLogistic Reg., KNN (k=7)\nCommon Test Partition", "color": "#1E3A8A", "border": "#3B82F6"},
        {"title": "5. Deployment", "desc": "Streamlit Web UI\nInference & Diagnostics\nSession Audit Logging", "color": "#312E81", "border": "#6366F1"},
    ]
    
    n = len(stages)
    box_w = 1.95
    box_h = 2.4
    spacing = (11.0 - n * box_w) / (n + 1)
    
    for i, s in enumerate(stages):
        x = spacing + i * (box_w + spacing)
        y = 0.9
        
        # Shadow
        rect_shadow = patches.FancyBboxPatch(
            (x + 0.04, y - 0.04), box_w, box_h,
            boxstyle="round,pad=0.06,rounding_size=0.14",
            facecolor='#CBD5E1', edgecolor='none', alpha=0.5
        )
        ax.add_patch(rect_shadow)
        
        # Card
        rect = patches.FancyBboxPatch(
            (x, y), box_w, box_h,
            boxstyle="round,pad=0.06,rounding_size=0.14",
            facecolor='#FFFFFF', edgecolor=s["border"], linewidth=2.0
        )
        ax.add_patch(rect)
        
        # Header banner
        header_rect = patches.FancyBboxPatch(
            (x, y + box_h - 0.65), box_w, 0.65,
            boxstyle="round,pad=0.06,rounding_size=0.14",
            facecolor=s["color"], edgecolor='none'
        )
        ax.add_patch(header_rect)
        
        # Header text
        ax.text(x + box_w/2, y + box_h - 0.32, s["title"],
                ha='center', va='center', color='#FFFFFF', fontsize=9.5, fontweight='bold')
        
        # Description text
        ax.text(x + box_w/2, y + (box_h - 0.65)/2, s["desc"],
                ha='center', va='center', color='#1E293B', fontsize=8.2, linespacing=1.35)
        
        # Arrow to next stage
        if i < n - 1:
            arrow_x = x + box_w + 0.04
            arrow_w = spacing - 0.08
            ax.annotate('', xy=(arrow_x + arrow_w, y + box_h/2),
                        xytext=(arrow_x, y + box_h/2),
                        arrowprops=dict(facecolor='#087F8C', edgecolor='#087F8C', width=2.2, headwidth=7, headlength=6))

    ax.set_xlim(0, 11.8)
    ax.set_ylim(0.4, 4.0)
    plt.title("AQUANTIS End-to-End Methodological Workflow", fontsize=13, fontweight='bold', pad=15, color='#0B2E3C')
    plt.tight_layout()
    out_path = FIG_DIR / "fig_workflow.png"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

def generate_system_architecture():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#FFFFFF')
    ax.axis('off')
    
    # 4 Architecture Layers
    layers = [
        {"title": "TIER 1: DATA INGESTION & VALIDATION", "y": 4.8, "h": 1.1, "color": "#0B2E3C",
         "items": ["Kaggle Benchmark Dataset\n(3,276 Rows, 9 Features)", "Type Coercion & Verification\n(Float64 Conversion)", "Target Filter\n(Potability ∈ {0, 1})"]},
        {"title": "TIER 2: PREPROCESSING PIPELINE (LEAKAGE ISOLATION)", "y": 3.3, "h": 1.1, "color": "#0F4C5C",
         "items": ["Stratified 80/20 Train-Test Split\n(Train: 2,620, Test: 656, Seed=42)", "Median Imputation\n(SimpleImputer strictly on X_train)", "Standardization (Z-Score)\n(StandardScaler on X_train)"]},
        {"title": "TIER 3: MODEL TRAINING & METRIC BENCHMARKING", "y": 1.8, "h": 1.1, "color": "#1E3A8A",
         "items": ["Support Vector Machine\n(RBF Kernel, C=1.0, Balanced)", "Random Forest\n(300 Trees, Gini Impurity, Bagging)", "Logistic Reg. & KNN (k=7)\n(L-BFGS, Euclidean Distance)", "Joblib Serialization\n(aquantis_bundle.joblib)"]},
        {"title": "TIER 4: STREAMLIT TELEMETRY & DECISION-SUPPORT DASHBOARD", "y": 0.3, "h": 1.1, "color": "#312E81",
         "items": ["Executive Telemetry\n(KPI Cards, Benchmark Charts)", "Interactive Analysis\n(3-Category Feature Sliders)", "Model Lab & EDA\n(ROC, Heatmaps, Densities)", "Prediction Audit Log\n(Session Audit, CSV Export)"]}
    ]
    
    for l in layers:
        y = l["y"]
        h = l["h"]
        
        # Layer container
        rect_layer = patches.FancyBboxPatch(
            (0.5, y), 10.0, h,
            boxstyle="round,pad=0.06,rounding_size=0.12",
            facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.2
        )
        ax.add_patch(rect_layer)
        
        # Layer Header Banner
        header = patches.FancyBboxPatch(
            (0.5, y + h - 0.32), 10.0, 0.32,
            boxstyle="round,pad=0.06,rounding_size=0.12",
            facecolor=l["color"], edgecolor='none'
        )
        ax.add_patch(header)
        ax.text(5.5, y + h - 0.16, l["title"], ha='center', va='center', color='#FFFFFF', fontsize=9.5, fontweight='bold')
        
        # Sub-boxes
        items = l["items"]
        m = len(items)
        sub_w = (9.4 - (m - 1) * 0.25) / m
        for j, itm in enumerate(items):
            sub_x = 0.8 + j * (sub_w + 0.25)
            sub_y = y + 0.08
            sub_h = h - 0.46
            
            box_sub = patches.FancyBboxPatch(
                (sub_x, sub_y), sub_w, sub_h,
                boxstyle="round,pad=0.04,rounding_size=0.08",
                facecolor='#F1F5F9', edgecolor='#94A3B8', linewidth=0.8
            )
            ax.add_patch(box_sub)
            ax.text(sub_x + sub_w/2, sub_y + sub_h/2, itm, ha='center', va='center',
                    color='#0F172A', fontsize=8, fontweight='medium', linespacing=1.3)
            
    # Connective Vertical Arrows between layers
    for arr_y in [4.8, 3.3, 1.8]:
        ax.annotate('', xy=(5.5, arr_y), xytext=(5.5, arr_y + 0.28),
                    arrowprops=dict(facecolor='#087F8C', edgecolor='#087F8C', width=2.5, headwidth=7, headlength=6))
        
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.4)
    plt.title("AQUANTIS Layered System Architecture & Data Pipeline", fontsize=13, fontweight='bold', pad=15, color='#0B2E3C')
    plt.tight_layout()
    out_path = FIG_DIR / "fig_architecture.png"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

if __name__ == "__main__":
    generate_system_workflow()
    generate_system_architecture()
