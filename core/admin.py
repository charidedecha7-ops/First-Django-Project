from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Region, Woreda, AuditLog

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active_staff']
    list_filter = ['role', 'is_active', 'is_staff', 'is_active_staff']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'address', 'kebele_id', 'profile_picture', 'is_active_staff')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'address', 'kebele_id')}),
    )

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_am', 'name_om', 'code']
    search_fields = ['name', 'code']

@admin.register(Woreda)
class WoredaAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'code']
    list_filter = ['region']
    search_fields = ['name', 'code']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'object_id', 'timestamp']
    list_filter = ['action', 'model_name', 'timestamp']
    search_fields = ['user__username', 'model_name']
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 'changes', 'ip_address', 'timestamp']
