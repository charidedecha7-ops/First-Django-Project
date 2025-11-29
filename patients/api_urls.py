from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import PatientViewSet, MedicalHistoryViewSet

router = DefaultRouter()
router.register(r'', PatientViewSet, basename='patient')
router.register(r'medical-history', MedicalHistoryViewSet, basename='medical-history')

urlpatterns = router.urls
