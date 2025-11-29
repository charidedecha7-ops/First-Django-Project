import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Ethiopian regions and woredas
regions_woredas = {
    'Oromia': ['Adama', 'Jimma', 'Nekemte', 'Dire Dawa', 'Harar'],
    'Amhara': ['Bahir Dar', 'Gondar', 'Debre Markos', 'Dessie', 'Debre Birhan'],
    'Tigray': ['Mekelle', 'Axum', 'Shire', 'Adigrat', 'Wukro'],
    'SNNPR': ['Hawassa', 'Arba Minch', 'Wolaita', 'Dilla', 'Hosanna'],
    'Addis Ababa': ['Bole', 'Kirkos', 'Yeka', 'Arada', 'Lideta'],
}

# Disease patterns
disease_patterns = {
    'Malaria': {
        'age_range': (15, 50),
        'symptoms': {'fever': 0.95, 'headache': 0.9, 'fatigue': 0.9, 'joint_pain': 0.7, 'vomiting': 0.3},
        'malaria_test': 'positive',
        'bp_systolic': (110, 130),
        'bp_diastolic': (70, 85),
        'glucose': (85, 100),
    },
    'Typhoid': {
        'age_range': (20, 55),
        'symptoms': {'fever': 0.95, 'headache': 0.85, 'fatigue': 0.9, 'cough': 0.6, 'vomiting': 0.7, 'diarrhea': 0.6},
        'malaria_test': 'negative',
        'bp_systolic': (120, 135),
        'bp_diastolic': (75, 90),
        'glucose': (90, 110),
    },
    'TB': {
        'age_range': (25, 65),
        'symptoms': {'cough': 0.95, 'fatigue': 0.9, 'fever': 0.7, 'headache': 0.5},
        'malaria_test': 'negative',
        'bp_systolic': (115, 130),
        'bp_diastolic': (70, 85),
        'glucose': (85, 105),
    },
    'Pneumonia': {
        'age_range': (5, 70),
        'symptoms': {'cough': 0.95, 'fever': 0.9, 'fatigue': 0.85, 'headache': 0.6},
        'malaria_test': 'negative',
        'bp_systolic': (120, 140),
        'bp_diastolic': (75, 90),
        'glucose': (90, 110),
    },
    'Diabetes': {
        'age_range': (35, 75),
        'symptoms': {'fatigue': 0.8, 'cough': 0.3, 'headache': 0.4},
        'malaria_test': 'negative',
        'bp_systolic': (135, 160),
        'bp_diastolic': (85, 105),
        'glucose': (180, 250),
    },
    'Hypertension': {
        'age_range': (40, 80),
        'symptoms': {'headache': 0.7, 'fatigue': 0.6},
        'malaria_test': 'negative',
        'bp_systolic': (150, 190),
        'bp_diastolic': (95, 120),
        'glucose': (95, 120),
    },
}

