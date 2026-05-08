# Maternal Health Prediction System

## Project Title
**Design and Implementation of a Maternal Health Prediction System Based on Unsupervised Learning**

This is a complete Django implementation of a web-based maternal health risk stratification system. It uses a K-Means clustering model to group maternal health records into **Low Risk**, **Medium Risk**, and **High Risk** categories.

> Important: This is an academic decision-support prototype. It does not replace professional medical diagnosis.

---

## Main Features

- User login and admin dashboard
- Patient maternal health data entry form
- Unsupervised K-Means model for risk grouping
- Risk prediction result with cluster ID, confidence estimate, and recommendation
- Prediction history with search and risk-level filtering
- CSV export of prediction records
- Model information page with clustering metrics
- Demo seed command for defense/presentation
- Retraining command for the machine learning model

---

## Technology Stack

- **Backend:** Django, Python
- **Machine Learning:** Scikit-learn, Pandas, NumPy, Joblib
- **Database:** SQLite by default
- **Frontend:** HTML, CSS, Django Templates
- **Algorithm:** K-Means Clustering

---

## Project Structure

```text
maternal_health_prediction_system/
│── manage.py
│── requirements.txt
│── README.md
│── maternal_health_system/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│── risk/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── ml/
│   │   ├── data/maternal_health_sample_dataset.csv
│   │   ├── predictor.py
│   │   ├── train_model.py
│   │   └── model_artifacts/
│   │       ├── maternal_kmeans_model.joblib
│   │       ├── maternal_scaler.joblib
│   │       ├── cluster_mapping.json
│   │       └── model_metrics.json
│   ├── management/commands/
│   │   ├── train_maternal_model.py
│   │   └── seed_demo.py
│   └── templates/risk/
│── static/css/styles.css
│── docs/
│   ├── DEFENSE_GUIDE.md
│   ├── DATABASE_SCHEMA.md
│   └── SYSTEM_DESIGN.md
└── scripts/
    ├── generate_artifacts.py
    └── run_prediction_test.py
```

---

## Installation Guide on Windows

### 1. Open the project folder in VS Code

Right-click the unzipped project folder and choose **Open with Code**.

### 2. Open VS Code terminal

Use:

```bash
Terminal > New Terminal
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

```bash
venv\Scripts\activate
```

You should see `(venv)` at the beginning of the terminal line.

### 5. Install requirements

```bash
pip install -r requirements.txt
```

### 6. Run database migrations

```bash
python manage.py migrate
```

### 7. Create demo user and sample data

```bash
python manage.py seed_demo
```

This creates:

```text
Username: admin
Password: admin12345
```

### 8. Start the server

```bash
python manage.py runserver
```

### 9. Open the system in your browser

```text
http://127.0.0.1:8000/
```

Login here:

```text
http://127.0.0.1:8000/accounts/login/
```

---

## How to Retrain the Model

The trained model is already included, but you can retrain it using:

```bash
python manage.py train_maternal_model
```

This command reads:

```text
risk/ml/data/maternal_health_sample_dataset.csv
```

and updates the saved model artifacts inside:

```text
risk/ml/model_artifacts/
```

---

## How to Test the Prediction Engine Without Running Django

```bash
python scripts/run_prediction_test.py
```

---

## Why This Is Unsupervised Learning

The system trains a K-Means model using only numerical maternal health indicators:

- Age
- Systolic BP
- Diastolic BP
- Blood Sugar
- Body Temperature
- Heart Rate
- Gestational Age

The dataset contains a `RiskLevel` column, but that column is **not used during model training**. It is only used after clustering to compare the discovered clusters with reference labels for academic evaluation.

---

## Defense Explanation

During defense, explain it like this:

> The project uses unsupervised learning because the K-Means model identifies natural groupings in maternal health data without being trained directly on risk labels. After clustering, the system interprets the clusters as low, medium, and high risk by examining the cluster centers and their clinical risk patterns. The existing RiskLevel column is retained only for evaluation and explanation, not for training the model.

---

## Common Commands

```bash
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
python manage.py train_maternal_model
python scripts/run_prediction_test.py
```
