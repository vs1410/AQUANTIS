# AQUANTIS Project Report: Pre-Submission Verification & Viva Checklist

Before final physical or digital submission to your academic department or examination committee, verify and customize the bracketed placeholders listed below.

---

## 1. Candidate & Institutional Placeholders (To Fill in the DOCX)

Open [`report/AQUANTIS_Academic_Project_Report.docx`](file:///c:/Users/veers/OneDrive/Desktop/Projects/ML/AQUANTIS_r/report/AQUANTIS_Academic_Project_Report.docx) in Microsoft Word and customize the title page table:

| Field | Current Placeholder in Document | Required Value |
|---|---|---|
| **Student Name(s)** | `[Student Name - e.g., Veer S. & Project Partner]` | Your full name and partner's name (if team project) |
| **University Roll No.** | `[University Roll Number / Registration ID]` | Your official University / College Roll Number |
| **Faculty Mentor** | `[Faculty Mentor Name / Project Supervisor]` | Professor / Assistant Professor guiding your lab |
| **Department / College** | `[Department of Computer Science & Engineering, University Name]` | Full official name of your College / University |
| **Academic Year** | `2025 – 2026` | Academic session / Semester (e.g., 6th Sem / 2025–26) |

---

## 2. Report Artifacts Generated

All artifacts have been compiled and verified in the [`report/`](file:///c:/Users/veers/OneDrive/Desktop/Projects/ML/AQUANTIS_r/report/) directory:

1. **Complete Editable Word Document**:  
   [`report/AQUANTIS_Academic_Project_Report.docx`](file:///c:/Users/veers/OneDrive/Desktop/Projects/ML/AQUANTIS_r/report/AQUANTIS_Academic_Project_Report.docx)  
   *Includes full academic sections, embedded high-resolution figures, styled data tables, mathematical definitions, and verified 2024–2025 IEEE/Elsevier references.*

2. **Full Matching PDF Document**:  
   [`report/AQUANTIS_Academic_Project_Report.pdf`](file:///c:/Users/veers/OneDrive/Desktop/Projects/ML/AQUANTIS_r/report/AQUANTIS_Academic_Project_Report.pdf)  
   *(1.09 MB – formatted with 1-inch margins, running headers/footers, and clean vector typography).*

3. **High-Resolution Vector / 300 DPI Publication Figures**:  
   * [`report/figures/fig1_class_distribution.png`](file:///c:/Users/veers/OneDrive/Desktop/Projects/ML/AQUANTIS_r/report/figures/fig1_class_distribution.png)
   * [`report/figures/fig2_missing_values.png`](file:///c:/Users/veers/OneDrive/Desktop/Projects/ML/AQUANTIS_r/report/figures/fig2_missing_values.png)
   * [`report/figures/fig3_model_comparison.png`](file:///c:/Users/veers/OneDrive/Desktop/Projects/ML/AQUANTIS_r/report/figures/fig3_model_comparison.png)
   * [`report/figures/fig4_confusion_matrices.png`](file:///c:/Users/veers/OneDrive/Desktop/Projects/ML/AQUANTIS_r/report/figures/fig4_confusion_matrices.png)
   * [`report/figures/fig5_roc_curves.png`](file:///c:/Users/veers/OneDrive/Desktop/Projects/ML/AQUANTIS_r/report/figures/fig5_roc_curves.png)
   * [`report/figures/fig6_correlation_heatmap.png`](file:///c:/Users/veers/OneDrive/Desktop/Projects/ML/AQUANTIS_r/report/figures/fig6_correlation_heatmap.png)

4. **Screenshot Evidence Checklist**:  
   [`report/screenshot_guide.md`](file:///c:/Users/veers/OneDrive/Desktop/Projects/ML/AQUANTIS_r/report/screenshot_guide.md)

---

## 3. Key Viva Defense Cheat-Sheet

* **Q: Why did Support Vector Machine have a lower accuracy than Random Forest, but you rank it highest by F1-Score?**  
  * **A:** *The dataset has class imbalance (61% non-potable, 39% potable). Random Forest achieved 64.9% accuracy by being conservative on the positive class (Recall = 41.8%, missing 149 potable samples). SVM with RBF kernel and balanced class weighting achieved a balanced 50.8% recall and 51.6% precision, yielding the highest F1-score of 0.5118.*

* **Q: How did you ensure there was no data leakage during imputation and scaling?**  
  * **A:** *We implemented scikit-learn `Pipeline` objects. The stratified 80/20 train/test split was created first. Imputation medians and `StandardScaler` mean/variance parameters were computed strictly on the training set (`X_train`) during `fit()`, and only applied via `transform()` to the held-out test set (`X_test`).*

* **Q: Why was `StandardScaler` omitted from the Random Forest pipeline?**  
  * **A:** *Tree-based ensemble models make orthogonal splits based on individual feature thresholds. Because decision tree partitions are invariant to monotonic feature scaling, standardization has no mathematical effect on decision boundaries and was omitted to preserve original feature interpretability.*
