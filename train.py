import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve
from src.aquantis import load_data, train_and_evaluate, RESULTS_DIR, FEATURES, TARGET

def main():
    df = load_data()
    results, models, details, split = train_and_evaluate(df)
    X_train, X_test, y_train, y_test = split

    print("\nDataset shape:", df.shape)
    print("Target distribution:\n", df[TARGET].value_counts().sort_index())
    print("\nMissing values:\n", df.isna().sum())
    print("\nHeld-out test results:\n", results.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    plt.figure(figsize=(10, 5))
    plot_df = results.set_index("Model")[["Accuracy", "Precision", "Recall", "F1-score"]]
    plot_df.plot(kind="bar", ylim=(0, 1), figsize=(11, 5))
    plt.title("AQUANTIS: Model Performance on the Same Test Set")
    plt.ylabel("Score")
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "model_comparison.png", dpi=160)
    plt.close()

    for name, detail in details.items():
        safe = name.lower().replace(" ", "_").replace("-", "")
        plt.figure(figsize=(5, 4))
        sns.heatmap(detail["confusion_matrix"], annot=True, fmt="d", cmap="Blues",
                    xticklabels=["Predicted 0", "Predicted 1"],
                    yticklabels=["Actual 0", "Actual 1"])
        plt.title(f"Confusion Matrix: {name}")
        plt.tight_layout()
        plt.savefig(RESULTS_DIR / f"confusion_matrix_{safe}.png", dpi=150)
        plt.close()

    plt.figure(figsize=(7, 5))
    for name, detail in details.items():
        if detail["probabilities"] is not None:
            from sklearn.metrics import roc_curve, roc_auc_score
            fpr, tpr, _ = roc_curve(detail["y_test"], detail["probabilities"])
            auc = roc_auc_score(detail["y_test"], detail["probabilities"])
            plt.plot(fpr, tpr, label=f"{name} (AUC={auc:.3f})")
    plt.plot([0, 1], [0, 1], linestyle="--", label="Random baseline")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curves on Held-Out Test Set")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "roc_curves.png", dpi=160)
    plt.close()
    print(f"\nSaved metrics and figures to: {RESULTS_DIR}")

if __name__ == "__main__":
    main()
