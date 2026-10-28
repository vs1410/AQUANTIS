import os
import sys
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from report_builder import (
    set_cell_background, set_cell_margins, set_cell_border,
    format_paragraph, add_heading_1, add_heading_2, add_heading_3,
    add_body_p, add_bullet, add_callout, add_table_data, add_figure_image
)

def add_clean_header_footer(doc):
    for s in doc.sections:
        s.different_first_page_header_footer = True
        header = s.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("AQUANTIS: Water Quality Prediction Framework | Academic Project Report")
        hrun.font.name = "Arial"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(148, 163, 184)
        
        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Department of Computer Science & Engineering | Academic Project Evaluation")
        frun.font.name = "Arial"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(148, 163, 184)

def build_aquantis_final_report():
    doc = Document()
    
    # 1. Page setup - 1 inch margins all around, Standard Letter
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        
    add_clean_header_footer(doc)
    
    # =========================================================================
    # 1. TITLE PAGE
    # =========================================================================
    p_inst = doc.add_paragraph()
    format_paragraph(p_inst, space_before=24, space_after=10)
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("ACADEMIC PROJECT REPORT\nDEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING")
    r_inst.font.name = "Arial"
    r_inst.font.size = Pt(11)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(100, 116, 139)
    
    p_title = doc.add_paragraph()
    format_paragraph(p_title, space_before=16, space_after=8)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("AQUANTIS: A Machine Learning Framework for Water Quality Prediction")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(11, 46, 60)
    
    p_sub = doc.add_paragraph()
    format_paragraph(p_sub, space_before=0, space_after=24)
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Comparative Benchmarking of Supervised Classifiers and Interactive Decision-Support Dashboard")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(8, 127, 140)
    
    p_deg = doc.add_paragraph()
    format_paragraph(p_deg, space_before=12, space_after=16)
    p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_deg = p_deg.add_run("Submitted in partial fulfillment of the requirements for the degree of\nBachelor of Technology in Computer Science & Engineering")
    r_deg.font.name = "Calibri"
    r_deg.font.size = Pt(10)
    r_deg.font.color.rgb = RGBColor(71, 85, 105)
    
    # Metadata Table with Both Team Members
    sub_table = [
        ["Project Title:", "AQUANTIS: Water Quality Prediction Framework"],
        ["Team Members:", "1. Veer Singh (Roll No. 26)\n2. Parth Sarode (Roll No. 31)"],
        ["Course / Subject:", "Machine Learning Laboratory / Academic Project"],
        ["Under the Guidance of:", "[Faculty Mentor Name / Project Supervisor - To be confirmed]"],
        ["Academic Institution:", "[Department of Computer Science & Engineering, University Name - To be confirmed]"],
        ["Academic Year / Session:", "2025 – 2026"],
        ["Submission Date:", "October 2026"]
    ]
    add_table_data(doc, ["Project Attribute", "Candidate & Institutional Submission Details"], sub_table, col_widths=[2.3, 4.2])
    
    doc.add_page_break()
    
    # =========================================================================
    # 2. CERTIFICATE, DECLARATION, APPROVAL SHEET & ACKNOWLEDGEMENT
    # =========================================================================
    add_heading_1(doc, "Certificate of Originality")
    add_body_p(doc,
        "This is to certify that the project entitled \"AQUANTIS: A Machine Learning Framework for Water Quality Prediction\" "
        "submitted by Veer Singh (Roll No. 26) and Parth Sarode (Roll No. 31) in partial fulfillment of the requirements for the "
        "award of the degree of Bachelor of Technology in Computer Science and Engineering is an authentic record of bona fide work "
        "carried out by them under my supervision and guidance.")
    add_body_p(doc,
        "To the best of my knowledge and belief, the matter embodied in this project report has not been submitted to any other "
        "University or Institute for the award of any degree, diploma, or certificate.")
    
    sig_table = [
        ["\n\n___________________________\n[Faculty Mentor Name]\nProject Guide / Supervisor\nDepartment of CSE", 
         "\n\n___________________________\n[Head of Department]\nHead of the Department\nDepartment of CSE"]
    ]
    add_table_data(doc, ["Project Supervisor", "Department Authorization"], sig_table, col_widths=[3.25, 3.25])
    
    add_heading_1(doc, "Candidate Declaration")
    add_body_p(doc,
        "We hereby declare that this project report entitled \"AQUANTIS: A Machine Learning Framework for Water Quality Prediction\" "
        "is an authentic record of our own research and developmental work under the guidance of our faculty supervisor. "
        "We have strictly adhered to academic honesty and integrity standards. All literature, data sources, code libraries, "
        "and empirical benchmarks cited have been appropriately referenced and acknowledged.")
    add_body_p(doc,
        "We further confirm that the empirical machine learning models and experimental metrics reported herein reflect the actual "
        "test outputs of the pipeline on the Kaggle Water Potability benchmark and do not claim to provide regulatory drinking water safety certification.")
    
    cand_sig = [
        ["\n\n___________________________\nVeer Singh\nRoll No. 26\nB.Tech CSE, Final Year",
         "\n\n___________________________\nParth Sarode\nRoll No. 31\nB.Tech CSE, Final Year"]
    ]
    add_table_data(doc, ["Candidate 1", "Candidate 2"], cand_sig, col_widths=[3.25, 3.25])
    
    add_heading_1(doc, "Approval Sheet")
    add_body_p(doc,
        "This project report entitled \"AQUANTIS: A Machine Learning Framework for Water Quality Prediction\" by Veer Singh (Roll No. 26) "
        "and Parth Sarode (Roll No. 31) has been evaluated, approved, and accepted in partial fulfillment of the requirements for the "
        "degree of Bachelor of Technology in Computer Science and Engineering.")
    
    appr_table = [
        ["Internal Examiner:\n\nSignature: ______________________\nName: [Internal Examiner Name]\nDate: ____ / ____ / 2026",
         "External Examiner:\n\nSignature: ______________________\nName: [External Examiner Name]\nDate: ____ / ____ / 2026"]
    ]
    add_table_data(doc, ["Internal Examination Committee", "External Examination Committee"], appr_table, col_widths=[3.25, 3.25])
    
    add_heading_1(doc, "Acknowledgement")
    add_body_p(doc,
        "We express our profound gratitude to our project supervisor and faculty mentor for their valuable guidance, intellectual support, "
        "and continuous encouragement throughout the conceptualization, model development, and validation of the AQUANTIS framework.")
    add_body_p(doc,
        "We extend our sincere thanks to the Head of the Department and the faculty members of the Department of Computer Science and Engineering "
        "for providing the requisite laboratory facilities, computing infrastructure, and academic ecosystem. We are also grateful to the open-source "
        "scientific computing community—specifically the developers of Python, Scikit-learn, Pandas, NumPy, Matplotlib, and Streamlit—whose tools "
        "empowered this implementation.")
    
    doc.add_page_break()
    
    # =========================================================================
    # 3. PREFATORY TABLES (TOC, LIST OF FIGURES, LIST OF TABLES, ABBREVIATIONS)
    # =========================================================================
    add_heading_1(doc, "Table of Contents")
    toc_data = [
        ["1", "Abstract", "4"],
        ["2", "Introduction & Background", "5"],
        ["3", "Problem Statement & Objectives", "6"],
        ["4", "Literature Review & Research Gap", "7"],
        ["5", "Dataset Description & Exploratory Data Analysis", "9"],
        ["6", "Data Preprocessing & Leakage-Free Pipeline Architecture", "12"],
        ["7", "Machine Learning Classifiers & Mathematical Foundations", "14"],
        ["8", "Experimental Setup & Evaluation Protocol", "16"],
        ["9", "Empirical Results, Benchmarking & Discussion", "17"],
        ["10", "Confusion Matrix & ROC Curve Analysis", "19"],
        ["11", "Streamlit Decision-Support Dashboard Architecture", "21"],
        ["12", "System Testing, Verification & Validation", "24"],
        ["13", "Limitations, Ethical Considerations & Water Safety Disclaimer", "25"],
        ["14", "Conclusion & Future Research Scope", "26"],
        ["15", "References", "27"]
    ]
    add_table_data(doc, ["Section", "Chapter Title", "Page No."], toc_data, col_widths=[0.8, 4.7, 1.0])
    
    add_heading_2(doc, "List of Figures")
    lof_data = [
        ["Figure 1", "AQUANTIS End-to-End Methodological Workflow Diagram", "6"],
        ["Figure 2", "Four-Tier System Architecture and Leakage-Free Data Pipeline", "8"],
        ["Figure 3", "Target Potability Class Distribution in Benchmark Dataset (N = 3,276)", "10"],
        ["Figure 4", "Missing Value Incidence Across Nine Monitored Water Indicators", "10"],
        ["Figure 5", "Pairwise Pearson Correlation Matrix Between Indicators and Potability", "11"],
        ["Figure 6", "Comparative Classifier Performance on 20% Stratified Test Partition", "18"],
        ["Figure 7", "Confusion Matrices for SVM, Random Forest, Logistic Regression, and KNN", "20"],
        ["Figure 8", "Receiver Operating Characteristic (ROC) Discrimination Curves", "20"]
    ]
    add_table_data(doc, ["Figure No.", "Descriptive Caption", "Page No."], lof_data, col_widths=[1.1, 4.4, 1.0])
    
    add_heading_2(doc, "List of Tables")
    lot_data = [
        ["Table 1", "Candidate & Project Submission Metadata", "1"],
        ["Table 2", "Structured Literature Review of 2024–2025 Water Quality Studies", "7"],
        ["Table 3", "Physicochemical Water Indicators: Ranges, Means, Missingness & Standards", "9"],
        ["Table 4", "Empirical Classifier Benchmarks on Held-Out Test Set (N = 656)", "17"],
        ["Table 5", "Confusion Matrix Categorization and Error Breakdown", "19"],
        ["Table 6", "Streamlit Dashboard Modular Architectural Specification", "22"]
    ]
    add_table_data(doc, ["Table No.", "Descriptive Caption", "Page No."], lot_data, col_widths=[1.1, 4.4, 1.0])
    
    add_heading_2(doc, "List of Abbreviations")
    abbr_data = [
        ["AI", "Artificial Intelligence"],
        ["AUC", "Area Under the Curve"],
        ["CSV", "Comma-Separated Values"],
        ["EDA", "Exploratory Data Analysis"],
        ["EPA", "United States Environmental Protection Agency"],
        ["FN / FP", "False Negative / False Positive"],
        ["KNN", "K-Nearest Neighbors"],
        ["ML", "Machine Learning"],
        ["NTU", "Nephelometric Turbidity Units"],
        ["PCA", "Principal Component Analysis"],
        ["ppm", "Parts Per Million (mg/L)"],
        ["RBF", "Radial Basis Function"],
        ["RF", "Random Forest"],
        ["ROC", "Receiver Operating Characteristic"],
        ["SDG 6", "United Nations Sustainable Development Goal 6 (Clean Water and Sanitation)"],
        ["SVM", "Support Vector Machine"],
        ["TDS", "Total Dissolved Solids"],
        ["TN / TP", "True Negative / True Positive"],
        ["TOC", "Total Organic Carbon"],
        ["WHO", "World Health Organization"],
        ["XAI", "Explainable Artificial Intelligence"]
    ]
    add_table_data(doc, ["Abbreviation", "Complete Expanded Definition"], abbr_data, col_widths=[1.5, 5.0])
    
    doc.add_page_break()
    
    # =========================================================================
    # 4. ABSTRACT
    # =========================================================================
    add_heading_1(doc, "Abstract")
    add_body_p(doc,
        "Access to clean, potable drinking water is a fundamental pillar of global human welfare and disease prevention. "
        "Conventional physical, chemical, and microbiological water quality assessment methodologies necessitate substantial laboratory "
        "instrumentation, skilled analytical personnel, and considerable diagnostic turnaround delays. In decentralized and resource-constrained "
        "environments, computational machine learning models provide an effective automated preliminary screening mechanism by modeling complex "
        "interdependencies among routine physicochemical water parameters. This academic project presents AQUANTIS, an end-to-end Machine Learning "
        "framework for drinking water potability prediction developed by Veer Singh and Parth Sarode.")
    
    add_body_p(doc,
        "AQUANTIS is trained and evaluated on a curated benchmark dataset of 3,276 water samples comprising 9 continuous physicochemical "
        "indicators: pH, Hardness, Total Dissolved Solids, Chloramines, Sulfate, Conductivity, Total Organic Carbon, Trihalomethanes, and Turbidity. "
        "To rigorously eliminate data leakage, imputation and standardization transformations were strictly encapsulated inside scikit-learn Pipelines "
        "fitted solely on training partitions under a stratified 80/20 train/test split. Four diverse supervised classification architectures—Support "
        "Vector Machine (RBF kernel), Random Forest, Logistic Regression, and K-Nearest Neighbors—were benchmarked on a common held-out test partition "
        "(N = 656 samples). The Support Vector Machine demonstrated the most balanced trade-off between precision and recall, achieving the highest "
        "F1-score of 0.5118 (Accuracy = 62.20%, Precision = 0.5159, Recall = 0.5078, ROC-AUC = 0.6440). Random Forest achieved the highest overall "
        "Accuracy of 64.94% and peak ROC-AUC of 0.6597 (Precision = 0.5691, Recall = 0.4180). Logistic Regression (Accuracy = 52.44%, ROC-AUC = 0.5474) "
        "and KNN (Accuracy = 58.99%, ROC-AUC = 0.5972) highlighted the non-linear separability of the feature space.")
    
    add_body_p(doc,
        "A major contribution of this work is establishing the vital distinction between empirical pattern classification and official water potability "
        "certification: AQUANTIS predicts statistical dataset labels and explicitly does not certify physical bacteriological water safety. An interactive, "
        "full-featured Streamlit decision-support dashboard featuring telemetry KPI cards, interactive sample diagnostics, model comparison lab, dataset explorer, "
        "and session prediction audit logging was successfully developed and validated.")
    
    add_body_p(doc, "Machine Learning, Water Potability, Classification, Support Vector Machine, Random Forest, Data Leakage Prevention, Streamlit.", bold_prefix="Index Terms — ")
    
    # =========================================================================
    # 5. INTRODUCTION & PROBLEM DEFINITION
    # =========================================================================
    add_heading_1(doc, "1. Introduction")
    add_body_p(doc,
        "Safe drinking water is recognized under the United Nations Sustainable Development Goal 6 (SDG 6) as an indispensable prerequisite "
        "for human health and socioeconomic progress. Ingestion of contaminated water remains one of the primary vectors for acute waterborne "
        "pathologies—such as cholera, dysentery, and typhoid—as well as long-term physiological toxicities arising from chemical contaminants, "
        "heavy metals, and chlorination disinfection byproducts. While state municipal water treatment utilities enforce strict water testing "
        "protocols, continuous laboratory testing across dispersed rural, regional, and decentralized distribution networks remains economically "
        "and logistically prohibitive.")
    
    add_body_p(doc,
        "Recent advances in environmental data collection and supervised machine learning present an attractive complementary paradigm: rapid, "
        "data-driven preliminary screening. By taking multi-dimensional physicochemical water parameters that can be measured via routine sensory "
        "probes, computational classification algorithms can detect non-linear indicator patterns associated with contamination, prioritize samples "
        "for detailed laboratory assays, and support water management decisions.")
    
    add_heading_2(doc, "1.1 Problem Statement")
    add_body_p(doc,
        "Given a multi-dimensional feature vector X in R^9 representing continuous physicochemical water measurements (pH, Hardness, Solids, "
        "Chloramines, Sulfate, Conductivity, Organic Carbon, Trihalomethanes, and Turbidity), the primary computational objective is to develop and "
        "empirically benchmark a supervised binary classification function h(X) -> {0, 1} that maps these measurements to the target label Potability, "
        "where y = 1 represents potable (safe) water and y = 0 represents non-potable water, while handling significant missing observations and "
        "maintaining strict isolation against data leakage.")
    
    add_heading_2(doc, "1.2 Project Objectives")
    add_bullet(doc, "To implement an airtight, leakage-free data preprocessing pipeline encapsulating median imputation and standardization strictly within scikit-learn Pipelines.", bold_prefix="Objective 1 (Data Pipeline): ")
    add_bullet(doc, "To train, benchmark, and comparatively analyze four diverse supervised classifiers (SVM with RBF kernel, Random Forest, Logistic Regression, and KNN) on a common held-out test partition.", bold_prefix="Objective 2 (Model Benchmarking): ")
    add_bullet(doc, "To evaluate model performance holistically across multiple metrics (Accuracy, Precision, Recall, F1-Score, Confusion Matrices, and ROC-AUC) to address dataset class imbalance.", bold_prefix="Objective 3 (Multi-Metric Evaluation): ")
    add_bullet(doc, "To develop a responsive, telemetry-grade Streamlit web application providing interactive sample inference, dynamic probability visualization, dataset exploration, and session audit history.", bold_prefix="Objective 4 (Dashboard Deployment): ")
    add_bullet(doc, "To articulate the critical boundary between statistical dataset pattern recognition and regulatory water potability certification, promoting responsible AI deployment.", bold_prefix="Objective 5 (Responsible AI & Safety): ")
    
    add_heading_2(doc, "1.3 System Workflow")
    add_body_p(doc,
        "The overarching methodology of the AQUANTIS framework is illustrated in Figure 1. The workflow proceeds sequentially from raw data "
        "acquisition and integrity validation to stratified hold-out partitioning, isolated pipeline preprocessing, multi-model benchmarking, "
        "and interactive telemetry deployment.")
    
    add_figure_image(doc, "report/figures/fig_workflow.png", "Figure 1: AQUANTIS End-to-End Methodological Workflow Diagram.")
    
    # =========================================================================
    # 6. LITERATURE REVIEW & RESEARCH GAP
    # =========================================================================
    add_heading_1(doc, "2. Literature Review")
    add_body_p(doc,
        "To establish rigorous academic foundation, five recent peer-reviewed research papers (published between 2024 and 2025) "
        "investigating machine learning architectures for water quality assessment and potability prediction were systematically analyzed. "
        "Table 2 summarizes the comparative findings:")
    
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
    add_table_data(doc, ["Paper & Citation", "Title & DOI", "Dataset Used", "Methodology", "Key Verified Findings", "Relevance to AQUANTIS"], lit_table, col_widths=[1.1, 1.4, 0.9, 1.1, 1.2, 1.1])
    
    add_heading_2(doc, "2.1 Research Gap and Project Motivation")
    add_body_p(doc,
        "A critical analysis of existing literature reveals three prominent gaps in contemporary water quality ML implementations: "
        "First, many published studies report simple accuracy without examining precision, recall, and false negative rates, which are of paramount "
        "importance in public health applications. Second, numerous studies compute normalization statistics and imputation parameters over the entire "
        "dataset prior to partitioning, inadvertently introducing subtle data leakage that inflates reported performance. Third, existing models are "
        "rarely translated into interactive, transparent decision-support tools that provide prediction probabilities, feature explanations, and session "
        "audit logs. AQUANTIS directly bridges these gaps by enforcing strict pipeline encapsulation, comprehensive multi-metric benchmarking, and an "
        "interactive Streamlit telemetry dashboard.")
    
    # =========================================================================
    # 7. SYSTEM ARCHITECTURE & DATASET DESCRIPTION
    # =========================================================================
    add_heading_1(doc, "3. System Architecture & Dataset Description")
    add_body_p(doc,
        "The AQUANTIS architecture is structured into a four-tier hierarchical paradigm as illustrated in Figure 2. The four tiers ensure "
        "clean separation of concerns, reproducibility, and robust insulation against data leakage.")
    
    add_figure_image(doc, "report/figures/fig_architecture.png", "Figure 2: Four-Tier System Architecture and Leakage-Free Data Pipeline.")
    
    add_heading_2(doc, "3.1 Benchmark Dataset Description")
    add_body_p(doc,
        "The system utilizes the widely referenced Kaggle Water Potability benchmark dataset. The dataset comprises 3,276 water sample records, "
        "each described by 9 continuous physicochemical parameters and one binary target indicator (Potability). Table 3 provides the comprehensive "
        "statistical breakdown and regulatory context for each feature.")
    
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
    
    # =========================================================================
    # 8. EXPLORATORY DATA ANALYSIS (EDA)
    # =========================================================================
    add_heading_1(doc, "4. Exploratory Data Analysis")
    add_body_p(doc,
        "Rigorous exploratory analysis was performed across all 3,276 records to characterize class proportions, missing value distributions, "
        "and pairwise inter-feature correlations.")
    
    add_figure_image(doc, "report/figures/fig1_class_distribution.png", "Figure 3: Target Potability Class Distribution in Benchmark Dataset (N = 3,276).")
    
    add_body_p(doc,
        "Figure 3 depicts the distribution of the target variable. Out of 3,276 samples, 1,998 samples (60.99%) are labeled Non-Potable (Class 0), "
        "while 1,278 samples (39.01%) are labeled Potable (Class 1). This 61:39 imbalance indicates that a naive majority-class classifier would achieve "
        "approximately 61% accuracy without learning any actual predictive signals. Consequently, evaluation metrics such as Precision, Recall, "
        "F1-Score, and ROC-AUC are essential for objective evaluation.")
    
    add_figure_image(doc, "report/figures/fig2_missing_values.png", "Figure 4: Missing Value Incidence Across Nine Monitored Water Indicators.")
    
    add_body_p(doc,
        "Figure 4 summarizes missing value patterns across the 9 indicators. Missingness is concentrated in exactly three parameters: Sulfate is missing "
        "781 values (23.84%), pH is missing 491 values (14.99%), and Trihalomethanes is missing 162 values (4.95%). The remaining six indicators are "
        "completely observed. In total, 1,434 cells (4.87% of all matrix entries) contain null values. To preserve the dataset volume, median imputation "
        "was adopted.")
    
    add_figure_image(doc, "report/figures/fig6_correlation_heatmap.png", "Figure 5: Pairwise Pearson Correlation Matrix Between Indicators and Potability.")
    
    add_body_p(doc,
        "Figure 5 displays the pairwise Pearson correlation heatmap. A striking characteristic of the dataset is the near-total absence of linear "
        "correlation: correlation coefficients among features—and between each feature and the Potability target—range between -0.09 and +0.03. "
        "This confirms that no individual physical or chemical parameter serves as a direct linear predictor of potability, necessitating non-linear "
        "classifiers capable of mapping complex interaction hyper-surfaces.")
    
    # =========================================================================
    # 9. METHODOLOGY & LEAKAGE-FREE PIPELINE
    # =========================================================================
    add_heading_1(doc, "5. Methodology & Leakage-Free Pipeline Design")
    add_body_p(doc,
        "A critical vulnerability in applied machine learning is data leakage, where test partition information inadvertently leaks into "
        "training transformations. To establish an airtight experimental protocol, AQUANTIS implements scikit-learn Pipeline abstractions.")
    
    add_bullet(doc, "The dataset (N = 3,276) is partitioned into 80% training (2,620 samples) and 20% held-out test (656 samples) using stratified sampling with fixed random_state=42. The test partition remains completely untouched during model training.", bold_prefix="1. Stratified Partitioning: ")
    add_bullet(doc, "A SimpleImputer(strategy='median') calculates median values strictly from training features X_train and applies these learned medians to impute both X_train and X_test.", bold_prefix="2. Training-Isolated Imputation: ")
    add_bullet(doc, "For distance-sensitive and margin-based models (SVM, KNN, Logistic Regression), a StandardScaler() fits mean and standard deviation strictly on X_train. For Random Forest, scaling is omitted because decision tree split boundaries are invariant to monotonic scaling.", bold_prefix="3. Feature Standardization: ")
    add_bullet(doc, "Model fitting and hyperparameter binding occur strictly inside the pipeline, guaranteeing zero contamination between training and evaluation phases.", bold_prefix="4. Encapsulation: ")
    
    add_heading_2(doc, "5.1 Supervised Classifier Architectures")
    add_body_p(doc, "Four foundational algorithms representing distinct inductive biases were evaluated:", bold_prefix="Evaluated Models: ")
    add_bullet(doc, "Models the log-odds of potability as a linear combination of input indicators: logit(P(Y=1|X)) = w^T X + b. Optimized using the L-BFGS solver with balanced class weighting to penalize minority class errors.", bold_prefix="1. Logistic Regression: ")
    add_bullet(doc, "Non-parametric instance-based classifier assigning class labels based on majority vote of the k closest samples in standardized Euclidean space. In AQUANTIS, k = 7 nearest neighbors was utilized.", bold_prefix="2. K-Nearest Neighbors (KNN): ")
    add_bullet(doc, "Projects feature vectors into an infinite-dimensional Hilbert space via the Radial Basis Function (RBF) kernel: K(x_i, x_j) = exp(-gamma ||x_i - x_j||^2). Regularization C = 1.0 with balanced class weighting and Platt-scaled calibrated probabilities was configured.", bold_prefix="3. Support Vector Machine (SVM): ")
    add_bullet(doc, "Ensemble architecture constructing 300 de-correlated decision trees (n_estimators=300) with bootstrap aggregating and random feature subsets at each split. Majority voting determines predicted potability, while fractional vote shares provide class probabilities.", bold_prefix="4. Random Forest (RF): ")
    
    # =========================================================================
    # 10. EXPERIMENTAL RESULTS & BENCHMARKING
    # =========================================================================
    add_heading_1(doc, "6. Experimental Results & Model Benchmarking")
    add_body_p(doc,
        "All four classifiers were trained on the identical 2,620 training samples and evaluated on the common 656 held-out test samples. "
        "The empirical performance metrics, verified against the saved results/model_comparison.csv, are reported in Table 4 and Figure 6:")
    
    results_table = [
        ["Support Vector Machine", "0.6220 (62.20%)", "0.5159 (51.59%)", "0.5078 (50.78%)", "0.5118", "0.6440"],
        ["Random Forest", "0.6494 (64.94%)", "0.5691 (56.91%)", "0.4180 (41.80%)", "0.4820", "0.6597"],
        ["Logistic Regression", "0.5244 (52.44%)", "0.4146 (41.46%)", "0.5312 (53.12%)", "0.4658", "0.5474"],
        ["K-Nearest Neighbors", "0.5899 (58.99%)", "0.4581 (45.81%)", "0.2773 (27.73%)", "0.3455", "0.5972"]
    ]
    add_table_data(doc, ["Model Architecture", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"], results_table, col_widths=[1.8, 1.0, 1.0, 1.0, 1.0, 1.0])
    
    add_figure_image(doc, "report/figures/fig3_model_comparison.png", "Figure 6: Comparative Classifier Performance on 20% Stratified Test Partition.")
    
    add_heading_2(doc, "6.1 Analytical Findings and Trade-Off Analysis")
    add_bullet(doc,
        "Support Vector Machine achieved the highest F1-score (0.5118) with a well-balanced Precision (51.59%) and Recall (50.78%). "
        "By mapping features into high-dimensional space via the RBF kernel and applying balanced class weighting, SVM effectively balanced "
        "Type I and Type II errors.", bold_prefix="SVM Balanced Trade-Off: ")
    add_bullet(doc,
        "Random Forest achieved the highest Accuracy (64.94%), highest Precision (56.91%), and highest ROC-AUC (0.6597). "
        "However, its Recall was 41.80%, missing 149 of the 256 truly potable samples. It adopted a conservative prediction threshold, "
        "minimizing false alarms at the cost of higher false negatives.", bold_prefix="Random Forest Conservatism: ")
    add_bullet(doc,
        "Logistic Regression achieved only 52.44% Accuracy and 0.5474 ROC-AUC, confirming that linear hyperplanes cannot adequately separate "
        "potable from non-potable samples in this feature space.", bold_prefix="Linear Inseparability: ")
    add_bullet(doc,
        "KNN struggled severely with Recall (27.73%), missing 72.3% of potable samples. In a 9-dimensional space, metric distances become "
        "sparse (curse of dimensionality), causing minority class points to be dominated by majority non-potable neighbors.", bold_prefix="Curse of Dimensionality in KNN: ")
    
    # =========================================================================
    # 11. CONFUSION MATRIX & ROC CURVE ANALYSIS
    # =========================================================================
    add_heading_1(doc, "7. Confusion Matrix & ROC Curve Analysis")
    add_body_p(doc,
        "To inspect exact classification counts on the 656 held-out test samples (400 Non-Potable, 256 Potable), Table 5 presents the complete "
        "contingency breakdown, visualized in Figure 7:")
    
    cm_table = [
        ["Support Vector Machine", "278 (69.5%)", "122 (30.5%)", "126 (49.2%)", "130 (50.8%)"],
        ["Random Forest", "319 (79.8%)", "81 (20.2%)", "149 (58.2%)", "107 (41.8%)"],
        ["Logistic Regression", "208 (52.0%)", "192 (48.0%)", "120 (46.9%)", "136 (53.1%)"],
        ["K-Nearest Neighbors", "316 (79.0%)", "84 (21.0%)", "185 (72.3%)", "71 (27.7%)"]
    ]
    add_table_data(doc, ["Model Architecture", "True Negatives (TN)", "False Positives (FP)", "False Negatives (FN)", "True Positives (TP)"], cm_table, col_widths=[1.8, 1.2, 1.2, 1.2, 1.2])
    
    add_figure_image(doc, "report/figures/fig4_confusion_matrices.png", "Figure 7: Confusion Matrices for SVM, Random Forest, Logistic Regression, and KNN.")
    add_figure_image(doc, "report/figures/fig5_roc_curves.png", "Figure 8: Receiver Operating Characteristic (ROC) Discrimination Curves.")
    
    add_body_p(doc,
        "The ROC curves (Figure 8) illustrate the discrimination trajectories across all decision thresholds. Random Forest achieves the superior "
        "overall trajectory (AUC = 0.660), followed closely by Support Vector Machine (AUC = 0.644). K-Nearest Neighbors achieves AUC = 0.597, "
        "and Logistic Regression achieves AUC = 0.547. All models maintain trajectories strictly above the random guessing diagonal (AUC = 0.500), "
        "confirming genuine pattern extraction from the underlying indicators.")
    
    # =========================================================================
    # 12. APPLICATION INTERFACE & DEPLOYMENT
    # =========================================================================
    add_heading_1(doc, "8. Streamlit Application Architecture & User Interface")
    add_body_p(doc,
        "The AQUANTIS front-end is deployed as an interactive Streamlit web application. Designed under a modern dark environmental technology "
        "aesthetic (midnight navy background #060D17, surface containers #0C1827, and rich teal #0ED4BE accents), the platform provides five "
        "dedicated operational modules as detailed in Table 6:")
    
    ui_table = [
        ["Overview Tab", "Executive telemetry view featuring 5 KPI cards (Records: 3,276, Indicators: 9, Models: 4, Top F1 Model: SVM, Peak ROC-AUC: 0.660), horizontal benchmark chart, potability class balance chart, and system architecture summary."],
        ["Analyze Sample Tab", "Interactive diagnostic workspace organizing the 9 indicators into three scientific categories: Acidity & Disinfection (pH, Chloramines, Trihalomethanes), Mineral & Carbon (Hardness, Sulfate, TOC), and Physical & Clarity (Conductivity, Turbidity, TDS). Generates animated Potable/Non-Potable badge, confidence percentage, probability distribution bar chart, and safety disclaimers."],
        ["Model Lab Tab", "Diagnostic laboratory featuring interactive metric leaderboards, side-by-side confusion matrix heatmaps, multi-model ROC curve plots, detailed scikit-learn classification reports, and CSV metric downloads."],
        ["Data Explorer Tab", "Dataset exploration workspace providing kernel density distribution plots for any selected feature grouped by potability class, a missing value horizontal bar chart, a Pearson correlation matrix, and source dataset export."],
        ["Prediction History Tab", "Live session audit log recording every analysis conducted during the active session. Tracks timestamp, chosen model, predicted classification, potability probability, and all 9 input values with CSV audit export."]
    ]
    add_table_data(doc, ["Dashboard Tab / View", "Functional Capabilities & Technical Implementation"], ui_table, col_widths=[1.8, 4.7])
    
    add_callout(doc,
        "Local Application Deployment Instructions:\n"
        "1. Activate virtual environment: .\\.venv\\Scripts\\Activate.ps1\n"
        "2. Launch Streamlit server: streamlit run app.py\n"
        "3. Access web dashboard: Navigate to http://localhost:8501 in any modern browser.",
        "How to Run the AQUANTIS Platform")
    
    # =========================================================================
    # 13. SYSTEM TESTING AND VALIDATION
    # =========================================================================
    add_heading_1(doc, "9. System Testing and Validation")
    add_body_p(doc,
        "Comprehensive software verification and pipeline testing was conducted across all components of AQUANTIS:")
    add_bullet(doc, "Static syntax compilation via python -m py_compile app.py confirmed zero syntax, indentation, or module-level defects.", bold_prefix="1. Static Syntax Verification: ")
    add_bullet(doc, "Integration tests confirmed that train_and_evaluate() reliably loads data, executes the stratified 80/20 split, fits all four pipelines, and serializes aquantis_bundle.joblib without data leakage.", bold_prefix="2. Pipeline Integration Testing: ")
    add_bullet(doc, "Matplotlib figure generation using clear_figure=True and explicit Agg canvas management confirmed that all visual artifacts render cleanly without memory leaks or backend errors.", bold_prefix="3. Graphic Rendering Verification: ")
    add_bullet(doc, "Local HTTP testing confirmed that the Streamlit server boots and serves HTTP 200 responses reliably on port 8501.", bold_prefix="4. HTTP Server Verification: ")
    
    # =========================================================================
    # 14. LIMITATIONS & WATER SAFETY DISCLAIMER
    # =========================================================================
    add_heading_1(doc, "10. Limitations & Water Safety Disclaimer")
    add_callout(doc,
        "CRITICAL OPERATIONAL & REGULATORY DISCLAIMER:\n"
        "AQUANTIS is an academic research and educational decision-support prototype. Machine learning algorithms identify statistical "
        "correlations within historical benchmark datasets; they do NOT certify that water is physically safe or potable to drink.\n\n"
        "Real-world drinking water potability legally requires certified chemical and microbiological laboratory assays (such as EPA/WHO "
        "bacteriological pathogen testing, heavy metal mass spectrometry, and viral screening). Automated predictions must never be used as a "
        "substitute for certified laboratory testing in public drinking water management.",
        "Mandatory Water Safety Disclaimer")
    
    add_bullet(doc, "The Kaggle Water Potability dataset is an aggregated historical benchmark that does not account for local seasonal hydrology, specific geographic watersheds, or acute upstream industrial contamination events.", bold_prefix="1. Benchmark Dataset Limitations: ")
    add_bullet(doc, "Approximately 23.8% of Sulfate and 15.0% of pH readings were imputed using median baseline values. While statistically robust, imputation does not reconstruct unobserved real-world fluctuations.", bold_prefix="2. Imputation Approximations: ")
    add_bullet(doc, "Predicted model probabilities reflect distance from training hyperplanes rather than calibrated physical risk probabilities.", bold_prefix="3. Probability Calibration: ")
    
    # =========================================================
    # 15. CONCLUSION & FUTURE SCOPE
    # =========================================================
    add_heading_1(doc, "11. Conclusion & Future Research Scope")
    add_body_p(doc,
        "The AQUANTIS project successfully designed, empirically validated, and deployed an end-to-end machine learning framework for "
        "water quality potability prediction. By evaluating four foundational classifiers on a common held-out test split (N = 656), the study "
        "demonstrated that non-linear kernel and ensemble architectures significantly outperform linear baselines. Support Vector Machine "
        "achieved the most balanced precision-recall performance (F1 = 0.5118), while Random Forest delivered the highest overall accuracy (64.94%) "
        "and peak ROC-AUC (0.6597). Strict pipeline encapsulation prevented data leakage, and the interactive Streamlit telemetry dashboard provides "
        "a transparent, defense-ready platform.")
    
    add_heading_2(doc, "11.1 Future Enhancements")
    add_bullet(doc, "Implementing SMOTE oversampling and Optuna Bayesian optimization to enhance Random Forest recall and F1-score.", bold_prefix="1. Resampling & Bayesian Optimization: ")
    add_bullet(doc, "Constructing a weighted soft-voting ensemble combining Random Forest and RBF SVM probabilities to maximize AUC-ROC.", bold_prefix="2. Ensemble Stacking: ")
    add_bullet(doc, "Quantizing trained pipeline weights into TinyML models for low-power edge microcontrollers (ESP32/ARM Cortex) paired with physical IoT sensors.", bold_prefix="3. Edge IoT Deployment: ")
    add_bullet(doc, "Integrating SHAP (SHapley Additive exPlanations) to provide local feature attributions for individual sample predictions.", bold_prefix="4. Explainable AI (XAI): ")
    
    # =========================================================
    # 16. REFERENCES
    # =========================================================
    add_heading_1(doc, "12. References")
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
    for r in refs:
        p_ref = doc.add_paragraph()
        format_paragraph(p_ref, space_before=2, space_after=4, line_spacing=1.15)
        run_ref = p_ref.add_run(r)
        run_ref.font.name = "Calibri"
        run_ref.font.size = Pt(9.5)
        run_ref.font.color.rgb = RGBColor(30, 41, 59)
        
    # Save the output DOCX files
    docx_path = Path("AQUANTIS_Final_Idea_Lab_Report.docx")
    doc.save(docx_path)
    print(f"Report DOCX saved to: {docx_path.resolve()}")
    
    # Also save a copy inside report/ directory
    doc.save(Path("report") / "AQUANTIS_Final_Idea_Lab_Report.docx")

if __name__ == "__main__":
    build_aquantis_final_report()
