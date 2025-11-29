from django.urls import path
from django.shortcuts import redirect
from . import views

def pharmacy_home(request):
    return redirect('medicine_list')

urlpatterns = [
    path('', pharmacy_home, name='pharmacy_home'),
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicines/<int:pk>/', views.medicine_detail, name='medicine_detail'),
    path('prescriptions/', views.prescription_list, name='prescription_list'),
    path('prescriptions/<int:pk>/', views.prescription_detail, name='prescription_detail'),
]