def generate_disease_dataset(n_samples=2000):
    data = []
    diseases = list(disease_patterns.keys())
    
    for _ in range(n_samples):
        disease = random.choice(diseases)
        pattern = disease_patterns[disease]
        
        # Generate patient data
        age = random.randint(*pattern['age_range'])
        gender = random.choice(['M', 'F'])
        region = random.choice(list(regions_woredas.keys()))
        woreda = random.choice(regions_woredas[region])
        
        # Generate symptoms
        symptoms = {}
        for symptom in ['fever', 'headache', 'fatigue', 'cough', 'vomiting', 'diarrhea', 'joint_pain', 'rash']:
            prob = pattern['symptoms'].get(symptom, 0.1)
            symptoms[symptom] = 1 if random.random() < prob else 0
        
        # Generate test results
        malaria_test = pattern['malaria_test']
        rdt_result = malaria_test
        
        # Generate vitals
        bp_systolic = random.randint(*pattern['bp_systolic'])
        bp_diastolic = random.randint(*pattern['bp_diastolic'])
        glucose = random.randint(*pattern['glucose'])
        
        row = {
            'age': age,
            'gender': gender,
            'region': region,
            'woreda': woreda,
            **symptoms,
            'malaria_test': malaria_test,
            'rdt_result': rdt_result,
            'blood_pressure_systolic': bp_systolic,
            'blood_pressure_diastolic': bp_diastolic,
            'glucose_level': glucose,
            'diagnosis': disease,
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    return df

def generate_risk_dataset(n_samples=2000):
    data = []
    
    for _ in range(n_samples):
        age = random.randint(18, 80)
        pregnancy = 1 if random.random() < 0.15 and age < 45 else 0
        glucose = random.randint(70, 250)
        bp_systolic = random.randint(90, 190)
        bp_diastolic = random.randint(60, 120)
        heart_rate = random.randint(55, 120)
        weight = random.randint(45, 120)
        height = random.randint(150, 190)
        bmi = weight / ((height/100) ** 2)
        
        # Calculate risk score
        risk_score = 0.0
        
        # Age risk
        if age > 60:
            risk_score += 0.2
        elif age > 45:
            risk_score += 0.1
        
        # Pregnancy risk
        if pregnancy:
            risk_score += 0.15
            if age > 35:
                risk_score += 0.1
        
        # Glucose risk
        if glucose > 180:
            risk_score += 0.25
        elif glucose > 140:
            risk_score += 0.15
        elif glucose < 70:
            risk_score += 0.1
        
        # Blood pressure risk
        if bp_systolic > 160 or bp_diastolic > 100:
            risk_score += 0.25
        elif bp_systolic > 140 or bp_diastolic > 90:
            risk_score += 0.15
        
        # Heart rate risk
        if heart_rate > 100 or heart_rate < 60:
            risk_score += 0.1
        
        # BMI risk
        if bmi > 30:
            risk_score += 0.15
        elif bmi < 18.5:
            risk_score += 0.1
        
        risk_score = min(risk_score, 1.0)
        
        row = {
            'age': age,
            'pregnancy': pregnancy,
            'glucose': glucose,
            'blood_pressure_systolic': bp_systolic,
            'blood_pressure_diastolic': bp_diastolic,
            'heart_rate': heart_rate,
            'weight': weight,
            'height': height,
            'bmi': round(bmi, 2),
            'risk_score': round(risk_score, 2),
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    return df

def generate_appointment_dataset(n_samples=2000):
    data = []
    start_date = datetime(2023, 1, 1)
    
    for i in range(n_samples):
        patient_id = f'PAT-{i+1:06d}'
        appointment_date = start_date + timedelta(days=random.randint(0, 365))
        distance = round(random.uniform(0.5, 50), 2)
        weather = random.choice(['sunny', 'rainy', 'cloudy'])
        
        # Calculate previous no-shows (simulate history)
        previous_no_shows = random.randint(0, 5)
        sms_sent = random.choice([0, 1])
        
        # Calculate probability of showing up
        show_prob = 0.8
        
        if distance > 30:
            show_prob -= 0.2
        elif distance > 15:
            show_prob -= 0.1
        
        if weather == 'rainy':
            show_prob -= 0.15
        
        if previous_no_shows > 2:
            show_prob -= 0.2
        elif previous_no_shows > 0:
            show_prob -= 0.1
        
        if sms_sent:
            show_prob += 0.15
        
        show_prob = max(0.1, min(0.95, show_prob))
        did_come = 1 if random.random() < show_prob else 0
        
        row = {
            'patient_id': patient_id,
            'appointment_date': appointment_date.strftime('%Y-%m-%d'),
            'distance_from_hospital': distance,
            'weather_condition': weather,
            'previous_no_shows': previous_no_shows,
            'sms_sent': sms_sent,
            'did_come': did_come,
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    return df

if __name__ == '__main__':
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("Generating disease prediction dataset...")
    disease_df = generate_disease_dataset(2000)
    disease_df.to_csv(os.path.join(script_dir, 'disease_dataset.csv'), index=False)
    print(f"Disease dataset created: {len(disease_df)} rows")
    print(disease_df['diagnosis'].value_counts())
    
    print("\nGenerating risk scoring dataset...")
    risk_df = generate_risk_dataset(2000)
    risk_df.to_csv(os.path.join(script_dir, 'risk_dataset.csv'), index=False)
    print(f"Risk dataset created: {len(risk_df)} rows")
    print(f"High risk patients (>0.7): {len(risk_df[risk_df['risk_score'] > 0.7])}")
    
    print("\nGenerating appointment no-show dataset...")
    appointment_df = generate_appointment_dataset(2000)
    appointment_df.to_csv(os.path.join(script_dir, 'appointments_dataset.csv'), index=False)
    print(f"Appointment dataset created: {len(appointment_df)} rows")
    print(f"No-show rate: {(1 - appointment_df['did_come'].mean()) * 100:.1f}%")
    
    print("\nAll datasets generated successfully!")
