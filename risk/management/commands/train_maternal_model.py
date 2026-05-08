from django.core.management.base import BaseCommand
from risk.ml.train_model import train_model


class Command(BaseCommand):
    help = "Train and save the unsupervised maternal health clustering model."

    def handle(self, *args, **options):
        metrics = train_model()
        self.stdout.write(self.style.SUCCESS("Maternal health model trained successfully."))
        self.stdout.write(f"Silhouette Score: {metrics.get('silhouette_score')}")
        self.stdout.write(f"Davies-Bouldin Index: {metrics.get('davies_bouldin_index')}")
        self.stdout.write(f"External Accuracy: {metrics.get('external_accuracy_against_reference_labels')}")
