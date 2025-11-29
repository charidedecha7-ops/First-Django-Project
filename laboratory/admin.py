from django.contrib import admin
from .models import LabTest

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ['test_id', 'patient', 'test_name', 'status', 'requested_date']
    list_filter = ['status', 'test_type', 'requested_date']
    search_fields = ['test_id', 'patient__first_name', 'patient__last_name', 'test_name']
    readonly_fields = ['test_id', 'created_at', 'updated_at']
