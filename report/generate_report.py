import os
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from report_builder import (
    add_header_footer, format_paragraph, add_heading_1, add_heading_2, add_heading_3,
    add_body_p, add_bullet, add_callout, add_table_data, add_figure_image
)

def build_full_report():
    doc = Document()
    
    # Page setup - 1 inch margins all around
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        
    add_header_footer(doc)
    
    # =========================================================================
    # SECTION 1: TITLE PAGE
    # =========================================================================
    p_pre = doc.add_paragraph()
    format_paragraph(p_pre, space_before=36, space_after=12)
    p_pre.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_pre.add_run("ACADEMIC MINI-PROJECT REPORT\nDEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING")
    r_inst.font.name = "Arial"
    r_inst.font.size = Pt(11)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(100, 116, 139)
    
    p_title = doc.add_paragraph()
    format_paragraph(p_title, space_before=18, space_after=8)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("AQUANTIS: A Machine Learning Framework for Water Quality Prediction")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(24)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(11, 46, 60) # Midnight Navy
    
    p_sub = doc.add_paragraph()
    format_paragraph(p_sub, space_before=0, space_after=32)
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Comparative Benchmarking of Supervised Classifiers and Interactive Decision-Support Dashboard")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(13)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(8, 127, 140) # Rich Teal
    
    # Student / Submission Block
    p_by = doc.add_paragraph()
    format_paragraph(p_by, space_before=24, space_after=4)
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_by = p_by.add_run("Submitted in partial fulfillment of the requirements for the degree of\nBachelor of Technology in Computer Science & Engineering / Information Technology")
    r_by.font.name = "Calibri"
    r_by.font.size = Pt(10)
    r_by.font.color.rgb = RGBColor(71, 85, 105)
    
    # Metadata Table
    sub_table = [
        ["Course / Subject:", "Machine Learning Laboratory (CS-ML-P01)"],
        ["Candidate Name(s):", "[Student Name - e.g., Veer S. & Project Partner]"],
        ["University Roll No.:", "[University Roll Number / Registration ID]"],
        ["Under the Guidance of:", "[Faculty Mentor Name / Project Supervisor]"],
        ["Academic Institution:", "[Department of Computer Science & Engineering, University Name]"],
        ["Academic Year / Session:", "2025 – 2026"],
        ["Submission Date:", "October 2026"]
    ]
    add_table_data(doc, ["Attribute", "Candidate Submission Details"], sub_table, col_widths=[2.4, 4.1])
    
    doc.add_page_break()
    
    # =========================================================================
    # SECTION 2: ABSTRACT
    # =========================================================================
    add_heading_1(doc, "Abstract")
    add_body_p(doc, 
        "Access to safe, potable drinking water is a fundamental prerequisite for global public health and human development. "
        "Conventional water quality monitoring involves comprehensive microbiological, heavy-metal, and physicochemical laboratory "
        "examinations that require substantial equipment, specialized chemical reagents, and significant turnaround latency. "
        "In response, computational data-driven modeling offers rapid, automated preliminary screening by capturing complex multi-dimensional "
        "relationships among physical and chemical quality metrics. This mini-project presents AQUANTIS, an end-to-end Machine Learning "
        "framework designed to predict drinking water potability from nine physicochemical water indicators: pH, Hardness, Total Dissolved Solids, "
        "Chloramines, Sulfate, Electrical Conductivity, Total Organic Carbon, Trihalomethanes, and Turbidity.")
    
    add_body_p(doc,
        "Using a curated benchmark dataset of 3,276 water samples (1,998 non-potable, 1,278 potable), an empirical evaluation was conducted "
        "across four foundational supervised machine learning architectures: Support Vector Machine (RBF kernel), Random Forest, "
        "Logistic Regression, and K-Nearest Neighbors. To rigorously prevent data leakage, missing value imputation (median baseline) and "
        "standardization were encapsulated inside isolated scikit-learn Pipelines fitted strictly on training data under a stratified 80/20 train/test split. "
        "On the common held-out test partition (N = 656 samples), the Support Vector Machine achieved the highest F1-score (0.5118) and a balanced "
        "precision/recall trade-off (Precision = 0.5159, Recall = 0.5078), while Random Forest exhibited the highest classification accuracy (64.94%) "
        "and highest ROC-AUC (0.6597).")
    
    add_body_p(doc,
        "Crucially, this report emphasizes the critical safety and academic distinction between empirical pattern classification and "
        "regulatory water certification: automated predictions reflect historical dataset distributions and cannot guarantee physical potable "
        "safety without certified microbiological and chemical testing. An interactive Streamlit dashboard featuring an executive telemetry view, "
        "sample inference workspace, model diagnostic laboratory, dataset explorer, and session audit history was engineered to facilitate "
        "transparent inspection and academic defense.")
    
    add_body_p(doc, "Keywords: Machine Learning, Water Potability, Classification, Support Vector Machine, Random Forest, Scikit-learn, Model Benchmarking, Streamlit.", bold_prefix="Index Terms — ")
    
    # =========================================================================
    # SECTION 3: INTRODUCTION & PROBLEM DEFINITION
    # =========================================================================
    add_heading_1(doc, "1. Introduction")
    add_body_p(doc,
        "Water security is recognized under the United Nations Sustainable Development Goal 6 (SDG 6) as a universal imperative. "
        "Contaminated water supplies are primary transmission vectors for debilitating waterborne diseases, including cholera, dysentery, "
        "typhoid, and chronic chemical toxicities stemming from heavy metals or chlorination disinfection byproducts. While municipal water "
        "treatment plants and environmental protection agencies enforce stringent testing protocols, continuous laboratory assays of all "
        "distributed water points remain economically and logistically infeasible, particularly in rural and underserved distributed networks.")
    
    add_body_p(doc,
        "The advent of intelligent environmental sensors and predictive machine learning architectures presents a viable complementary "
        "paradigm: rapid data-driven classification. By measuring readily accessible physical, chemical, and mineral indicators, "
        "predictive algorithms can identify non-linear water quality anomalies, triage testing priorities, and alert authorities to potential "
        "contamination events.")
    
    add_heading_1(doc, "2. Problem Statement")
    add_body_p(doc,
        "Given a multi-dimensional feature vector X in R^9 representing physical and chemical water quality measurements, "
        "the objective is to construct and empirically validate a supervised binary classification hypothesis h(X) -> {0, 1} that maps "
        "these measurements to the binary target label 'Potability', where y = 1 denotes water classified as safe for consumption "
        "and y = 0 denotes non-potable water, while handling pervasive missing observations and maintaining strict insulation against data leakage.")
    
    add_heading_1(doc, "3. Objectives")
    add_bullet(doc, "To implement a clean, leakage-free data preprocessing pipeline incorporating median imputation and standard scaling inside isolated scikit-learn Pipelines.", bold_prefix="Objective 1 (Data Pipeline): ")
    add_bullet(doc, "To train and benchmark four distinct supervised classification algorithms (Logistic Regression, K-Nearest Neighbors, Support Vector Machine with RBF kernel, and Random Forest) using a standardized, stratified 80/20 train-test partition.", bold_prefix="Objective 2 (Model Benchmarking): ")
    add_bullet(doc, "To rigorously evaluate model discrimination using multiple evaluation metrics (Accuracy, Precision, Recall, F1-Score, Confusion Matrices, and ROC-AUC) to address class imbalance.", bold_prefix="Objective 3 (Comprehensive Evaluation): ")
    add_bullet(doc, "To develop a responsive, futuristic Web-based dashboard in Streamlit providing interactive sample prediction, real-time probability visualization, dataset exploration, and audit logging.", bold_prefix="Objective 4 (Dashboard Interface): ")
    add_bullet(doc, "To document the critical operational and safety boundaries of predictive environmental models, preventing unsafe over-reliance on algorithmic outputs in real-world drinking scenarios.", bold_prefix="Objective 5 (Responsible AI & Governance): ")
    
    add_heading_1(doc, "4. Scope and Significance")
    add_body_p(doc,
        "The technical scope of AQUANTIS encompasses offline exploratory data analysis, pipeline-based model fitting, hold-out metric validation, "
        "and local interactive dashboard deployment. It bridges undergraduate machine learning concepts—inductive bias, class imbalance, "
        "hyperplane margins, and ensemble bagging—with real-world environmental data science. Its significance lies in demonstrating how "
        "rigorous statistical methodology prevents premature model deployment and illuminates the true discriminative power of physicochemical data.")
    
    # =========================================================================
    # SECTION 4: LITERATURE REVIEW
    # =========================================================================
    add_heading_1(doc, "5. Literature Review")
    add_body_p(doc,
        "To establish rigorous academic context, five contemporary peer-reviewed research papers (published between 2024 and 2025) "
        "investigating machine learning frameworks for water quality assessment and potability classification were inspected and analyzed:")
    
    lit_table = [
        [
            "El-Bacha (2025)\nEnv. Challenges",
            "Predicting Water Potability Using a Machine Learning Approach\nDOI: 10.1016/j.envc.2025.101131",
            "Kaggle Water Potability (N=3,276)",
            "Supervised ML classifiers; feature correlation; automated imputation",
            "Demonstrated that ensemble algorithms capture non-linear relationships across water parameters better than linear baselines.",
            "Confirms that non-linear architectures (Random Forest/SVM) are essential for this feature space."
        ],
        [
            "Pereira et al. (2024)\nSustain. Comput.",
            "An Energy Efficient TinyML Model for Water Potability\nDOI: 10.1016/j.suscom.2024.101010",
            "Sensory water parameters / benchmark",
            "TinyML quantization for microcontroller edge deployment",
            "Compressed decision models achieved over 85% energy reduction on microcontrollers with minimal accuracy degradation.",
            "Highlights edge applicability; proves that trained pipeline weights can be exported for decentralized sensors."
        ],
        [
            "Sangwan & Bhardwaj (2024)\nWater Pract. Tech.",
            "Machine Learning Framework for Predicting Water Quality\nDOI: 10.2166/wpt.2024.259",
            "Environmental water indices & chemical metrics",
            "Comparative multi-classifier framework with optimization",
            "Detailed non-linear dynamic interdependencies among chemical indicators; validated standard normalization benefits.",
            "Validates AQUANTIS's multi-metric benchmarking and strict parameter scaling."
        ],
        [
            "Chatterjee et al. (2024)\nPLOS Water",
            "Optimizing ML for Water Safety: Comparative Analysis with PCA\nDOI: 10.1371/journal.pwat.0000259",
            "Water Potability Dataset (9 features)",
            "Baseline ML vs. PCA Dimensionality Reduction (6 components)",
            "Baseline models scored 62%–69% accuracy (SVM top at 69%); PCA transformation dramatically improved cluster separation.",
            "Directly benchmarks our baseline results: SVM and RF baseline accuracy in AQUANTIS (62.2% and 64.9%) matches their reported raw baseline range."
        ],
        [
            "Kamath et al. (2025)\nETASR",
            "Exploratory Data Analysis & Water Potability with Supervised ML\nDOI: 10.48084/etasr.8904",
            "Water Potability Dataset (3,276 rows)",
            "EDA, SMOTE resampling, Optuna tuning, Weighted Voting Ensemble",
            "Random Forest reached 68% accuracy after tuning; hybrid RF+KNN voting ensemble achieved 71% accuracy.",
            "Confirms that tree-based ensembles lead individual classifiers on this dataset; informs AQUANTIS's future ensemble tuning."
        ]
    ]
    
    add_table_data(doc, 
                   ["Paper & Citation", "Title & DOI", "Dataset Used", "Methodology", "Key Verified Findings", "Relevance to AQUANTIS"], 
                   lit_table, 
                   col_widths=[1.1, 1.4, 0.9, 1.1, 1.2, 1.1])
    
    add_heading_1(doc, "6. Research Gap and Project Motivation")
    add_body_p(doc,
        "While published literature demonstrates varying degrees of classification accuracy, a prominent research gap persists in "
        "practical engineering demonstrations: many studies either report raw accuracy on imbalanced data without detailing the precision/recall "
        "trade-offs crucial for drinking water safety, or they apply data scaling and imputation across the entire dataset prior to partitioning, "
        "introducing subtle data leakage. Furthermore, few implementations package trained models into accessible, transparent diagnostic "
        "tools that provide explicit probability confidence scores and audit histories. AQUANTIS addresses this gap by implementing an airtight "
        "pipeline architecture coupled with an intuitive, telemetry-grade dashboard that prioritizes ethical transparency over blind accuracy claims.")
    
    # =========================================================
    # SECTION 5: SYSTEM ARCHITECTURE & DATASET
    # =========================================================
    add_heading_1(doc, "7. Proposed System Architecture")
    add_body_p(doc,
        "The AQUANTIS architecture is organized into a modular four-tier hierarchy: Data Ingestion, Pipeline Preprocessing, "
        "Model Training & Benchmarking, and Interactive Inference/Audit Interface. All pipeline transformations are implemented using "
        "scikit-learn Pipeline abstractions to enforce separation of concerns.")
    
    add_callout(doc,
        "System Execution Flow:\n"
        "1. Raw CSV Ingestion (data/water_potability.csv) -> Type Coercion & Integrity Validation\n"
        "2. Stratified Hold-Out Split (80% Train: 2,620 samples / 20% Test: 656 samples, Seed=42)\n"
        "3. Pipeline Execution: SimpleImputer(median) -> StandardScaler() -> Estimator\n"
        "4. Model Benchmarking: Metric computation (Accuracy, Precision, Recall, F1, ROC-AUC)\n"
        "5. Model Serialization: Joblib bundle export (models/aquantis_bundle.joblib)\n"
        "6. Telemetry & User Interface: Streamlit 5-section dashboard with session audit logging.",
        "AQUANTIS Architectural Workflow Summary")
    
    add_heading_1(doc, "8. Dataset Description")
    add_body_p(doc,
        "The framework is trained and evaluated on the widely recognized Kaggle Water Potability benchmark dataset. "
        "The dataset contains 3,276 individual water sample records. Each sample is characterized by 9 numerical physicochemical continuous features "
        "and one binary target variable (Potability).")
    
    feat_table = [
        ["ph", "Continuous (pH units)", "0.000 – 14.000", "7.081 ± 1.594", "491 (14.99%)", "Acid-base balance (WHO recommended safe drinking range: 6.5 – 8.5)."],
        ["Hardness", "Continuous (mg/L)", "47.432 – 323.124", "196.369 ± 32.880", "0 (0.00%)", "Calcium and Magnesium salt concentration causing soap precipitation."],
        ["Solids (TDS)", "Continuous (ppm)", "320.943 – 61,227.196", "22,014.093 ± 8,768.571", "0 (0.00%)", "Total Dissolved Solids indicating mineral and salt saturation."],
        ["Chloramines", "Continuous (ppm)", "0.352 – 13.127", "7.122 ± 1.583", "0 (0.00%)", "Chlorine-ammonia disinfectant residuals (EPA limit: <= 4.0 ppm)."],
        ["Sulfate", "Continuous (mg/L)", "129.000 – 481.031", "333.776 ± 41.417", "781 (23.84%)", "Dissolved mineral salts from natural geological formations."],
        ["Conductivity", "Continuous (µS/cm)", "181.484 – 753.343", "426.205 ± 80.824", "0 (0.00%)", "Electrical conductivity reflecting dissolved ionic concentration."],
        ["Organic_carbon", "Continuous (ppm)", "2.200 – 28.300", "14.285 ± 3.308", "0 (0.00%)", "Total Organic Carbon (TOC) measuring dissolved organic matter."],
        ["Trihalomethanes", "Continuous (µg/L)", "0.738 – 124.000", "66.396 ± 16.175", "162 (4.95%)", "Disinfection byproducts formed by chlorine-organic matter reactions."],
        ["Turbidity", "Continuous (NTU)", "1.450 – 6.739", "3.967 ± 0.780", "0 (0.00%)", "Water clarity and cloudiness due to suspended fine particulates."],
        ["Potability (Target)", "Binary Categorical", "0 or 1", "0: 61.0%, 1: 39.0%", "0 (0.00%)", "Target class: 1 denotes Potable (Safe), 0 denotes Non-Potable (Unsafe)."]
    ]
    add_table_data(doc, ["Feature Name", "Type & Units", "Observed Range", "Mean ± Std Dev", "Missing Count (%)", "Physicochemical Significance"], feat_table, col_widths=[1.1, 1.1, 1.1, 1.1, 1.0, 1.6])
    
    # =========================================================
    # SECTION 6: EDA & DATA CLEANING
    # =========================================================
    add_heading_1(doc, "9. Exploratory Data Analysis")
    add_body_p(doc,
        "Exploratory Data Analysis (EDA) was performed across the 3,276 records to examine class proportions, missing value patterns, "
        "and pairwise inter-feature correlations. Analysis of the target variable reveals that 1,998 samples (60.99%) are classified as "
        "Non-Potable (Class 0), while 1,278 samples (39.01%) are classified as Potable (Class 1). This 61:39 ratio represents a moderate "
        "class imbalance that makes raw Accuracy an inadequate benchmark indicator.")
    
    add_figure_image(doc, "report/figures/fig1_class_distribution.png", "Figure 1: Class distribution of target Potability variable in source dataset.")
    add_figure_image(doc, "report/figures/fig2_missing_values.png", "Figure 2: Missing value incidence across monitored water indicators.")
    
    add_body_p(doc,
        "Missing value profiling indicates that missingness is concentrated in three indicators: Sulfate lacks 781 observations (23.84%), "
        "pH lacks 491 observations (14.99%), and Trihalomethanes lacks 162 observations (4.95%). The remaining six parameters have complete "
        "records across all 3,276 samples. In total, 1,434 individual cells (4.87% of all matrix entries) require imputation.")
    
    add_figure_image(doc, "report/figures/fig6_correlation_heatmap.png", "Figure 3: Pairwise Pearson correlation heatmap between physicochemical features and target.")
    
    add_body_p(doc,
        "The Pearson correlation heatmap (Figure 3) demonstrates an essential characteristic of this domain: linear correlations between "
        "all pairs of features—as well as between individual features and the target label—are remarkably weak, spanning between -0.09 and +0.03. "
        "This absence of strong linear collinearity demonstrates that no single chemical metric acts as an isolated determinant of potability. "
        "Consequently, linear decision boundaries are expected to underperform relative to non-linear kernel and ensemble architectures.")
    
    add_heading_1(doc, "10. Data Cleaning and Preprocessing Pipeline")
    add_body_p(doc,
        "A critical pitfall in published machine learning research is data leakage, which occurs when transformations (such as computing "
        "the mean, median, or variance) are computed over the full dataset before splitting into training and test partitions. "
        "Under such conditions, the model's test evaluation is artificially optimistic because test set distribution parameters have leaked "
        "into training.")
    
    add_body_p(doc,
        "In AQUANTIS, data integrity is rigorously safeguarded by encapsulating preprocessing inside scikit-learn Pipelines. "
        "First, records missing target labels or containing non-binary values are verified and dropped. Then, an 80/20 stratified split is executed. "
        "Within each pipeline, a SimpleImputer(strategy='median') computes median replacement values strictly from training rows X_train. "
        "For distance-sensitive and margin-based classifiers (Logistic Regression, KNN, and SVM), a StandardScaler() normalizes feature "
        "distributions to zero mean and unit variance. For Random Forest, tree partition splits are invariant to monotonic scaling; "
        "hence, scaling is omitted to preserve original physical feature magnitudes.")
    
    # =========================================================
    # SECTION 7: METHODOLOGY & ALGORITHMS
    # =========================================================
    add_heading_1(doc, "11. Methodology and Experimental Setup")
    add_body_p(doc,
        "The experiments were executed on a Windows 64-bit environment using Python 3.13, Scikit-learn 1.6+, Pandas 2.2+, NumPy 2.2+, "
        "and Streamlit 1.43+. The dataset of 3,276 samples was partitioned into a training set of 2,620 samples (80%) and a held-out "
        "test set of 656 samples (20%) using stratified random sampling with fixed seed random_state=42. "
        "The exact class composition in the test set is 400 Non-Potable samples (60.98%) and 256 Potable samples (39.02%), faithfully "
        "mirroring the overall dataset balance.")
    
    add_heading_1(doc, "12. Machine Learning Algorithms Evaluated")
    add_body_p(doc, "Four foundational algorithms with diverse inductive biases were selected for comparative study:", bold_prefix="Algorithm Selection: ")
    
    add_body_p(doc,
        "Logistic Regression models the log-odds of potability as a linear combination of input indicators: "
        "logit(P(Y=1|X)) = w^T X + b. The optimization is performed using the L-BFGS solver with a maximum iteration cap of 2,000. "
        "To counter class imbalance, class_weight='balanced' inversely weights class loss by class frequencies.", bold_prefix="1. Logistic Regression: ")
    
    add_body_p(doc,
        "KNN is a non-parametric instance-based learner that assigns a class label based on the majority vote of the k closest training "
        "instances in Euclidean space. In AQUANTIS, k = 7 nearest neighbors was selected with standard feature scaling to prevent features "
        "with large numerical scales (e.g., Solids) from dominating distance computations.", bold_prefix="2. K-Nearest Neighbors (KNN): ")
    
    add_body_p(doc,
        "SVM constructs an optimal separating hyperplane in a transformed high-dimensional Hilbert feature space defined by the Radial Basis Function (RBF) kernel: "
        "K(x_i, x_j) = exp(-gamma ||x_i - x_j||^2). Regularization parameter C = 1.0 was utilized with balanced class weighting. "
        "Calibrated class probabilities are obtained via Platt scaling (probability=True).", bold_prefix="3. Support Vector Machine (SVM): ")
    
    add_body_p(doc,
        "Random Forest is an ensemble bagging architecture that constructs a collection of 300 de-correlated decision trees (n_estimators=300). "
        "Each tree is trained on a bootstrap sample of the training data, and split decisions at each node consider a random subset of features. "
        "The final class prediction is obtained through majority voting, while probabilities represent the fraction of tree votes for the positive class.", bold_prefix="4. Random Forest (RF): ")
    
    # =========================================================
    # SECTION 8: EVALUATION METRICS
    # =========================================================
    add_heading_1(doc, "13. Evaluation Metrics and Mathematical Definitions")
    add_body_p(doc,
        "In water quality safety classification, evaluation metrics must balance both false alarms (Type I error: non-potable water predicted as potable) "
        "and false assurances (Type II error: dangerous water predicted as safe). Let TP denote True Positives, TN True Negatives, "
        "FP False Positives, and FN False Negatives on the held-out test partition:")
    
    add_bullet(doc, "Accuracy = (TP + TN) / (TP + TN + FP + FN). Measures overall correct predictions, but can be deceptive under class imbalance.", bold_prefix="Accuracy: ")
    add_bullet(doc, "Precision = TP / (TP + FP). Reflects reliability of positive predictions: of all samples predicted potable, how many are actually safe.", bold_prefix="Precision: ")
    add_bullet(doc, "Recall (Sensitivity) = TP / (TP + FN). Measures completeness: of all actually potable samples, how many were identified.", bold_prefix="Recall: ")
    add_bullet(doc, "F1-Score = 2 * (Precision * Recall) / (Precision + Recall). The harmonic mean of precision and recall, balancing Type I and Type II errors.", bold_prefix="F1-Score: ")
    add_bullet(doc, "ROC-AUC = Area under the Receiver Operating Characteristic curve. Evaluates threshold-independent ranking capability across all probability cutoffs.", bold_prefix="ROC-AUC: ")
    
    # =========================================================
    # SECTION 9: RESULTS AND DISCUSSION
    # =========================================================
    add_heading_1(doc, "14. Experimental Results and Model Comparison")
    add_body_p(doc,
        "All four models were fitted on the 2,620 training samples and evaluated on the 656 held-out test samples. "
        "The measured results, recorded directly from the AQUANTIS evaluation pipeline in results/model_comparison.csv, are summarized below:")
    
    results_table = [
        ["Support Vector Machine", "0.6220 (62.20%)", "0.5159 (51.59%)", "0.5078 (50.78%)", "0.5118", "0.6440"],
        ["Random Forest", "0.6494 (64.94%)", "0.5691 (56.91%)", "0.4180 (41.80%)", "0.4820", "0.6597"],
        ["Logistic Regression", "0.5244 (52.44%)", "0.4146 (41.46%)", "0.5312 (53.12%)", "0.4658", "0.5474"],
        ["K-Nearest Neighbors", "0.5899 (58.99%)", "0.4581 (45.81%)", "0.2773 (27.73%)", "0.3455", "0.5972"]
    ]
    add_table_data(doc, ["Model Architecture", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"], results_table, col_widths=[1.8, 1.0, 1.0, 1.0, 1.0, 1.0])
    
    add_figure_image(doc, "report/figures/fig3_model_comparison.png", "Figure 4: Comparative evaluation across all four classification models on the 20% test set.")
    
    add_heading_1(doc, "15. In-Depth Results Discussion and Trade-Off Analysis")
    add_body_p(doc,
        "Analysis of the experimental benchmarks yields critical insights into algorithm behavior on environmental quality data:", bold_prefix="Key Analytical Insights: ")
    
    add_bullet(doc,
        "Support Vector Machine achieved the top F1-score (0.5118), balancing Precision (51.59%) and Recall (50.78%). "
        "Because it utilizes the RBF kernel to project features into a higher-dimensional space with balanced class weighting, "
        "it avoided skewing predictions toward the majority non-potable class.", bold_prefix="SVM Balanced Trade-Off: ")
    
    add_bullet(doc,
        "Random Forest achieved the highest Accuracy (64.94%), highest Precision (56.91%), and highest ROC-AUC (0.6597). "
        "However, its Recall was 41.80%, indicating that it identified only 107 of the 256 truly potable samples. "
        "It tended to be conservative, making fewer positive predictions but ensuring that positive predictions were more reliable.", bold_prefix="Random Forest Conservatism: ")
    
    add_bullet(doc,
        "Logistic Regression produced the lowest Accuracy (52.44%) and ROC-AUC (0.5474), barely outperforming random chance. "
        "This confirms that the complex interactions among water quality metrics cannot be separated by a planar hyperplane.", bold_prefix="Linear Inseparability: ")
    
    add_bullet(doc,
        "KNN struggled significantly with Recall (27.73%), missing nearly three out of every four potable samples (185 False Negatives). "
        "In a 9-dimensional continuous feature space, distance metrics suffer from sparsity, causing minority class samples to be surrounded "
        "by majority class neighbors.", bold_prefix="Curse of Dimensionality in KNN: ")
    
    add_heading_1(doc, "16. Confusion Matrix and ROC Curve Analysis")
    add_body_p(doc,
        "To inspect exact classification counts on the 656 test samples, Table 5 and Figures 5 and 6 present the complete error breakdown:")
    
    cm_table = [
        ["Support Vector Machine", "278 (69.5%)", "122 (30.5%)", "126 (49.2%)", "130 (50.8%)"],
        ["Random Forest", "319 (79.8%)", "81 (20.2%)", "149 (58.2%)", "107 (41.8%)"],
        ["Logistic Regression", "208 (52.0%)", "192 (48.0%)", "120 (46.9%)", "136 (53.1%)"],
        ["K-Nearest Neighbors", "316 (79.0%)", "84 (21.0%)", "185 (72.3%)", "71 (27.7%)"]
    ]
    add_table_data(doc, ["Model Architecture", "True Negatives (TN)", "False Positives (FP)", "False Negatives (FN)", "True Positives (TP)"], cm_table, col_widths=[1.8, 1.2, 1.2, 1.2, 1.2])
    
    add_figure_image(doc, "report/figures/fig4_confusion_matrices.png", "Figure 5: Confusion matrices for all four classifiers on the 656-sample held-out test set.")
    add_figure_image(doc, "report/figures/fig5_roc_curves.png", "Figure 6: Receiver Operating Characteristic (ROC) curves showing threshold discrimination.")
    
    add_body_p(doc,
        "The ROC curves (Figure 6) illustrate the true positive rate versus false positive rate across all discrimination thresholds. "
        "Random Forest achieves the superior overall trajectory (AUC = 0.660), followed closely by Support Vector Machine (AUC = 0.644). "
        "K-Nearest Neighbors achieves AUC = 0.597, and Logistic Regression achieves AUC = 0.547. All models maintain trajectories "
        "above the random guessing diagonal (AUC = 0.500), verifying genuine statistical signal extraction from the underlying indicators.")
    
    # =========================================================
    # SECTION 10: APPLICATION DESIGN & VALIDATION
    # =========================================================
    add_heading_1(doc, "17. Streamlit Application Architecture & User Interface")
    add_body_p(doc,
        "The front-end of AQUANTIS was implemented as a Streamlit web application adhering to a dark environmental technology "
        "design system (deep midnight navy background #060d17, surface cards #0c1827, and rich teal #0ed4be accents). "
        "The application provides five distinct operational sections:")
    
    add_bullet(doc, "Executive dashboard featuring key performance indicator cards (record count, indicator count, model count, top F1 model, peak ROC-AUC), horizontal grouped model benchmark charts, class distribution, and data pipeline documentation.", bold_prefix="1. Overview Tab: ")
    add_bullet(doc, "Interactive prediction workspace organizing the 9 indicators into three scientific categories (Acidity & Disinfection, Mineral & Carbon Content, Physical & Clarity). Includes bounded inputs, step sizes, tooltips, model selector, prediction badge, probability chart, and disclaimers.", bold_prefix="2. Analyze Sample Tab: ")
    add_bullet(doc, "Comprehensive model laboratory providing an interactive metrics leaderboard, confusion matrix heatmaps, ROC curve plots, detailed scikit-learn classification reports, and CSV metric downloads.", bold_prefix="3. Model Lab Tab: ")
    add_bullet(doc, "Exploratory data workspace featuring kernel density distribution plots for any selected indicator grouped by potability class, a missing value horizontal bar chart, a Pearson correlation matrix, and source dataset export.", bold_prefix="4. Data Explorer Tab: ")
    add_bullet(doc, "Live audit logging tracking all sample analyses conducted during the active session. Displays timestamp, chosen model, predicted classification, potability probability, input parameter values, and CSV audit export.", bold_prefix="5. Prediction History Tab: ")
    
    add_heading_1(doc, "18. System Testing and Validation")
    add_body_p(doc,
        "Rigorous software engineering validation was performed across the codebase: "
        "1. Static syntax verification via python -m py_compile app.py confirmed zero syntax or formatting defects. "
        "2. Pipeline integration testing verified that train_and_evaluate() reliably loads data, executes the stratified 80/20 split, fits all four pipelines, and serializes artifacts without data leakage. "
        "3. Cross-platform Matplotlib verification confirmed that figure generation utilizing clear_figure=True eliminated FigureCanvasAgg keyword incompatibilities. "
        "4. Live HTTP verification confirmed that the Streamlit server boots and serves on port 8501 with HTTP 200 responses.")
    
    # =========================================================
    # SECTION 11: LIMITATIONS & FUTURE WORK
    # =========================================================
    add_heading_1(doc, "19. Limitations and Ethical Disclaimers")
    add_body_p(doc,
        "In accordance with responsible academic engineering, the primary operational limitations of the project are explicitly documented:")
    
    add_bullet(doc, "The Kaggle Water Potability dataset is a static benchmark derived from historical aggregated sources. It does not reflect specific geographic watersheds, real-time seasonal variations, or immediate upstream contamination events.", bold_prefix="1. Benchmark Dataset Scope: ")
    add_bullet(doc, "Approximately 23.8% of Sulfate and 15.0% of pH readings are missing in the dataset. While median imputation provides a robust statistical baseline, it does not reconstruct unobserved physical dynamics.", bold_prefix="2. Imputation Approximations: ")
    add_bullet(doc, "Machine learning predictions indicate statistical correlations within the training distribution; they do not certify bacteriological safety, heavy metal compliance, or regulatory drinking water potability. Certified laboratory testing remains mandatory for real-world consumption.", bold_prefix="3. Certification Disclaimer: ")
    
    add_heading_1(doc, "20. Future Enhancements")
    add_bullet(doc, "Implementing SMOTE oversampling and Optuna hyperparameter optimization to improve Random Forest recall and F1-score.", bold_prefix="1. Advanced Resampling & Hyperparameter Tuning: ")
    add_bullet(doc, "Constructing a weighted soft-voting ensemble combining Random Forest and RBF SVM probabilities to maximize AUC-ROC.", bold_prefix="2. Ensemble Stacking: ")
    add_bullet(doc, "Implementing TinyML model quantization (as demonstrated by Pereira et al., 2024) to enable direct deployment onto low-power ESP32 or ARM Cortex microcontrollers paired with physical sensors.", bold_prefix="3. Edge IoT Deployment: ")
    add_bullet(doc, "Conducting SHAP (SHapley Additive exPlanations) feature attribution to provide interpretable explanations for individual sample classifications.", bold_prefix="4. Explainable AI (XAI): ")
    
    add_heading_1(doc, "21. Conclusion")
    add_body_p(doc,
        "The AQUANTIS project successfully demonstrates the design, empirical evaluation, and dashboard deployment of an end-to-end "
        "machine learning framework for water quality prediction. By comparing four distinct classifiers on a common held-out test split, "
        "the study demonstrated that non-linear kernel and tree ensemble methods significantly outperform linear baselines. "
        "Support Vector Machine achieved the most balanced trade-off between precision and recall (F1 = 0.5118), while Random Forest "
        "delivered the highest classification accuracy (64.94%) and discriminative ability (ROC-AUC = 0.6597). "
        "Through strict pipeline encapsulation against data leakage, comprehensive multi-metric benchmarking, and an interactive "
        "Streamlit telemetry interface, AQUANTIS provides a robust, educational, and defense-ready machine learning mini-project.")
    
    # =========================================================
    # SECTION 12: REFERENCES
    # =========================================================
    add_heading_1(doc, "22. References")
    
    refs = [
        "[1] R. El-Bacha, \"Predicting Water Potability Using a Machine Learning Approach,\" Environmental Challenges, vol. 19, p. 101131, Mar. 2025. DOI: 10.1016/j.envc.2025.101131.",
        "[2] E. A. M. Pereira, J. F. d. S. Santos, and E. d. A. Barboza, \"An Energy Efficient TinyML Model for a Water Potability Classification Problem,\" Sustainable Computing: Informatics and Systems, vol. 43, p. 101010, Jun. 2024. DOI: 10.1016/j.suscom.2024.101010.",
        "[3] V. Sangwan and R. Bhardwaj, \"Machine Learning Framework for Predicting Water Quality Classification,\" Water Practice & Technology, vol. 19, no. 11, pp. 4499–4521, Nov. 2024. DOI: 10.2166/wpt.2024.259.",
        "[4] D. Chatterjee, P. Ghosh, A. Banerjee, and S. S. Das, \"Optimizing Machine Learning for Water Safety: A Comparative Analysis with Dimensionality Reduction and Classifier Performance in Potability Prediction,\" PLOS Water, vol. 3, no. 8, p. e0000259, Aug. 2024. DOI: 10.1371/journal.pwat.0000259.",
        "[5] P. K. B., G. Sharma, A. Bongale, D. Dharrao, and M. Seitshiro, \"Exploratory Data Analysis and Water Potability Classification Using Supervised Machine Learning Algorithms,\" Engineering, Technology & Applied Science Research, vol. 15, no. 2, pp. 20898–20903, Apr. 2025. DOI: 10.48084/etasr.8904.",
        "[6] Kaggle, \"Water Potability Dataset: Clean Water Evaluation and Classification Benchmark,\" [Online]. Available: https://www.kaggle.com/datasets/adityakadiwal/water-potability.",
        "[7] F. Pedregosa et al., \"Scikit-learn: Machine Learning in Python,\" Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011.",
        "[8] L. Breiman, \"Random Forests,\" Machine Learning, vol. 45, no. 1, pp. 5–32, 2001.",
        "[9] C. Cortes and V. Vapnik, \"Support-Vector Networks,\" Machine Learning, vol. 20, no. 3, pp. 273–297, 1995.",
        "[10] World Health Organization (WHO), \"Guidelines for Drinking-Water Quality,\" 4th ed., Geneva: World Health Organization, 2017."
    ]
    for ref in refs:
        p_ref = doc.add_paragraph()
        format_paragraph(p_ref, space_before=2, space_after=4, line_spacing=1.15)
        run_ref = p_ref.add_run(ref)
        run_ref.font.name = "Calibri"
        run_ref.font.size = Pt(9.5)
        run_ref.font.color.rgb = RGBColor(30, 41, 59)
        
    out_path = Path("report") / "AQUANTIS_Academic_Project_Report.docx"
    doc.save(out_path)
    print(f"Report document successfully saved to: {out_path}")

if __name__ == "__main__":
    build_full_report()
