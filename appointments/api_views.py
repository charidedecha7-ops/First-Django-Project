from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Appointment
from .serializers import AppointmentSerializer
import joblib
import os
from django.conf import settings

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    
    @action(detail=True, methods=['post'])
    def predict_noshow(self, request, pk=None):
        appointment = self.get_object()
        
        try:
            model_path = os.path.join(settings.ML_MODELS_PATH, 'noshow_prediction_model.pkl')
            model = joblib.load(model_path)
            
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
            
            return Response({
                'appointment_id': appointment.appointment_id,
                'no_show_probability': float(probability),
                'risk_level': 'High' if probability > 0.7 else 'Medium' if probability > 0.4 else 'Low',
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
