from django.contrib import admin
from .models import Bill, BillItem, Payment

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['bill_id', 'patient', 'total_amount', 'paid_amount', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['bill_id', 'patient__first_name', 'patient__last_name']
    readonly_fields = ['bill_id', 'created_at', 'updated_at']

@admin.register(BillItem)
class BillItemAdmin(admin.ModelAdmin):
    list_display = ['bill', 'description', 'quantity', 'unit_price', 'total_price']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['bill', 'amount', 'payment_method', 'created_at']
    list_filter = ['payment_method', 'created_at']
    search_fields = ['bill__bill_id', 'transaction_id']
