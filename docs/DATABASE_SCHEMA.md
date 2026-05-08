# Database Schema

The system uses SQLite by default for easy installation and defense. Django ORM creates the database tables during migration.

## Patient Table

Stores basic patient identity and demographic information.

| Field | Type | Description |
|---|---|---|
| id | BigAutoField | Primary key |
| patient_code | CharField | Unique generated patient code |
| full_name | CharField | Patient full name |
| age | PositiveIntegerField | Patient age |
| phone_number | CharField | Optional phone number |
| address | CharField | Optional address |
| created_at | DateTimeField | Date created |

## MaternalPrediction Table

Stores maternal clinical input and machine learning output.

| Field | Type | Description |
|---|---|---|
| id | BigAutoField | Primary key |
| patient | ForeignKey | Linked patient |
| gestational_age | PositiveIntegerField | Pregnancy age in weeks |
| systolic_bp | PositiveIntegerField | Systolic blood pressure |
| diastolic_bp | PositiveIntegerField | Diastolic blood pressure |
| blood_sugar | DecimalField | Blood sugar value |
| body_temperature | DecimalField | Body temperature in Fahrenheit |
| heart_rate | PositiveIntegerField | Heart rate in bpm |
| cluster_id | IntegerField | K-Means cluster number |
| risk_level | CharField | Low, Medium, or High Risk |
| confidence_score | DecimalField | Estimated confidence score |
| recommendation | TextField | Clinical recommendation text |
| created_by | ForeignKey | User who made the prediction |
| created_at | DateTimeField | Date predicted |

## Relationship

One patient can have many maternal prediction records.

```text
Patient 1 ---- * MaternalPrediction
```
