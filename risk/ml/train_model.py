"""Train the unsupervised K-Means model for maternal health risk grouping."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

import joblib
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import (
    accuracy_score,
    calinski_harabasz_score,
    confusion_matrix,
    davies_bouldin_score,
    f1_score,
    precision_score,
    recall_score,
    silhouette_score,
)
from sklearn.preprocessing import StandardScaler

FEATURE_COLUMNS = ["Age", "SystolicBP", "DiastolicBP", "BS", "BodyTemp", "HeartRate", "GestationalAge"]
RISK_LABELS = ["Low Risk", "Medium Risk", "High Risk"]
REFERENCE_LABELS = ["low risk", "mid risk", "high risk"]

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "data" / "maternal_health_sample_dataset.csv"
ARTIFACT_DIR = BASE_DIR / "model_artifacts"


def _risk_score(row: pd.Series) -> float:
    score = 0.0
    score += max(0, row["Age"] - 30) / 20
    score += max(0, row["SystolicBP"] - 120) / 70
    score += max(0, row["DiastolicBP"] - 80) / 45
    score += max(0, row["BS"] - 7.0) / 12
    score += max(0, row["BodyTemp"] - 98.6) / 5
    score += max(0, row["HeartRate"] - 90) / 45
    return float(score)


def train_model(dataset_path: Path = DATASET_PATH) -> Dict:
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(dataset_path)
    missing_columns = [column for column in FEATURE_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError("Missing required dataset column(s): " + ", ".join(missing_columns))

    X = df[FEATURE_COLUMNS].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(n_clusters=3, random_state=42, n_init=20)
    clusters = model.fit_predict(X_scaled)

    centers = scaler.inverse_transform(model.cluster_centers_)
    center_df = pd.DataFrame(centers, columns=FEATURE_COLUMNS)
    cluster_scores = {int(idx): _risk_score(center_df.loc[idx]) for idx in center_df.index}
    ordered_clusters = sorted(cluster_scores, key=cluster_scores.get)
    cluster_to_label = {int(cluster): label for cluster, label in zip(ordered_clusters, RISK_LABELS)}

    pred_labels = pd.Series(clusters).map(cluster_to_label).str.lower().str.replace("medium", "mid", regex=False)

    metrics = {
        "model_type": "K-Means Clustering",
        "learning_type": "Unsupervised Learning",
        "feature_columns": FEATURE_COLUMNS,
        "n_clusters": 3,
        "records_used": int(len(df)),
        "silhouette_score": round(float(silhouette_score(X_scaled, clusters)), 4),
        "davies_bouldin_index": round(float(davies_bouldin_score(X_scaled, clusters)), 4),
        "calinski_harabasz_score": round(float(calinski_harabasz_score(X_scaled, clusters)), 4),
        "cluster_to_label": {str(k): v for k, v in cluster_to_label.items()},
        "cluster_risk_scores": {str(k): round(v, 4) for k, v in cluster_scores.items()},
        "cluster_centers": center_df.round(3).to_dict(orient="index"),
        "note": "RiskLevel is not used during clustering. It is used only for post-clustering academic comparison.",
    }

    if "RiskLevel" in df.columns:
        y = df["RiskLevel"].astype(str).str.strip().str.lower()
        metrics.update({
            "external_accuracy_against_reference_labels": round(float(accuracy_score(y, pred_labels)), 4),
            "external_precision_weighted": round(float(precision_score(y, pred_labels, average="weighted", zero_division=0)), 4),
            "external_recall_weighted": round(float(recall_score(y, pred_labels, average="weighted", zero_division=0)), 4),
            "external_f1_weighted": round(float(f1_score(y, pred_labels, average="weighted", zero_division=0)), 4),
            "confusion_matrix_labels": REFERENCE_LABELS,
            "confusion_matrix": confusion_matrix(y, pred_labels, labels=REFERENCE_LABELS).tolist(),
        })

    joblib.dump(model, ARTIFACT_DIR / "maternal_kmeans_model.joblib")
    joblib.dump(scaler, ARTIFACT_DIR / "maternal_scaler.joblib")
    with open(ARTIFACT_DIR / "cluster_mapping.json", "w", encoding="utf-8") as file:
        json.dump({str(k): v for k, v in cluster_to_label.items()}, file, indent=2)
    with open(ARTIFACT_DIR / "model_metrics.json", "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)

    return metrics


if __name__ == "__main__":
    result = train_model()
    print(json.dumps(result, indent=2))
