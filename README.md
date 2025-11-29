# Ethiopian Hospital Management System

A comprehensive Hospital Management System built with Django and Machine Learning, designed specifically for Ethiopian healthcare facilities.

## Features

### Core Modules
- Patient Registration & Medical Records
- Doctor & Staff Management
- Appointment Booking System
- Laboratory Test Management
- Pharmacy/Drug Store Inventory
- Billing & Payment Tracking
- Diagnosis/Treatment History
- Role-Based Access Control

### Machine Learning Models
1. **Disease Prediction** - Predicts common Ethiopian diseases (Malaria, Typhoid, TB, Pneumonia, Diabetes, Hypertension)
2. **Patient Risk Scoring** - Identifies high-risk patients
3. **Appointment No-Show Prediction** - Predicts patient attendance

### Ethiopia-Specific Features
- Multi-language support (English, Amharic, Afaan Oromoo)
- Ethiopian timezone (Africa/Addis_Ababa)
- Ethiopian phone number format
- Kebele ID support
- Ethiopian calendar option
- Common Ethiopian diseases focus

## Tech Stack
- Django 4.2+
- Django REST Framework
- PostgreSQL
- scikit-learn
- pandas, numpy
- Bootstrap 5

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data
python manage.py loaddata sample_data.json

# Train ML models
python ml_models/train_models.py

# Run server
python manage.py runserver
```

## Project Structure
```
hospital_system/
├── core/                  # Core Django app
├── patients/              # Patient management
├── doctors/               # Doctor & staff management
├── appointments/          # Appointment booking
├── laboratory/            # Lab test management
├── pharmacy/              # Pharmacy inventory
├── billing/               # Billing & payments
├── ml_models/             # Machine learning models
├── datasets/              # Training datasets
└── templates/             # HTML templates
```

## Default Login Credentials
- Admin: admin@hospital.et / admin123
- Doctor: doctor@hospital.et / doctor123
- Nurse: nurse@hospital.et / nurse123
- Lab: lab@hospital.et / lab123
- Pharmacy: pharmacy@hospital.et / pharmacy123

## Deployment
See DEPLOYMENT.md for detailed deployment instructions.
