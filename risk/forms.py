from django import forms


class MaternalPredictionForm(forms.Form):
    full_name = forms.CharField(
        label="Patient full name",
        max_length=120,
        widget=forms.TextInput(attrs={"placeholder": "e.g. Aisha Musa"}),
    )
    phone_number = forms.CharField(
        label="Phone number",
        max_length=25,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Optional"}),
    )
    address = forms.CharField(
        label="Address",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Optional"}),
    )
    age = forms.IntegerField(
        min_value=10,
        max_value=60,
        widget=forms.NumberInput(attrs={"placeholder": "e.g. 28"}),
    )
    gestational_age = forms.IntegerField(
        label="Gestational age (weeks)",
        min_value=1,
        max_value=45,
        widget=forms.NumberInput(attrs={"placeholder": "e.g. 26"}),
    )
    systolic_bp = forms.IntegerField(
        label="Systolic BP (mmHg)",
        min_value=60,
        max_value=230,
        widget=forms.NumberInput(attrs={"placeholder": "e.g. 120"}),
    )
    diastolic_bp = forms.IntegerField(
        label="Diastolic BP (mmHg)",
        min_value=40,
        max_value=150,
        widget=forms.NumberInput(attrs={"placeholder": "e.g. 80"}),
    )
    blood_sugar = forms.DecimalField(
        label="Blood sugar level",
        min_value=1,
        max_value=30,
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"step": "0.1", "placeholder": "e.g. 7.2"}),
    )
    body_temperature = forms.DecimalField(
        label="Body temperature (°F)",
        min_value=90,
        max_value=110,
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"step": "0.1", "placeholder": "e.g. 98.6"}),
    )
    heart_rate = forms.IntegerField(
        label="Heart rate (bpm)",
        min_value=35,
        max_value=180,
        widget=forms.NumberInput(attrs={"placeholder": "e.g. 82"}),
    )

    def clean(self):
        cleaned = super().clean()
        systolic = cleaned.get("systolic_bp")
        diastolic = cleaned.get("diastolic_bp")
        if systolic and diastolic and diastolic >= systolic:
            raise forms.ValidationError("Diastolic BP should normally be lower than systolic BP.")
        return cleaned
