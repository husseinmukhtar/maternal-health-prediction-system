# Generated manually for project package portability.
import django.core.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_code', models.CharField(blank=True, max_length=30, unique=True)),
                ('full_name', models.CharField(max_length=120)),
                ('age', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(60)])),
                ('phone_number', models.CharField(blank=True, max_length=25)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='MaternalPrediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gestational_age', models.PositiveIntegerField(help_text='Gestational age in weeks', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(45)])),
                ('systolic_bp', models.PositiveIntegerField(help_text='Systolic blood pressure in mmHg', validators=[django.core.validators.MinValueValidator(60), django.core.validators.MaxValueValidator(230)])),
                ('diastolic_bp', models.PositiveIntegerField(help_text='Diastolic blood pressure in mmHg', validators=[django.core.validators.MinValueValidator(40), django.core.validators.MaxValueValidator(150)])),
                ('blood_sugar', models.DecimalField(decimal_places=2, help_text='Blood sugar level', max_digits=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)])),
                ('body_temperature', models.DecimalField(decimal_places=2, help_text='Body temperature in Fahrenheit', max_digits=5, validators=[django.core.validators.MinValueValidator(90), django.core.validators.MaxValueValidator(110)])),
                ('heart_rate', models.PositiveIntegerField(help_text='Heart rate in beats per minute', validators=[django.core.validators.MinValueValidator(35), django.core.validators.MaxValueValidator(180)])),
                ('cluster_id', models.IntegerField(blank=True, null=True)),
                ('risk_level', models.CharField(choices=[('Low Risk', 'Low Risk'), ('Medium Risk', 'Medium Risk'), ('High Risk', 'High Risk')], max_length=20)),
                ('confidence_score', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('recommendation', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='maternal_predictions', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predictions', to='risk.patient')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
