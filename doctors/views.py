from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Doctor, Nurse

@login_required
def doctor_list(request):
    specialization = request.GET.get('specialization', '')
    doctors = Doctor.objects.filter(is_available=True).select_related('user')
    
    if specialization:
        doctors = doctors.filter(specialization=specialization)
    
    return render(request, 'doctors/doctor_list.html', {
        'doctors': doctors,
        'specializations': Doctor.SPECIALIZATION_CHOICES,
        'selected_specialization': specialization,
    })

@login_required
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'doctors/doctor_detail.html', {'doctor': doctor})

@login_required
def nurse_list(request):
    nurses = Nurse.objects.all().select_related('user')
    return render(request, 'doctors/nurse_list.html', {'nurses': nurses})
