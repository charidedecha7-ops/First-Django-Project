from django.db import models
from core.models import User

class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('general', 'General Practitioner'),
        ('pediatrics', 'Pediatrics'),
        ('gynecology', 'Gynecology'),
        ('surgery', 'Surgery'),
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('dermatology', 'Dermatology'),
        ('psychiatry', 'Psychiatry'),
        ('ophthalmology', 'Ophthalmology'),
        ('ent', 'ENT'),
        ('radiology', 'Radiology'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    license_number = models.CharField(max_length=50, unique=True)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    qualification = models.CharField(max_length=200)
    experience_years = models.IntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    available_days = models.CharField(max_length=100, help_text='e.g., Mon,Tue,Wed,Thu,Fri')
    available_time_start = models.TimeField()
    available_time_end = models.TimeField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'doctors'
        ordering = ['user__first_name']
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.get_specialization_display()}"


class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='nurse_profile')
    license_number = models.CharField(max_length=50, unique=True)
    qualification = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    shift = models.CharField(max_length=20, choices=[
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('night', 'Night'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'nurses'
        ordering = ['user__first_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.department}"
