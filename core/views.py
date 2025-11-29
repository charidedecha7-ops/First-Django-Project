from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from datetime import datetime, timedelta
from patients.models import Patient
from appointments.models import Appointment
from laboratory.models import LabTest
from pharmacy.models import Medicine
from billing.models import Bill

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user
    today = datetime.now().date()
    
    context = {
        'user': user,
        'total_patients': Patient.objects.count(),
        'today_appointments': Appointment.objects.filter(appointment_date=today).count(),
        'pending_tests': LabTest.objects.filter(status='pending').count(),
        'low_stock_medicines': Medicine.objects.filter(quantity__lt=50).count(),
    }
    
    if user.role == 'doctor':
        context['my_appointments'] = Appointment.objects.filter(
            doctor__user=user,
            appointment_date=today
        ).select_related('patient', 'doctor')[:5]
    
    elif user.role == 'lab_technician':
        context['pending_lab_tests'] = LabTest.objects.filter(
            status='pending'
        ).select_related('patient')[:5]
    
    elif user.role == 'pharmacist':
        context['low_stock'] = Medicine.objects.filter(
            quantity__lt=50
        ).order_by('quantity')[:5]
    
    return render(request, 'core/dashboard.html', context)

@login_required
def profile_view(request):
    return render(request, 'core/profile.html', {'user': request.user})
