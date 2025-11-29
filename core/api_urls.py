from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('patients/', include('patients.api_urls')),
    path('appointments/', include('appointments.api_urls')),
    path('laboratory/', include('laboratory.api_urls')),
    path('pharmacy/', include('pharmacy.api_urls')),
    path('billing/', include('billing.api_urls')),
]
