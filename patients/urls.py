from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('<int:pk>/', views.patient_detail, name='patient_detail'),
    path('create/', views.patient_create, name='patient_create'),
    path('<int:pk>/update/', views.patient_update, name='patient_update'),
    path('<int:patient_id>/add-history/', views.add_medical_history, name='add_medical_history'),
]
