"""Prediction utilities for the Maternal Health Risk Prediction System.

The core model is K-Means clustering. It is unsupervised because the model is
trained using only numerical maternal health indicators. The original risk labels
in the dataset are used only after clustering for academic comparison.
"""
from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from typing import Dict, Iterable, Tuple

import joblib
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
ARTIFACT_DIR = BASE_DIR / "model_artifacts"
MODEL_PATH = ARTIFACT_DIR / "maternal_kmeans_model.joblib"
SCALER_PATH = ARTIFACT_DIR / "maternal_scaler.joblib"
MAPPING_PATH = ARTIFACT_DIR / "cluster_mapping.json"
METRICS_PATH = ARTIFACT_DIR / "model_metrics.json"

FEATURE_COLUMNS = [
    "Age",
    "SystolicBP",
    "DiastolicBP",
    "BS",
    "BodyTemp",
    "HeartRate",
    "GestationalAge",
]

RECOMMENDATIONS = {
    "Low Risk": "Continue routine antenatal care, maintain healthy nutrition, and attend scheduled check-ups.",
    "Medium Risk": "Schedule closer monitoring, review vital signs regularly, and advise follow-up with a qualified clinician.",
    "High Risk": "Treat as a priority case. Recommend urgent clinical review and continuous monitoring by a healthcare professional.",
}


def _to_float(value) -> float:
    if isinstance(value, Decimal):
        return float(value)
    return float(value)


def load_artifacts():
    missing = [str(path.name) for path in (MODEL_PATH, SCALER_PATH, MAPPING_PATH) if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing ML artifact(s): " + ", ".join(missing) + ". Run: python manage.py train_maternal_model"
        )
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    with open(MAPPING_PATH, "r", encoding="utf-8") as file:
        mapping = json.load(file)
    return model, scaler, mapping


def get_model_metrics() -> Dict:
    if not METRICS_PATH.exists():
        return {}
    with open(METRICS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def build_feature_vector(data: Dict) -> pd.DataFrame:
    """Convert cleaned form data to the feature order used during training."""
    values = [[
        _to_float(data["age"]),
        _to_float(data["systolic_bp"]),
        _to_float(data["diastolic_bp"]),
        _to_float(data["blood_sugar"]),
        _to_float(data["body_temperature"]),
        _to_float(data["heart_rate"]),
        _to_float(data["gestational_age"]),
    ]]
    return pd.DataFrame(values, columns=FEATURE_COLUMNS)


def estimate_confidence(model, scaled_values: np.ndarray, cluster_id: int) -> float:
    """Approximates confidence from distance to cluster centers.

    K-Means does not return probability. For a defense-friendly system, this uses
    how much closer the input is to the nearest cluster compared with the next
    nearest cluster. It should be explained as an estimated confidence, not a
    medical probability.
    """
    centers = model.cluster_centers_
    distances = np.linalg.norm(centers - scaled_values, axis=1)
    ordered = np.sort(distances)
    if len(ordered) < 2 or ordered[1] == 0:
        return 100.0
    separation = max(0.0, 1 - (ordered[0] / ordered[1]))
    confidence = 55 + (separation * 45)
    return round(float(min(99.0, max(55.0, confidence))), 2)


def predict_maternal_risk(data: Dict) -> Dict:
    model, scaler, mapping = load_artifacts()
    vector = build_feature_vector(data)
    scaled_values = scaler.transform(vector)
    cluster_id = int(model.predict(scaled_values)[0])
    risk_level = mapping.get(str(cluster_id), "Medium Risk")
    confidence = estimate_confidence(model, scaled_values[0], cluster_id)
    return {
        "cluster_id": cluster_id,
        "risk_level": risk_level,
        "confidence_score": confidence,
        "recommendation": RECOMMENDATIONS.get(risk_level, RECOMMENDATIONS["Medium Risk"]),
    }
