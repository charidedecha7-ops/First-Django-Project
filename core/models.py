from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('lab_technician', 'Lab Technician'),
        ('pharmacist', 'Pharmacist'),
        ('receptionist', 'Receptionist'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='receptionist')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    kebele_id = models.CharField(max_length=50, blank=True, verbose_name='Kebele ID')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_active_staff = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    @property
    def full_name(self):
        return self.get_full_name() or self.username


class Region(models.Model):
    name = models.CharField(max_length=100)
    name_am = models.CharField(max_length=100, blank=True, verbose_name='Name (Amharic)')
    name_om = models.CharField(max_length=100, blank=True, verbose_name='Name (Oromoo)')
    code = models.CharField(max_length=10, unique=True)
    
    class Meta:
        db_table = 'regions'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Woreda(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='woredas')
    name = models.CharField(max_length=100)
    name_am = models.CharField(max_length=100, blank=True)
    name_om = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=20, unique=True)
    
    class Meta:
        db_table = 'woredas'
        ordering = ['region', 'name']
    
    def __str__(self):
        return f"{self.name}, {self.region.name}"


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    object_id = models.IntegerField()
    changes = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name} - {self.timestamp}"
