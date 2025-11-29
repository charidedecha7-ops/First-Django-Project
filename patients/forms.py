from django import forms
from .models import Patient, MedicalHistory, Allergy

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'father_name', 'date_of_birth',
            'gender', 'blood_group', 'phone', 'email', 'woreda',
            'address', 'kebele_id', 'emergency_contact_name',
            'emergency_contact_phone', 'photo'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = [
            'diagnosis', 'symptoms', 'treatment', 'doctor', 'notes',
            'blood_pressure', 'temperature', 'heart_rate', 'weight',
            'height', 'glucose_level'
        ]
        widgets = {
            'symptoms': forms.Textarea(attrs={'rows': 3}),
            'treatment': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class AllergyForm(forms.ModelForm):
    class Meta:
        model = Allergy
        fields = ['allergen', 'reaction', 'severity', 'diagnosed_date', 'notes']
        widgets = {
            'diagnosed_date': forms.DateInput(attrs={'type': 'date'}),
            'reaction': forms.Textarea(attrs={'rows': 2}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
