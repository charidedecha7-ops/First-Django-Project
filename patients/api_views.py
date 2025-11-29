from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Patient, MedicalHistory
from .serializers import PatientSerializer, MedicalHistorySerializer
import joblib
import os
from django.conf import settings

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
    @action(detail=True, methods=['post'])
    def predict_disease(self, request, pk=None):
        patient = self.get_object()
        
        try:
            model_path = os.path.join(settings.ML_MODELS_PATH, 'disease_prediction_model.pkl')
            model = joblib.load(model_path)
            
            # Extract features from request
            features = [[
                patient.age,
                1 if patient.gender == 'M' else 0,
                float(request.data.get('blood_pressure', 120)),
                float(request.data.get('glucose_level', 100)),
                float(request.data.get('temperature', 37)),
            ]]
            
            prediction = model.predict(features)
            probability = model.predict_proba(features)
            
            return Response({
                'patient_id': patient.patient_id,
                'predicted_disease': prediction[0],
                'confidence': float(max(probability[0])),
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def calculate_risk(self, request, pk=None):
        patient = self.get_object()
        
        try:
            model_path = os.path.join(settings.ML_MODELS_PATH, 'risk_scoring_model.pkl')
            model = joblib.load(model_path)
            
            features = [[
                patient.age,
                int(request.data.get('pregnancy', 0)),
                float(request.data.get('glucose', 100)),
                float(request.data.get('blood_pressure', 120)),
                float(request.data.get('heart_rate', 75)),
                float(request.data.get('weight', 70)),
            ]]
            
            risk_score = model.predict(features)[0]
            
            return Response({
                'patient_id': patient.patient_id,
                'risk_score': float(risk_score),
                'risk_level': 'High' if risk_score > 0.7 else 'Medium' if risk_score > 0.4 else 'Low',
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class MedicalHistoryViewSet(viewsets.ModelViewSet):
    queryset = MedicalHistory.objects.all()
    serializer_class = MedicalHistorySerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset
