from django.urls import path
from . import views

urlpatterns = [
    path('', views.lab_test_list, name='lab_test_list'),
    path('<int:pk>/', views.lab_test_detail, name='lab_test_detail'),
    path('<int:pk>/update-results/', views.lab_test_update_results, name='lab_test_update_results'),
]
