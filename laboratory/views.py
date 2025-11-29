from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LabTest
from datetime import datetime

@login_required
def lab_test_list(request):
    status_filter = request.GET.get('status', '')
    tests = LabTest.objects.select_related('patient', 'doctor__user')
    
    if status_filter:
        tests = tests.filter(status=status_filter)
    
    return render(request, 'laboratory/lab_test_list.html', {
        'tests': tests,
        'status_choices': LabTest.STATUS_CHOICES,
    })

@login_required
def lab_test_detail(request, pk):
    test = get_object_or_404(LabTest, pk=pk)
    return render(request, 'laboratory/lab_test_detail.html', {'test': test})

@login_required
def lab_test_update_results(request, pk):
    test = get_object_or_404(LabTest, pk=pk)
    
    if request.method == 'POST':
        test.results = request.POST.get('results')
        test.status = 'completed'
        test.completed_date = datetime.now()
        test.save()
        messages.success(request, 'Test results updated successfully!')
        return redirect('lab_test_detail', pk=pk)
    
    return render(request, 'laboratory/lab_test_results_form.html', {'test': test})
