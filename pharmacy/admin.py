from django.contrib import admin
from .models import Medicine, Prescription, PrescriptionItem

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['medicine_id', 'name', 'category', 'quantity', 'unit_price', 'expiry_date', 'is_low_stock']
    list_filter = ['category', 'expiry_date']
    search_fields = ['medicine_id', 'name', 'generic_name']
    readonly_fields = ['medicine_id', 'created_at', 'updated_at']

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['prescription_id', 'patient', 'doctor', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['prescription_id', 'patient__first_name', 'patient__last_name']
    readonly_fields = ['prescription_id', 'created_at']

@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ['prescription', 'medicine', 'dosage', 'quantity']
    search_fields = ['prescription__prescription_id', 'medicine__name']
