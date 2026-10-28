from pathlib import Path
import urllib.request
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report, roc_curve
)
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import joblib

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
MODEL_DIR = ROOT / "models"
RESULTS_DIR = ROOT / "results"
DATA_PATH = DATA_DIR / "water_potability.csv"
DATA_URL = "https://raw.githubusercontent.com/krishnaik06/5th-Aug-2020-Kaggle-Competitions-/master/water_potability.csv"
TARGET = "Potability"
FEATURES = [
    "ph", "Hardness", "Solids", "Chloramines", "Sulfate",
    "Conductivity", "Organic_carbon", "Trihalomethanes", "Turbidity"
]

def ensure_dirs():
    for path in (DATA_DIR, MODEL_DIR, RESULTS_DIR):
        path.mkdir(parents=True, exist_ok=True)

def load_data(download=True):
    ensure_dirs()
    if not DATA_PATH.exists() and download:
        try:
            urllib.request.urlretrieve(DATA_URL, DATA_PATH)
        except Exception as exc:
            raise RuntimeError(
                "Could not download the dataset. Download a verified Water Potability "
                "CSV and save it as data/water_potability.csv. See README.md."
            ) from exc
    if not DATA_PATH.exists():
        raise FileNotFoundError("Dataset missing: data/water_potability.csv")
    df = pd.read_csv(DATA_PATH)
    missing = set(FEATURES + [TARGET]) - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing expected columns: {sorted(missing)}")
    df = df[FEATURES + [TARGET]].copy()
    df = df.dropna(subset=[TARGET])
    df[TARGET] = pd.to_numeric(df[TARGET], errors="coerce")
    df = df.dropna(subset=[TARGET])
    df = df[df[TARGET].isin([0, 1])]
    for col in FEATURES:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def build_models():
    scaled = lambda estimator: Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("model", estimator),
    ])
    return {
        "Logistic Regression": scaled(LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)),
        "K-Nearest Neighbors": scaled(KNeighborsClassifier(n_neighbors=7)),
        "Support Vector Machine": scaled(SVC(C=1.0, kernel="rbf", probability=True, class_weight="balanced", random_state=42)),
        "Random Forest": Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("model", RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=42, n_jobs=-1)),
        ]),
    }

def train_and_evaluate(df=None):
    ensure_dirs()
    df = load_data() if df is None else df.copy()
    X, y = df[FEATURES], df[TARGET].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    metrics, fitted, details = [], {}, {}
    for name, model in build_models().items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None
        row = {
            "Model": name,
            "Accuracy": accuracy_score(y_test, pred),
            "Precision": precision_score(y_test, pred, zero_division=0),
            "Recall": recall_score(y_test, pred, zero_division=0),
            "F1-score": f1_score(y_test, pred, zero_division=0),
            "ROC-AUC": roc_auc_score(y_test, proba) if proba is not None else np.nan,
        }
        metrics.append(row)
        fitted[name] = model
        details[name] = {
            "confusion_matrix": confusion_matrix(y_test, pred),
            "report": classification_report(y_test, pred, zero_division=0),
            "y_test": y_test.to_numpy(),
            "probabilities": proba,
        }
    result = pd.DataFrame(metrics).sort_values("F1-score", ascending=False)
    result.to_csv(RESULTS_DIR / "model_comparison.csv", index=False)
    for name, model in fitted.items():
        safe = name.lower().replace(" ", "_").replace("-", "")
        joblib.dump(model, MODEL_DIR / f"{safe}.joblib")
    joblib.dump({"features": FEATURES, "models": fitted, "metrics": result}, MODEL_DIR / "aquantis_bundle.joblib")
    return result, fitted, details, (X_train, X_test, y_train, y_test)
