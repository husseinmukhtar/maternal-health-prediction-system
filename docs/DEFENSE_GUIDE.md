# Defense Guide

## 1. Project Summary

The Maternal Health Prediction System is a web-based application designed to support early maternal health risk screening. It accepts maternal clinical data and uses unsupervised machine learning to group records into risk categories.

## 2. Main Problem Solved

Manual maternal risk assessment can be slow, inconsistent, and dependent on the availability of skilled healthcare personnel. This project introduces a data-driven support system that can help identify possible low, medium, and high-risk maternal cases more quickly.

## 3. Why Unsupervised Learning Was Used

Unsupervised learning is useful when the goal is to discover hidden patterns in data. In this project, K-Means clustering groups similar maternal health records together. The model is trained without using the RiskLevel column.

## 4. Algorithm Used

The algorithm used is **K-Means Clustering**. It works by:

1. Selecting a number of clusters, in this case 3.
2. Assigning data points to the nearest cluster center.
3. Updating the centers based on assigned records.
4. Repeating the process until the clusters stabilize.

## 5. Features Used

- Age
- Systolic Blood Pressure
- Diastolic Blood Pressure
- Blood Sugar
- Body Temperature
- Heart Rate
- Gestational Age

## 6. Evaluation Metrics

Since the main algorithm is unsupervised, the key metrics are:

- Silhouette Score
- Davies-Bouldin Index
- Calinski-Harabasz Score

The system also reports accuracy, precision, recall, and F1-score only as an external comparison against reference labels.

## 7. System Modules

- Authentication module
- Patient data entry module
- Machine learning prediction module
- Dashboard and analytics module
- Prediction history module
- CSV export module
- Admin management module

## 8. How to Demonstrate

1. Run the server.
2. Login with the demo account.
3. Open the dashboard.
4. Create a new prediction.
5. Enter low-risk values and show result.
6. Enter high-risk values and show result.
7. Open history page.
8. Show model information page.
9. Explain that RiskLevel was not used for training.

## 9. Suggested Demo Inputs

### Low Risk

- Age: 24
- Gestational Age: 22
- Systolic BP: 112
- Diastolic BP: 74
- Blood Sugar: 6.2
- Body Temperature: 98.1
- Heart Rate: 76

### Medium Risk

- Age: 31
- Gestational Age: 30
- Systolic BP: 140
- Diastolic BP: 92
- Blood Sugar: 8.4
- Body Temperature: 99.0
- Heart Rate: 95

### High Risk

- Age: 42
- Gestational Age: 34
- Systolic BP: 170
- Diastolic BP: 110
- Blood Sugar: 14.7
- Body Temperature: 101.2
- Heart Rate: 116

## 10. Limitation

The system is a decision-support prototype and should not replace medical diagnosis by qualified healthcare workers.
