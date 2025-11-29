from django.urls import path
from . import views

urlpatterns = [
    path('', views.bill_list, name='bill_list'),
    path('<int:pk>/', views.bill_detail, name='bill_detail'),
    path('<int:bill_id>/add-payment/', views.add_payment, name='add_payment'),
]
