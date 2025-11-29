from django.db import models
from patients.models import Patient
from doctors.models import Doctor

class Medicine(models.Model):
    medicine_id = models.CharField(max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True)
    manufacturer = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    unit = models.CharField(max_length=50, default='tablet')
    quantity = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=50)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'medicines'
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.medicine_id:
            last_medicine = Medicine.objects.order_by('-id').first()
            if last_medicine:
                last_id = int(last_medicine.medicine_id.split('-')[1])
                self.medicine_id = f'MED-{last_id + 1:06d}'
            else:
                self.medicine_id = 'MED-000001'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"
    
    @property
    def is_low_stock(self):
        return self.quantity < self.reorder_level


class Prescription(models.Model):
    prescription_id = models.CharField(max_length=20, unique=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    diagnosis = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('dispensed', 'Dispensed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    dispensed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'prescriptions'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.prescription_id:
            last_prescription = Prescription.objects.order_by('-id').first()
            if last_prescription:
                last_id = int(last_prescription.prescription_id.split('-')[1])
                self.prescription_id = f'PRE-{last_id + 1:06d}'
            else:
                self.prescription_id = 'PRE-000001'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.prescription_id} - {self.patient.full_name}"


class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    quantity = models.IntegerField()
    instructions = models.TextField(blank=True)
    
    class Meta:
        db_table = 'prescription_items'
    
    def __str__(self):
        return f"{self.medicine.name} - {self.dosage}"
