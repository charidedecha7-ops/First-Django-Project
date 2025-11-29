from django.contrib import admin
from .models import Doctor, Nurse

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'license_number', 'consultation_fee', 'is_available']
    list_filter = ['specialization', 'is_available']
    search_fields = ['user__first_name', 'user__last_name', 'license_number']

@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'shift', 'license_number']
    list_filter = ['department', 'shift']
    search_fields = ['user__first_name', 'user__last_name', 'license_number']
