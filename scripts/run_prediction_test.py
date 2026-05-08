"""Quick test for the ML prediction engine without starting the Django server."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from risk.ml.predictor import predict_maternal_risk  # noqa: E402

samples = [
    {
        "name": "Low risk sample",
        "age": 24,
        "gestational_age": 22,
        "systolic_bp": 112,
        "diastolic_bp": 74,
        "blood_sugar": 6.2,
        "body_temperature": 98.1,
        "heart_rate": 76,
    },
    {
        "name": "Medium risk sample",
        "age": 31,
        "gestational_age": 30,
        "systolic_bp": 140,
        "diastolic_bp": 92,
        "blood_sugar": 8.4,
        "body_temperature": 99.0,
        "heart_rate": 95,
    },
    {
        "name": "High risk sample",
        "age": 42,
        "gestational_age": 34,
        "systolic_bp": 170,
        "diastolic_bp": 110,
        "blood_sugar": 14.7,
        "body_temperature": 101.2,
        "heart_rate": 116,
    },
]

for sample in samples:
    result = predict_maternal_risk(sample)
    print("=" * 60)
    print(sample["name"])
    print(f"Cluster: {result['cluster_id']}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Confidence: {result['confidence_score']}%")
    print(f"Recommendation: {result['recommendation']}")
