"""
ML Prediction utilities for Ethiopian Hospital System
"""

import joblib
import os
import numpy as np
from django.conf import settings

class DiseasePrediction:
    """Disease prediction using trained ML model"""
    
    def __init__(self):
        model_path = os.path.join(settings.ML_MODELS_PATH, 'disease_prediction_model.pkl')
        self.model = joblib.load(model_path)
        self.diseases = ['Malaria', 'Typhoid', 'TB', 'Pneumonia', 'Diabetes', 'Hypertension']
    
    def predict(self, patient_data):
        """
        Predict disease based on patient symptoms and vitals
        
        Args:
            patient_data: dict with keys:
                - age: int
                - gender: 'M' or 'F'
                - fever: 0 or 1
                - headache: 0 or 1
                - fatigue: 0 or 1
                - cough: 0 or 1
                - vomiting: 0 or 1
                - diarrhea: 0 or 1
                - joint_pain: 0 or 1
                - rash: 0 or 1
                - blood_pressure_systolic: int
                - blood_pressure_diastolic: int
                - glucose_level: float
        
        Returns:
            dict with prediction and confidence
        """
        features = [[
            patient_data['age'],
            patient_data['fever'],
            patient_data['headache'],
            patient_data['fatigue'],
            patient_data['cough'],
            patient_data['vomiting'],
            patient_data['diarrhea'],
            patient_data['joint_pain'],
            patient_data['rash'],
            patient_data['blood_pressure_systolic'],
            patient_data['blood_pressure_diastolic'],
            patient_data['glucose_level'],
            1 if patient_data['gender'] == 'M' else 0,
        ]]
        
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        confidence = max(probabilities)
        
        return {
            'disease': prediction,
            'confidence': float(confidence),
            'all_probabilities': {
                disease: float(prob) 
                for disease, prob in zip(self.diseases, probabilities)
            }
        }


class RiskScoring:
    """Patient risk scoring using trained ML model"""
    
    def __init__(self):
        model_path = os.path.join(settings.ML_MODELS_PATH, 'risk_scoring_model.pkl')
        scaler_path = os.path.join(settings.ML_MODELS_PATH, 'risk_scaler.pkl')
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
    
    def calculate_risk(self, patient_data):
        """
        Calculate patient risk score
        
        Args:
            patient_data: dict with keys:
                - age: int
                - pregnancy: 0 or 1
                - glucose: float
                - blood_pressure_systolic: int
                - blood_pressure_diastolic: int
                - heart_rate: int
                - weight: float
                - bmi: float
        
        Returns:
            dict with risk score and level
        """
        features = [[
            patient_data['age'],
            patient_data.get('pregnancy', 0),
            patient_data['glucose'],
            patient_data['blood_pressure_systolic'],
            patient_data['blood_pressure_diastolic'],
            patient_data['heart_rate'],
            patient_data['weight'],
            patient_data.get('bmi', 25),
        ]]
        
        features_scaled = self.scaler.transform(features)
        risk_score = self.model.predict(features_scaled)[0]
        
        if risk_score > 0.7:
            risk_level = 'High'
            recommendation = 'Immediate medical attention required'
        elif risk_score > 0.4:
            risk_level = 'Medium'
            recommendation = 'Regular monitoring recommended'
        else:
            risk_level = 'Low'
            recommendation = 'Continue routine checkups'
        
        return {
            'risk_score': float(risk_score),
            'risk_level': risk_level,
            'recommendation': recommendation,
        }


class NoShowPrediction:
    """Appointment no-show prediction using trained ML model"""
    
    def __init__(self):
        model_path = os.path.join(settings.ML_MODELS_PATH, 'noshow_prediction_model.pkl')
        self.model = joblib.load(model_path)
    
    def predict_noshow(self, appointment_data):
        """
        Predict if patient will show up for appointment
        
        Args:
            appointment_data: dict with keys:
                - distance_from_hospital: float
                - weather_condition: 'sunny', 'rainy', or 'cloudy'
                - previous_no_shows: int
                - sms_sent: 0 or 1
        
        Returns:
            dict with prediction and probability
        """
        weather_encoding = {
            'sunny': 0,
            'rainy': 1,
            'cloudy': 2,
        }
        
        features = [[
            appointment_data['distance_from_hospital'],
            appointment_data['previous_no_shows'],
            appointment_data['sms_sent'],
            weather_encoding.get(appointment_data['weather_condition'], 0),
        ]]
        
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0]
        
        noshow_prob = probability[0]
        show_prob = probability[1]
        
        return {
            'will_show_up': bool(prediction),
            'show_probability': float(show_prob),
            'noshow_probability': float(noshow_prob),
            'risk_level': 'High' if noshow_prob > 0.7 else 'Medium' if noshow_prob > 0.4 else 'Low',
            'recommendation': 'Send reminder SMS' if noshow_prob > 0.5 else 'No action needed',
        }


# Example usage
if __name__ == '__main__':
    # Disease prediction example
    disease_predictor = DiseasePrediction()
    patient = {
        'age': 25,
        'gender': 'M',
        'fever': 1,
        'headache': 1,
        'fatigue': 1,
        'cough': 0,
        'vomiting': 0,
        'diarrhea': 0,
        'joint_pain': 1,
        'rash': 0,
        'blood_pressure_systolic': 120,
        'blood_pressure_diastolic': 80,
        'glucose_level': 95,
    }
    result = disease_predictor.predict(patient)
    print("Disease Prediction:", result)
    
    # Risk scoring example
    risk_scorer = RiskScoring()
    patient_risk = {
        'age': 55,
        'pregnancy': 0,
        'glucose': 180,
        'blood_pressure_systolic': 160,
        'blood_pressure_diastolic': 100,
        'heart_rate': 85,
        'weight': 80,
        'bmi': 28,
    }
    risk_result = risk_scorer.calculate_risk(patient_risk)
    print("Risk Score:", risk_result)
    
    # No-show prediction example
    noshow_predictor = NoShowPrediction()
    appointment = {
        'distance_from_hospital': 25,
        'weather_condition': 'rainy',
        'previous_no_shows': 2,
        'sms_sent': 0,
    }
    noshow_result = noshow_predictor.predict_noshow(appointment)
    print("No-Show Prediction:", noshow_result)
