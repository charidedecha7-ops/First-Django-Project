from django.db import models
from core.models import User, Woreda

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    
    patient_id = models.CharField(max_length=20, unique=True, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    woreda = models.ForeignKey(Woreda, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField()
    kebele_id = models.CharField(max_length=50, blank=True)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='patients/', blank=True, null=True)
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'patients'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.patient_id:
            last_patient = Patient.objects.order_by('-id').first()
            if last_patient:
                last_id = int(last_patient.patient_id.split('-')[1])
                self.patient_id = f'PAT-{last_id + 1:06d}'
            else:
                self.patient_id = 'PAT-000001'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.patient_id} - {self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )


class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_histories')
    diagnosis = models.CharField(max_length=200)
    symptoms = models.TextField()
    treatment = models.TextField()
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    visit_date = models.DateTimeField(auto_now_add=True)
    
    # Vitals
    blood_pressure = models.CharField(max_length=20, blank=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    glucose_level = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # ML Predictions
    predicted_disease = models.CharField(max_length=100, blank=True)
    risk_score = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'medical_histories'
        ordering = ['-visit_date']
        verbose_name_plural = 'Medical Histories'
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.diagnosis} - {self.visit_date.date()}"


class Allergy(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='allergies')
    allergen = models.CharField(max_length=100)
    reaction = models.TextField()
    severity = models.CharField(max_length=20, choices=[
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    ])
    diagnosed_date = models.DateField()
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'allergies'
        verbose_name_plural = 'Allergies'
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.allergen}"
