from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("predict/", views.predict, name="predict"),
    path("history/", views.prediction_history, name="history"),
    path("history/export/", views.export_predictions_csv, name="export_predictions_csv"),
    path("prediction/<int:pk>/", views.prediction_detail, name="prediction_detail"),
    path("model/", views.model_info, name="model_info"),
]
