from django.contrib import admin
from .models import MaternalPrediction, Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("patient_code", "full_name", "age", "phone_number", "created_at")
    search_fields = ("patient_code", "full_name", "phone_number")
    list_filter = ("created_at",)


@admin.register(MaternalPrediction)
class MaternalPredictionAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "risk_level",
        "confidence_score",
        "systolic_bp",
        "diastolic_bp",
        "blood_sugar",
        "created_at",
    )
    search_fields = ("patient__full_name", "patient__patient_code", "risk_level")
    list_filter = ("risk_level", "created_at")
    readonly_fields = ("cluster_id", "risk_level", "confidence_score", "recommendation", "created_at")
