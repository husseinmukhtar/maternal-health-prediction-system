from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from risk.ml.predictor import predict_maternal_risk
from risk.models import MaternalPrediction, Patient


class Command(BaseCommand):
    help = "Create a demo user and sample prediction records for presentation or defense."

    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(username="admin")
        if created:
            user.set_password("admin12345")
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS("Created demo admin user: admin / admin12345"))
        else:
            self.stdout.write("Demo admin user already exists. Username: admin")

        samples = [
            {"full_name": "Aisha Musa", "age": 24, "gestational_age": 22, "systolic_bp": 112, "diastolic_bp": 74, "blood_sugar": Decimal("6.2"), "body_temperature": Decimal("98.1"), "heart_rate": 76},
            {"full_name": "Fatima Bello", "age": 31, "gestational_age": 30, "systolic_bp": 140, "diastolic_bp": 92, "blood_sugar": Decimal("8.4"), "body_temperature": Decimal("99.0"), "heart_rate": 95},
            {"full_name": "Zainab Umar", "age": 42, "gestational_age": 34, "systolic_bp": 170, "diastolic_bp": 110, "blood_sugar": Decimal("14.7"), "body_temperature": Decimal("101.2"), "heart_rate": 116},
        ]
        created_count = 0
        for sample in samples:
            if Patient.objects.filter(full_name=sample["full_name"]).exists():
                continue
            result = predict_maternal_risk(sample)
            patient = Patient.objects.create(full_name=sample["full_name"], age=sample["age"])
            MaternalPrediction.objects.create(
                patient=patient,
                gestational_age=sample["gestational_age"],
                systolic_bp=sample["systolic_bp"],
                diastolic_bp=sample["diastolic_bp"],
                blood_sugar=sample["blood_sugar"],
                body_temperature=sample["body_temperature"],
                heart_rate=sample["heart_rate"],
                cluster_id=result["cluster_id"],
                risk_level=result["risk_level"],
                confidence_score=Decimal(str(result["confidence_score"])),
                recommendation=result["recommendation"],
                created_by=user,
            )
            created_count += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created_count} demo prediction record(s)."))
