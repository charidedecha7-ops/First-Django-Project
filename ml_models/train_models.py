import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score, mean_squared_error, r2_score
import joblib
import os

# Create directories
os.makedirs('trained_models', exist_ok=True)

print("=" * 60)
print("ETHIOPIAN HOSPITAL ML MODELS TRAINING")
print("=" * 60)

# ============================================================================
# 1. DISEASE PREDICTION MODEL
# ============================================================================
print("\n1. Training Disease Prediction Model...")
print("-" * 60)

# Load dataset
import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
disease_df = pd.read_csv(os.path.join(base_dir, 'datasets', 'disease_dataset.csv'))
print(f"Dataset loaded: {len(disease_df)} samples")
print(f"Diseases: {disease_df['diagnosis'].unique()}")

# Prepare features
feature_cols = ['age', 'fever', 'headache', 'fatigue', 'cough', 'vomiting', 
                'diarrhea', 'joint_pain', 'rash', 'blood_pressure_systolic',
                'blood_pressure_diastolic', 'glucose_level']

X = disease_df[feature_cols]
y = disease_df['diagnosis']

# Encode gender
gender_encoder = LabelEncoder()
X['gender_encoded'] = gender_encoder.fit_transform(disease_df['gender'])

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {len(X_train)} samples")
print(f"Test set: {len(X_test)} samples")

# Train Random Forest model
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    class_weight='balanced'
)
rf_model.fit(X_train, y_train)

# Evaluate
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Feature importance
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)
print("\nTop 5 Important Features:")
print(feature_importance.head())

# Save model
joblib.dump(rf_model, 'trained_models/disease_prediction_model.pkl')
joblib.dump(gender_encoder, 'trained_models/gender_encoder.pkl')
print("\n✓ Disease prediction model saved!")

# ============================================================================
# 2. PATIENT RISK SCORING MODEL
# ============================================================================
print("\n" + "=" * 60)
print("2. Training Patient Risk Scoring Model...")
print("-" * 60)

# Load dataset
risk_df = pd.read_csv(os.path.join(base_dir, 'datasets', 'risk_dataset.csv'))
print(f"Dataset loaded: {len(risk_df)} samples")

# Prepare features
risk_features = ['age', 'pregnancy', 'glucose', 'blood_pressure_systolic',
                 'blood_pressure_diastolic', 'heart_rate', 'weight', 'bmi']

X_risk = risk_df[risk_features]
y_risk = risk_df['risk_score']

# Split data
X_train_risk, X_test_risk, y_train_risk, y_test_risk = train_test_split(
    X_risk, y_risk, test_size=0.2, random_state=42
)

print(f"Training set: {len(X_train_risk)} samples")
print(f"Test set: {len(X_test_risk)} samples")

# Scale features
scaler = StandardScaler()
X_train_risk_scaled = scaler.fit_transform(X_train_risk)
X_test_risk_scaled = scaler.transform(X_test_risk)

# Train Random Forest Regressor
risk_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
risk_model.fit(X_train_risk_scaled, y_train_risk)

# Evaluate
y_pred_risk = risk_model.predict(X_test_risk_scaled)
mse = mean_squared_error(y_test_risk, y_pred_risk)
r2 = r2_score(y_test_risk, y_pred_risk)
print(f"\nMean Squared Error: {mse:.4f}")
print(f"R² Score: {r2:.4f}")

# Risk distribution
high_risk = (y_test_risk > 0.7).sum()
medium_risk = ((y_test_risk > 0.4) & (y_test_risk <= 0.7)).sum()
low_risk = (y_test_risk <= 0.4).sum()
print(f"\nRisk Distribution (Test Set):")
print(f"  High Risk (>0.7): {high_risk} ({high_risk/len(y_test_risk)*100:.1f}%)")
print(f"  Medium Risk (0.4-0.7): {medium_risk} ({medium_risk/len(y_test_risk)*100:.1f}%)")
print(f"  Low Risk (≤0.4): {low_risk} ({low_risk/len(y_test_risk)*100:.1f}%)")

# Save model
joblib.dump(risk_model, 'trained_models/risk_scoring_model.pkl')
joblib.dump(scaler, 'trained_models/risk_scaler.pkl')
print("\n✓ Risk scoring model saved!")

# ============================================================================
# 3. APPOINTMENT NO-SHOW PREDICTION MODEL
# ============================================================================
print("\n" + "=" * 60)
print("3. Training Appointment No-Show Prediction Model...")
print("-" * 60)

# Load dataset
appointment_df = pd.read_csv(os.path.join(base_dir, 'datasets', 'appointments_dataset.csv'))
print(f"Dataset loaded: {len(appointment_df)} samples")

# Prepare features
appointment_features = ['distance_from_hospital', 'previous_no_shows', 'sms_sent']

# Encode weather condition
weather_encoder = LabelEncoder()
appointment_df['weather_encoded'] = weather_encoder.fit_transform(appointment_df['weather_condition'])

X_appt = appointment_df[appointment_features + ['weather_encoded']]
y_appt = appointment_df['did_come']

# Split data
X_train_appt, X_test_appt, y_train_appt, y_test_appt = train_test_split(
    X_appt, y_appt, test_size=0.2, random_state=42, stratify=y_appt
)

print(f"Training set: {len(X_train_appt)} samples")
print(f"Test set: {len(X_test_appt)} samples")
print(f"No-show rate: {(1 - y_appt.mean()) * 100:.1f}%")

# Train Logistic Regression model
noshow_model = LogisticRegression(
    random_state=42,
    class_weight='balanced',
    max_iter=1000
)
noshow_model.fit(X_train_appt, y_train_appt)

# Evaluate
y_pred_appt = noshow_model.predict(X_test_appt)
accuracy_appt = accuracy_score(y_test_appt, y_pred_appt)
print(f"\nAccuracy: {accuracy_appt:.4f}")
print("\nClassification Report:")
print(classification_report(y_test_appt, y_pred_appt, target_names=['No Show', 'Showed Up']))

# Save model
joblib.dump(noshow_model, 'trained_models/noshow_prediction_model.pkl')
joblib.dump(weather_encoder, 'trained_models/weather_encoder.pkl')
print("\n✓ No-show prediction model saved!")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 60)
print("TRAINING COMPLETE!")
print("=" * 60)
print("\nModels saved in 'trained_models/' directory:")
print("  1. disease_prediction_model.pkl")
print("  2. risk_scoring_model.pkl")
print("  3. noshow_prediction_model.pkl")
print("\nEncoders and scalers also saved for preprocessing.")
print("\nYou can now use these models in your Django application!")
print("=" * 60)
