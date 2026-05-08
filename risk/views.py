import csv
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import MaternalPredictionForm
from .ml.predictor import get_model_metrics, predict_maternal_risk
from .models import MaternalPrediction, Patient


def home(request):
    total_predictions = MaternalPrediction.objects.count()
    high_risk_count = MaternalPrediction.objects.filter(risk_level="High Risk").count()
    metrics = get_model_metrics()
    context = {
        "total_predictions": total_predictions,
        "high_risk_count": high_risk_count,
        "metrics": metrics,
    }
    return render(request, "risk/home.html", context)


@login_required
def dashboard(request):
    total_predictions = MaternalPrediction.objects.count()
    total_patients = Patient.objects.count()
    risk_summary = MaternalPrediction.objects.values("risk_level").annotate(total=Count("id")).order_by("risk_level")
    recent_predictions = MaternalPrediction.objects.select_related("patient", "created_by")[:8]
    metrics = get_model_metrics()

    # Make sure all three categories appear in the dashboard even if there are no records yet.
    ordered = ["Low Risk", "Medium Risk", "High Risk"]
    summary_map = {item["risk_level"]: item["total"] for item in risk_summary}
    summary = [{"risk_level": level, "total": summary_map.get(level, 0)} for level in ordered]
    max_count = max([item["total"] for item in summary] + [1])
    for item in summary:
        item["percentage"] = round((item["total"] / max_count) * 100, 1)

    context = {
        "total_predictions": total_predictions,
        "total_patients": total_patients,
        "summary": summary,
        "recent_predictions": recent_predictions,
        "metrics": metrics,
    }
    return render(request, "risk/dashboard.html", context)


@login_required
def predict(request):
    if request.method == "POST":
        form = MaternalPredictionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            result = predict_maternal_risk(data)
            patient = Patient.objects.create(
                full_name=data["full_name"],
                age=data["age"],
                phone_number=data.get("phone_number", ""),
                address=data.get("address", ""),
            )
            prediction = MaternalPrediction.objects.create(
                patient=patient,
                gestational_age=data["gestational_age"],
                systolic_bp=data["systolic_bp"],
                diastolic_bp=data["diastolic_bp"],
                blood_sugar=data["blood_sugar"],
                body_temperature=data["body_temperature"],
                heart_rate=data["heart_rate"],
                cluster_id=result["cluster_id"],
                risk_level=result["risk_level"],
                confidence_score=Decimal(str(result["confidence_score"])),
                recommendation=result["recommendation"],
                created_by=request.user,
            )
            messages.success(request, "Prediction completed successfully.")
            return redirect("prediction_detail", pk=prediction.pk)
    else:
        form = MaternalPredictionForm()
    return render(request, "risk/predict.html", {"form": form})


@login_required
def prediction_history(request):
    risk_level = request.GET.get("risk")
    query = request.GET.get("q", "").strip()
    predictions = MaternalPrediction.objects.select_related("patient", "created_by")
    if risk_level in ["Low Risk", "Medium Risk", "High Risk"]:
        predictions = predictions.filter(risk_level=risk_level)
    if query:
        predictions = predictions.filter(patient__full_name__icontains=query)
    context = {
        "predictions": predictions,
        "selected_risk": risk_level,
        "query": query,
    }
    return render(request, "risk/history.html", context)


@login_required
def prediction_detail(request, pk):
    prediction = get_object_or_404(MaternalPrediction.objects.select_related("patient", "created_by"), pk=pk)
    return render(request, "risk/detail.html", {"prediction": prediction})


@login_required
def export_predictions_csv(request):
    response = HttpResponse(content_type="text/csv")
    filename = f"maternal_predictions_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow([
        "Patient Code",
        "Full Name",
        "Age",
        "Gestational Age",
        "Systolic BP",
        "Diastolic BP",
        "Blood Sugar",
        "Body Temperature",
        "Heart Rate",
        "Cluster ID",
        "Risk Level",
        "Confidence",
        "Created At",
    ])
    for pred in MaternalPrediction.objects.select_related("patient").all():
        writer.writerow([
            pred.patient.patient_code,
            pred.patient.full_name,
            pred.patient.age,
            pred.gestational_age,
            pred.systolic_bp,
            pred.diastolic_bp,
            pred.blood_sugar,
            pred.body_temperature,
            pred.heart_rate,
            pred.cluster_id,
            pred.risk_level,
            pred.confidence_score,
            pred.created_at.strftime("%Y-%m-%d %H:%M"),
        ])
    return response


@login_required
def model_info(request):
    metrics = get_model_metrics()
    return render(request, "risk/model_info.html", {"metrics": metrics})
