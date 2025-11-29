from django.db import models
from patients.models import Patient
from doctors.models import Doctor

class LabTest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    test_id = models.CharField(max_length=20, unique=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_tests')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    test_name = models.CharField(max_length=200)
    test_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    results = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Common test results
    malaria_test = models.CharField(max_length=20, blank=True, choices=[
        ('positive', 'Positive'),
        ('negative', 'Negative'),
    ])
    rdt_result = models.CharField(max_length=20, blank=True)
    blood_glucose = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hemoglobin = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lab_tests'
        ordering = ['-requested_date']
    
    def save(self, *args, **kwargs):
        if not self.test_id:
            last_test = LabTest.objects.order_by('-id').first()
            if last_test:
                last_id = int(last_test.test_id.split('-')[1])
                self.test_id = f'LAB-{last_id + 1:06d}'
            else:
                self.test_id = 'LAB-000001'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.test_id} - {self.patient.full_name} - {self.test_name}"
