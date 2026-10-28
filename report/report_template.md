# AQUANTIS: A Machine Learning Framework for Water Quality Prediction

> Replace bracketed prompts with verified information from your run. Do not submit unfilled prompts or invented research citations.

## Abstract
[Summarize the problem, dataset source and size, four models, evaluation protocol, actual best model and measured results. Avoid claiming water safety certification.]

## 1. Introduction
Explain why water-quality monitoring matters and define the limited scope of predicting the dataset's Potability label.

## 2. Problem Statement and Objectives
- Predict the source dataset's binary Potability label from nine measured features.
- Compare four classification models using a common test set.
- Provide an interactive dashboard for exploration and demonstration.

## 3. Literature Review
Discuss at least five genuine recent research papers relevant to water-quality prediction, water potability, or ML-based water-quality classification. For each: citation, objective, dataset, method, reported findings, limitations, and relevance to AQUANTIS. Verify every citation and reported number from the paper itself.

| Paper | Year | Dataset | Method | Findings (verified) | Limitation / relevance |
|---|---:|---|---|---|---|
| [Paper 1] | | | | | |
| [Paper 2] | | | | | |
| [Paper 3] | | | | | |
| [Paper 4] | | | | | |
| [Paper 5] | | | | | |

## 4. Dataset and Preprocessing
Document the exact dataset source, download date, license, row/column count, target distribution, units if documented, missing-value counts, and any invalid records. The pipeline uses median imputation; scaling is applied to Logistic Regression, KNN, and SVM. Imputation/scaling are fitted on training data only.

## 5. Methodology
Describe the stratified 80/20 train/test split with random seed 42. Explain Logistic Regression, KNN, RBF SVM, and Random Forest in your own words. Include a workflow diagram.

## 6. Experimental Setup and Metrics
Report Python and library versions, split strategy, class distribution, and metrics. Define accuracy, precision, recall, F1-score, and ROC-AUC. Explain that all models use the same held-out test rows.

## 7. Results and Discussion
Insert the actual `results/model_comparison.csv` table and generated figures. Discuss tradeoffs, class imbalance, potential overfitting, and why accuracy alone is insufficient. Do not assert that the best test-set model generalizes to all locations.

## 8. User Interface and Deployment
Add screenshots of Overview, Predict, Model Lab, Data Explorer, and Prediction History. Explain how to run `streamlit run app.py`.

## 9. Limitations and Responsible Use
The dataset may not represent local water sources, collection methods, seasons, or all regulatory limits. Dataset labels are not a substitute for laboratory tests. Prediction probabilities are not calibrated safety guarantees.

## 10. Conclusion and Future Work
Summarize measured findings and propose external validation, more representative data, calibration, and integration with certified lab results.

## References
[At least five verified research papers plus dataset and software references. Use the citation style specified by your faculty.]
