import uuid
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Patient(models.Model):
    """Stores basic anonymized patient identity used for local prediction history."""

    patient_code = models.CharField(max_length=30, unique=True, blank=True)
    full_name = models.CharField(max_length=120)
    age = models.PositiveIntegerField(validators=[MinValueValidator(10), MaxValueValidator(60)])
    phone_number = models.CharField(max_length=25, blank=True)
    address = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.patient_code:
            timestamp = timezone.now().strftime("%Y%m%d")
            suffix = uuid.uuid4().hex[:6].upper()
            self.patient_code = f"MHP-{timestamp}-{suffix}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient_code} - {self.full_name}"


class MaternalPrediction(models.Model):
    """Stores clinical input values and prediction result returned by the ML model."""

    RISK_CHOICES = [
        ("Low Risk", "Low Risk"),
        ("Medium Risk", "Medium Risk"),
        ("High Risk", "High Risk"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="predictions")
    gestational_age = models.PositiveIntegerField(
        help_text="Gestational age in weeks",
        validators=[MinValueValidator(1), MaxValueValidator(45)],
    )
    systolic_bp = models.PositiveIntegerField(
        help_text="Systolic blood pressure in mmHg",
        validators=[MinValueValidator(60), MaxValueValidator(230)],
    )
    diastolic_bp = models.PositiveIntegerField(
        help_text="Diastolic blood pressure in mmHg",
        validators=[MinValueValidator(40), MaxValueValidator(150)],
    )
    blood_sugar = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Blood sugar level",
        validators=[MinValueValidator(1), MaxValueValidator(30)],
    )
    body_temperature = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Body temperature in Fahrenheit",
        validators=[MinValueValidator(90), MaxValueValidator(110)],
    )
    heart_rate = models.PositiveIntegerField(
        help_text="Heart rate in beats per minute",
        validators=[MinValueValidator(35), MaxValueValidator(180)],
    )
    cluster_id = models.IntegerField(null=True, blank=True)
    risk_level = models.CharField(max_length=20, choices=RISK_CHOICES)
    confidence_score = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    recommendation = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maternal_predictions",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def risk_class(self):
        return self.risk_level.lower().replace(" ", "-")

    def __str__(self):
        return f"{self.patient.full_name} - {self.risk_level}"
