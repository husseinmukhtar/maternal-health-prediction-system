# System Design

## Architecture

The system follows a three-layer architecture:

1. Presentation Layer: HTML, CSS, Django templates
2. Application Layer: Django views, forms, URLs, authentication, business logic
3. Data and ML Layer: SQLite database, K-Means model, scaler, model artifacts

## Data Flow

```text
Healthcare Worker
      ↓
Maternal Input Form
      ↓
Django View Validation
      ↓
Feature Vector Builder
      ↓
Standard Scaler
      ↓
K-Means Clustering Model
      ↓
Risk Mapping
      ↓
Prediction Result + Recommendation
      ↓
Database Storage
```

## Main Use Cases

- Login
- Enter patient data
- Predict maternal health risk
- View prediction result
- View dashboard
- Search prediction history
- Export prediction records
- View model information

## Machine Learning Pipeline

```text
Dataset Collection
      ↓
Data Cleaning
      ↓
Feature Selection
      ↓
Feature Scaling
      ↓
K-Means Training
      ↓
Cluster Interpretation
      ↓
Model Evaluation
      ↓
Model Deployment
```

## Why Cluster Mapping Is Needed

K-Means returns numerical cluster IDs such as 0, 1, and 2. These numbers do not automatically mean low, medium, or high risk. Therefore, the system examines the cluster centers and orders them using a risk scoring logic. The lowest-risk center becomes Low Risk, the next becomes Medium Risk, and the highest-risk center becomes High Risk.
