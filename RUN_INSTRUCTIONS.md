# Ethiopian Hospital Management System - Quick Start Guide

## 🚀 Quick Setup (5 Minutes)

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Generate Datasets and Train ML Models

```bash
# Generate synthetic datasets (2000+ rows each)
cd datasets
python generate_datasets.py
cd ..

# Train machine learning models
cd ml_models
python train_models.py
cd ..
```

This will create:
- `disease_dataset.csv` (2000 rows) - For disease prediction
- `risk_dataset.csv` (2000 rows) - For patient risk scoring
- `appointments_dataset.csv` (2000 rows) - For no-show prediction

And train 3 ML models:
- Disease Prediction Model (Random Forest)
- Risk Scoring Model (Random Forest Regressor)
- No-Show Prediction Model (Logistic Regression)

### Step 3: Setup Database

```bash
# Run migrations
python manage.py migrate

# Load sample data (regions, users, patients)
python manage.py load_sample_data
```

### Step 4: Run the Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

## 🔐 Login Credentials

```
Role          Username    Password
─────────────────────────────────────
Admin         admin       admin123
Doctor        doctor      doctor123
Nurse         nurse       nurse123
Lab Tech      lab         lab123
Pharmacist    pharmacy    pharmacy123
```

## 📋 What You Can Do

### 1. Patient Management
- Register new patients with Ethiopian details (Kebele ID, Woreda, etc.)
- Search patients by name, ID, or phone
- View patient medical history
- Add allergies and medical records

### 2. Appointments
- Book appointments with doctors
- View appointment schedule
- **ML Feature**: Automatic no-show prediction based on:
  - Distance from hospital
  - Weather conditions
  - Previous no-show history
  - SMS reminder status

### 3. Medical Records
- Add diagnosis and treatment
- Record vital signs (BP, temperature, glucose, etc.)
- **ML Feature**: Automatic disease prediction for:
  - Malaria
  - Typhoid
  - TB
  - Pneumonia
  - Diabetes
  - Hypertension

### 4. Laboratory
- Request lab tests
- Update test results
- Track test status

### 5. Pharmacy
- Manage medicine inventory
- Track low stock items
- Create and dispense prescriptions

### 6. Billing
- Generate bills for services
- Record payments
- Track payment status

## 🤖 Machine Learning Features

### Disease Prediction API

```bash
curl -X POST http://localhost:8000/api/patients/1/predict_disease/ \
  -H "Content-Type: application/json" \
  -d '{
    "blood_pressure": "120/80",
    "glucose_level": 95,
    "temperature": 37.5
  }' \
  --user doctor:doctor123
```

### Risk Scoring API

```bash
curl -X POST http://localhost:8000/api/patients/1/calculate_risk/ \
  -H "Content-Type: application/json" \
  -d '{
    "pregnancy": 0,
    "glucose": 180,
    "blood_pressure": 160,
    "heart_rate": 85,
    "weight": 80
  }' \
  --user doctor:doctor123
```

### No-Show Prediction API

```bash
curl -X POST http://localhost:8000/api/appointments/1/predict_noshow/ \
  -H "Content-Type: application/json" \
  --user admin:admin123
```

## 🇪🇹 Ethiopian-Specific Features

1. **Multi-language Support**: English, Amharic (አማርኛ), Afaan Oromoo
2. **Ethiopian Regions & Woredas**: Pre-loaded with major regions
3. **Kebele ID**: Ethiopian identification system
4. **Ethiopian Phone Format**: +251 format
5. **Ethiopian Timezone**: Africa/Addis_Ababa
6. **Common Ethiopian Diseases**: Malaria, Typhoid, TB focus
7. **Ethiopian Calendar Option**: (Can be extended)

## 📊 Sample Data Included

- 5 Regions (Oromia, Amhara, Tigray, SNNPR, Addis Ababa)
- 20+ Woredas
- 5 Staff users (Admin, Doctors, Nurse, Lab, Pharmacy)
- 20 Sample patients
- 3 Trained ML models

## 🔧 Troubleshooting

### Problem: ML models not found
```bash
cd ml_models
python train_models.py
```

### Problem: No patients showing
```bash
python manage.py load_sample_data
```

### Problem: Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Problem: Database errors
```bash
# Delete database and start fresh
rm db.sqlite3
python manage.py migrate
python manage.py load_sample_data
```

## 📁 Project Structure

```
hospital_system/
├── core/                   # Core app (users, auth, dashboard)
├── patients/               # Patient management
├── doctors/                # Doctor & staff management
├── appointments/           # Appointment booking
├── laboratory/             # Lab tests
├── pharmacy/               # Medicine inventory
├── billing/                # Billing & payments
├── ml_models/              # ML models & training scripts
│   ├── trained_models/     # Saved models (.pkl files)
│   ├── train_models.py     # Training script
│   └── predict.py          # Prediction utilities
├── datasets/               # Training datasets
│   ├── disease_dataset.csv
│   ├── risk_dataset.csv
│   ├── appointments_dataset.csv
│   └── generate_datasets.py
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS)
└── manage.py               # Django management
```

## 🚀 Next Steps

1. **Explore the Dashboard**: Login and check different role views
2. **Register a Patient**: Add a new patient with Ethiopian details
3. **Book an Appointment**: Create appointment and see ML prediction
4. **Add Medical History**: Enter symptoms and see disease prediction
5. **Check API**: Test REST API endpoints
6. **Customize**: Modify for your specific hospital needs

## 📚 Documentation

- **Full Deployment Guide**: See `DEPLOYMENT.md`
- **Testing Guide**: See `TESTING.md`
- **Database Schema**: See `database_schema.sql`
- **API Documentation**: Visit `/api/` after running server

## 🆘 Support

For issues:
1. Check `TESTING.md` for common problems
2. Review error logs
3. Ensure all dependencies are installed
4. Verify ML models are trained

## 🎉 Success!

If you see the login page at http://127.0.0.1:8000, you're all set!

Login with `admin` / `admin123` and start exploring the system.

---

**Built for Ethiopian Healthcare** 🇪🇹 🏥
