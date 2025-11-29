from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Patient, MedicalHistory, Allergy
from .forms import PatientForm, MedicalHistoryForm
import joblib
import os
from django.conf import settings

@login_required
def patient_list(request):
    query = request.GET.get('q', '')
    patients = Patient.objects.all()
    
    if query:
        patients = patients.filter(
            Q(patient_id__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone__icontains=query)
        )
    
    return render(request, 'patients/patient_list.html', {
        'patients': patients,
        'query': query
    })

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    medical_histories = patient.medical_histories.all()[:10]
    allergies = patient.allergies.all()
    
    return render(request, 'patients/patient_detail.html', {
        'patient': patient,
        'medical_histories': medical_histories,
        'allergies': allergies,
    })

@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.registered_by = request.user
            patient.save()
            messages.success(request, f'Patient {patient.full_name} registered successfully!')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm()
    
    return render(request, 'patients/patient_form.html', {'form': form})

@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient information updated successfully!')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    
    return render(request, 'patients/patient_form.html', {
        'form': form,
        'patient': patient
    })

@login_required
def add_medical_history(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            history = form.save(commit=False)
            history.patient = patient
            
            # ML Disease Prediction
            try:
                model_path = os.path.join(settings.ML_MODELS_PATH, 'disease_prediction_model.pkl')
                if os.path.exists(model_path):
                    model = joblib.load(model_path)
                    # Prepare features for prediction
                    features = [[
                        patient.age,
                        1 if patient.gender == 'M' else 0,
                        float(history.blood_pressure.split('/')[0]) if history.blood_pressure else 120,
                        float(history.glucose_level) if history.glucose_level else 100,
                        float(history.temperature) if history.temperature else 37,
                    ]]
                    prediction = model.predict(features)
                    history.predicted_disease = prediction[0]
            except Exception as e:
                print(f"ML Prediction Error: {e}")
            
            history.save()
            messages.success(request, 'Medical history added successfully!')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = MedicalHistoryForm()
    
    return render(request, 'patients/medical_history_form.html', {
        'form': form,
        'patient': patient
    })
