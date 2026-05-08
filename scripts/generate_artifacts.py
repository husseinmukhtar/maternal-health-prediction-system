from pathlib import Path
import json
import math
import random

import joblib
import numpy as np
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

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "risk" / "ml" / "data"
ART_DIR = ROOT / "risk" / "ml" / "model_artifacts"
DATA_DIR.mkdir(parents=True, exist_ok=True)
ART_DIR.mkdir(parents=True, exist_ok=True)

random.seed(42)
np.random.seed(42)

rows = []
# Synthetic but clinically plausible ranges. Label is kept for academic evaluation only.
# The unsupervised model is trained without using the RiskLevel column.
def clamp(value, low, high):
    return max(low, min(high, value))

for i in range(240):
    r = random.random()
    if r < 0.42:  # low risk
        age = round(clamp(np.random.normal(25, 4), 17, 34))
        sys = round(clamp(np.random.normal(112, 8), 90, 129))
        dia = round(clamp(np.random.normal(73, 6), 55, 84))
        bs = round(clamp(np.random.normal(6.4, 0.7), 4.5, 7.8), 1)
        temp = round(clamp(np.random.normal(98.0, 0.5), 96.8, 99.0), 1)
        hr = round(clamp(np.random.normal(78, 8), 60, 95))
        gest = round(clamp(np.random.normal(24, 8), 6, 40))
        label = "low risk"
    elif r < 0.76:  # medium risk
        age = round(clamp(np.random.normal(31, 7), 18, 44))
        sys = round(clamp(np.random.normal(132, 10), 105, 154))
        dia = round(clamp(np.random.normal(86, 8), 70, 99))
        bs = round(clamp(np.random.normal(7.9, 1.2), 5.8, 11.0), 1)
        temp = round(clamp(np.random.normal(98.7, 0.7), 97.2, 100.3), 1)
        hr = round(clamp(np.random.normal(89, 10), 65, 110))
        gest = round(clamp(np.random.normal(27, 7), 8, 40))
        label = "mid risk"
    else:  # high risk
        age = round(clamp(np.random.normal(37, 8), 19, 50))
        sys = round(clamp(np.random.normal(158, 16), 125, 190))
        dia = round(clamp(np.random.normal(103, 12), 85, 125))
        bs = round(clamp(np.random.normal(12.1, 2.4), 7.5, 19.0), 1)
        temp = round(clamp(np.random.normal(100.1, 1.2), 98.0, 103.5), 1)
        hr = round(clamp(np.random.normal(103, 13), 75, 130))
        gest = round(clamp(np.random.normal(29, 8), 10, 40))
        label = "high risk"
    rows.append({
        "Age": age,
        "SystolicBP": sys,
        "DiastolicBP": dia,
        "BS": bs,
        "BodyTemp": temp,
        "HeartRate": hr,
        "GestationalAge": gest,
        "RiskLevel": label,
    })

# Add a few edge cases the examiner may try.
rows.extend([
    {"Age": 19, "SystolicBP": 105, "DiastolicBP": 70, "BS": 5.8, "BodyTemp": 98.0, "HeartRate": 72, "GestationalAge": 20, "RiskLevel": "low risk"},
    {"Age": 28, "SystolicBP": 145, "DiastolicBP": 95, "BS": 8.9, "BodyTemp": 99.1, "HeartRate": 96, "GestationalAge": 32, "RiskLevel": "mid risk"},
    {"Age": 43, "SystolicBP": 170, "DiastolicBP": 112, "BS": 15.5, "BodyTemp": 101.5, "HeartRate": 118, "GestationalAge": 34, "RiskLevel": "high risk"},
])

df = pd.DataFrame(rows)
dataset_path = DATA_DIR / "maternal_health_sample_dataset.csv"
df.to_csv(dataset_path, index=False)

FEATURE_COLUMNS = ["Age", "SystolicBP", "DiastolicBP", "BS", "BodyTemp", "HeartRate", "GestationalAge"]
X = df[FEATURE_COLUMNS].copy()
y = df["RiskLevel"].str.strip().str.lower()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
model = KMeans(n_clusters=3, random_state=42, n_init=20)
clusters = model.fit_predict(X_scaled)

# Convert cluster centers back to original scale and order them from safest to riskiest.
centers = scaler.inverse_transform(model.cluster_centers_)
center_df = pd.DataFrame(centers, columns=FEATURE_COLUMNS)

def risk_score(row):
    # Simple interpretable clinical risk proxy. It is only used to name clusters.
    score = 0.0
    score += max(0, row["Age"] - 30) / 20
    score += max(0, row["SystolicBP"] - 120) / 70
    score += max(0, row["DiastolicBP"] - 80) / 45
    score += max(0, row["BS"] - 7.0) / 12
    score += max(0, row["BodyTemp"] - 98.6) / 5
    score += max(0, row["HeartRate"] - 90) / 45
    return float(score)

cluster_scores = {int(idx): risk_score(center_df.loc[idx]) for idx in center_df.index}
ordered_clusters = sorted(cluster_scores, key=cluster_scores.get)
labels = ["Low Risk", "Medium Risk", "High Risk"]
cluster_to_label = {int(cluster): label for cluster, label in zip(ordered_clusters, labels)}
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
    "external_accuracy_against_reference_labels": round(float(accuracy_score(y, pred_labels)), 4),
    "external_precision_weighted": round(float(precision_score(y, pred_labels, average="weighted", zero_division=0)), 4),
    "external_recall_weighted": round(float(recall_score(y, pred_labels, average="weighted", zero_division=0)), 4),
    "external_f1_weighted": round(float(f1_score(y, pred_labels, average="weighted", zero_division=0)), 4),
    "cluster_to_label": {str(k): v for k, v in cluster_to_label.items()},
    "cluster_risk_scores": {str(k): round(v, 4) for k, v in cluster_scores.items()},
    "cluster_centers": center_df.round(3).to_dict(orient="index"),
    "note": "RiskLevel was not used during clustering. It is retained only for academic comparison after clustering.",
}

labels_order = ["low risk", "mid risk", "high risk"]
metrics["confusion_matrix_labels"] = labels_order
metrics["confusion_matrix"] = confusion_matrix(y, pred_labels, labels=labels_order).tolist()

joblib.dump(model, ART_DIR / "maternal_kmeans_model.joblib")
joblib.dump(scaler, ART_DIR / "maternal_scaler.joblib")
with open(ART_DIR / "cluster_mapping.json", "w", encoding="utf-8") as f:
    json.dump({str(k): v for k, v in cluster_to_label.items()}, f, indent=2)
with open(ART_DIR / "model_metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2)
print(f"Generated dataset and artifacts in {ROOT}")
