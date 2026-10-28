# AQUANTIS Viva Preparation

1. **What is the problem statement?** Predict the Potability label in a public water-quality dataset from nine numerical measurements.
2. **Is this a water-safety certification system?** No. It predicts a dataset label and cannot replace laboratory testing or regulatory assessment.
3. **Why compare four models?** To compare different inductive biases under the same evaluation protocol.
4. **Why use a train/test split?** To estimate performance on held-out samples rather than evaluating only on training data.
5. **Why stratify the split?** To preserve approximately the same class proportions in training and test sets.
6. **What is data leakage?** Information from test data influencing training or preprocessing. Pipelines fit imputation and scaling on training data only.
7. **Why median imputation?** It is a simple robust baseline for missing numerical values. It does not prove missingness is harmless.
8. **Why scale features?** KNN, SVM, and Logistic Regression can be sensitive to feature scales.
9. **Why does Random Forest not use StandardScaler here?** Tree splits are generally insensitive to monotonic feature scaling.
10. **What does precision mean?** Of samples predicted positive, the proportion that are actually positive.
11. **What does recall mean?** Of actual positive samples, the proportion correctly identified.
12. **Why F1-score?** It combines precision and recall via their harmonic mean.
13. **What does ROC-AUC measure?** Ranking discrimination across classification thresholds, when probabilities/scores are available.
14. **Why can accuracy be misleading?** It can hide poor performance on a minority class.
15. **What are limitations?** Dataset representativeness, missing values, potential label limitations, and lack of external validation.
16. **How can it be improved?** Use independently collected representative samples, validate externally, tune hyperparameters without test leakage, and assess calibration and fairness across source conditions.
