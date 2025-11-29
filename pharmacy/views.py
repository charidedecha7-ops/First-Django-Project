from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from .models import Medicine, Prescription
from datetime import datetime, timedelta

@login_required
def medicine_list(request):
    medicines = Medicine.objects.all()
    low_stock = request.GET.get('low_stock', '')
    
    if low_stock:
        medicines = medicines.filter(quantity__lt=F('reorder_level'))
    
    return render(request, 'pharmacy/medicine_list.html', {'medicines': medicines})

@login_required
def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    return render(request, 'pharmacy/medicine_detail.html', {'medicine': medicine})

@login_required
def prescription_list(request):
    status_filter = request.GET.get('status', '')
    prescriptions = Prescription.objects.select_related('patient', 'doctor__user')
    
    if status_filter:
        prescriptions = prescriptions.filter(status=status_filter)
    
    return render(request, 'pharmacy/prescription_list.html', {
        'prescriptions': prescriptions,
    })

@login_required
def prescription_detail(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    items = prescription.items.select_related('medicine')
    return render(request, 'pharmacy/prescription_detail.html', {
        'prescription': prescription,
        'items': items,
    })
