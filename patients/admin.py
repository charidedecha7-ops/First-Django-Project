from django.contrib import admin
from .models import Patient, MedicalHistory, Allergy

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'full_name', 'gender', 'age', 'phone', 'created_at']
    list_filter = ['gender', 'blood_group', 'created_at']
    search_fields = ['patient_id', 'first_name', 'last_name', 'phone', 'kebele_id']
    readonly_fields = ['patient_id', 'created_at', 'updated_at']

@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ['patient', 'diagnosis', 'doctor', 'visit_date']
    list_filter = ['visit_date', 'diagnosis']
    search_fields = ['patient__first_name', 'patient__last_name', 'diagnosis']

@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ['patient', 'allergen', 'severity', 'diagnosed_date']
    list_filter = ['severity', 'diagnosed_date']
    search_fields = ['patient__first_name', 'patient__last_name', 'allergen']
