from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from .forms import AppointmentForm
from datetime import datetime
import joblib
import os
from django.conf import settings

@login_required
def appointment_list(request):
    date_filter = request.GET.get('date', '')
    status_filter = request.GET.get('status', '')
    
    appointments = Appointment.objects.select_related('patient', 'doctor__user')
    
    if date_filter:
        appointments = appointments.filter(appointment_date=date_filter)
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    if request.user.role == 'doctor':
        appointments = appointments.filter(doctor__user=request.user)
    
    return render(request, 'appointments/appointment_list.html', {
        'appointments': appointments,
        'status_choices': Appointment.STATUS_CHOICES,
    })

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            
            # ML No-Show Prediction
            try:
                model_path = os.path.join(settings.ML_MODELS_PATH, 'noshow_prediction_model.pkl')
                if os.path.exists(model_path):
                    model = joblib.load(model_path)
                    
                    # Calculate previous no-shows
                    previous_no_shows = Appointment.objects.filter(
                        patient=appointment.patient,
                        status='no_show'
                    ).count()
                    
                    features = [[
                        appointment.patient.age,
                        float(appointment.distance_from_hospital or 5),
                        1 if appointment.weather_condition == 'rainy' else 0,
                        previous_no_shows,
                        1 if appointment.sms_sent else 0,
                    ]]
                    
                    probability = model.predict_proba(features)[0][1]
                    appointment.no_show_probability = round(probability, 2)
                    appointment.save()
                    
                    if probability > 0.7:
                        messages.warning(request, f'High no-show risk ({probability*100:.0f}%). Consider sending reminder.')
            except Exception as e:
                print(f"ML Prediction Error: {e}")
            
            messages.success(request, 'Appointment created successfully!')
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    
    return render(request, 'appointments/appointment_form.html', {'form': form})

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})

@login_required
def appointment_update_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Appointment.STATUS_CHOICES):
            appointment.status = new_status
            appointment.save()
            messages.success(request, f'Appointment status updated to {appointment.get_status_display()}')
        return redirect('appointment_detail', pk=pk)
    
    return render(request, 'appointments/update_status.html', {
        'appointment': appointment,
        'status_choices': Appointment.STATUS_CHOICES,
    })
