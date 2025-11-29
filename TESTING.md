# Testing Guide - Ethiopian Hospital Management System

## Quick Start Testing

### 1. Setup Test Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Generate datasets
cd datasets
python generate_datasets.py
cd ..

# Train ML models
cd ml_models
python train_models.py
cd ..

# Setup database
python manage.py migrate
python manage.py load_sample_data

# Run server
python manage.py runserver
```

### 2. Login Credentials

```
Admin:     admin / admin123
Doctor:    doctor / doctor123
Nurse:     nurse / nurse123
Lab Tech:  lab / lab123
Pharmacy:  pharmacy / pharmacy123
```

## Testing Scenarios

### A. Patient Management

#### Test 1: Register New Patient
1. Login as admin or receptionist
2. Navigate to Patients → Register Patient
3. Fill in patient details:
   - First Name: Abebe
   - Last Name: Tesfaye
   - Date of Birth: 1990-01-15
   - Gender: Male
   - Phone: +251911234567
   - Address: Addis Ababa, Bole
4. Submit form
5. Verify patient ID is generated (PAT-XXXXXX)

#### Test 2: Search Patient
1. Go to Patients list
2. Search by name, phone, or patient ID
3. Verify search results

#### Test 3: Add Medical History
1. Open patient detail page
2. Click "Add Medical History"
3. Enter symptoms and vitals:
   - Fever: Yes
   - Headache: Yes
   - Blood Pressure: 120/80
   - Glucose: 95
4. Submit
5. Verify ML disease prediction appears

### B. Appointment Management

#### Test 4: Create Appointment
1. Login as receptionist
2. Navigate to Appointments → New Appointment
3. Select patient and doctor
4. Choose date and time
5. Enter reason for visit
6. Set distance from hospital: 15 km
7. Weather condition: Sunny
8. SMS sent: Yes
9. Submit
10. Verify no-show probability is calculated

#### Test 5: Doctor View Appointments
1. Login as doctor
2. View dashboard
3. Verify today's appointments are listed
4. Click on appointment to view details

### C. Laboratory Tests

#### Test 6: Request Lab Test
1. Login as doctor
2. Navigate to Laboratory → New Test
3. Select patient
4. Choose test type (e.g., Malaria Test)
5. Submit request
6. Verify test ID is generated

#### Test 7: Update Test Results
1. Login as lab technician
2. View pending tests
3. Select a test
4. Enter results
5. Mark as completed
6. Verify status changes

### D. Pharmacy Management

#### Test 8: View Medicine Inventory
1. Login as pharmacist
2. Navigate to Pharmacy → Medicines
3. View all medicines
4. Filter by low stock
5. Verify medicines below reorder level are shown

#### Test 9: Create Prescription
1. Login as doctor
2. Create new prescription for patient
3. Add medicines with dosage
4. Submit
5. Verify prescription ID is generated

### E. Billing

#### Test 10: Generate Bill
1. Navigate to Billing
2. Create new bill for patient
3. Add items (consultation, tests, medicines)
4. Calculate total
5. Submit
6. Verify bill ID is generated

#### Test 11: Record Payment
1. Open bill detail
2. Click "Add Payment"
3. Enter amount and payment method
4. Submit
5. Verify bill status updates (partial/paid)

### F. Machine Learning Features

#### Test 12: Disease Prediction
1. Add medical history with symptoms
2. Enter vitals:
   - Age: 25
   - Fever: Yes
   - Headache: Yes
   - Joint Pain: Yes
   - BP: 120/80
   - Glucose: 95
3. Submit
4. Verify predicted disease (should predict Malaria)
5. Check confidence score

#### Test 13: Risk Scoring
1. Use API endpoint: `/api/patients/{id}/calculate_risk/`
2. POST data:
```json
{
  "pregnancy": 0,
  "glucose": 180,
  "blood_pressure": 160,
  "heart_rate": 85,
  "weight": 80
}
```
3. Verify risk score is returned
4. Check risk level (High/Medium/Low)

#### Test 14: No-Show Prediction
1. Create appointment with:
   - Distance: 30 km
   - Weather: Rainy
   - Previous no-shows: 2
   - SMS sent: No
2. Verify high no-show probability
3. Check recommendation to send SMS

## API Testing

### Using cURL

#### Get Patients List
```bash
curl -X GET http://localhost:8000/api/patients/ \
  -H "Content-Type: application/json" \
  --user admin:admin123
```

#### Disease Prediction
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

#### Risk Calculation
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

#### No-Show Prediction
```bash
curl -X POST http://localhost:8000/api/appointments/1/predict_noshow/ \
  -H "Content-Type: application/json" \
  --user admin:admin123
```

### Using Python Requests

```python
import requests

# Login
session = requests.Session()
session.auth = ('admin', 'admin123')

# Get patients
response = session.get('http://localhost:8000/api/patients/')
print(response.json())

# Disease prediction
data = {
    'blood_pressure': '120/80',
    'glucose_level': 95,
    'temperature': 37.5
}
response = session.post(
    'http://localhost:8000/api/patients/1/predict_disease/',
    json=data
)
print(response.json())
```

## ML Model Testing

### Test Disease Prediction Model

```bash
cd ml_models
python predict.py
```

Expected output:
```
Disease Prediction: {
  'disease': 'Malaria',
  'confidence': 0.85,
  'all_probabilities': {...}
}
```

### Test Risk Scoring Model

```python
from ml_models.predict import RiskScoring

scorer = RiskScoring()
result = scorer.calculate_risk({
    'age': 55,
    'pregnancy': 0,
    'glucose': 180,
    'blood_pressure_systolic': 160,
    'blood_pressure_diastolic': 100,
    'heart_rate': 85,
    'weight': 80,
    'bmi': 28
})
print(result)
```

Expected output:
```
{
  'risk_score': 0.75,
  'risk_level': 'High',
  'recommendation': 'Immediate medical attention required'
}
```

## Performance Testing

### Load Testing with Apache Bench

```bash
# Test homepage
ab -n 1000 -c 10 http://localhost:8000/

# Test API endpoint
ab -n 100 -c 5 -A admin:admin123 http://localhost:8000/api/patients/
```

### Database Query Performance

```python
# In Django shell
python manage.py shell

from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as queries:
    # Your code here
    patients = Patient.objects.select_related('woreda').all()[:10]
    for p in patients:
        print(p.full_name)

print(f"Number of queries: {len(queries)}")
```

## Common Issues and Solutions

### Issue 1: ML Model Not Found
```
Error: [Errno 2] No such file or directory: 'ml_models/trained_models/disease_prediction_model.pkl'
```
**Solution**: Run `cd ml_models && python train_models.py`

### Issue 2: Database Migration Error
```
Error: django.db.utils.OperationalError: no such table: patients
```
**Solution**: Run `python manage.py migrate`

### Issue 3: Static Files Not Loading
```
Error: 404 on /static/css/style.css
```
**Solution**: Run `python manage.py collectstatic`

### Issue 4: Permission Denied
```
Error: User does not have permission to access this resource
```
**Solution**: Check user role and login with appropriate credentials

## Test Coverage

To run automated tests (when implemented):

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test patients

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## Security Testing

### Test Authentication
1. Try accessing protected pages without login
2. Verify redirect to login page
3. Test with wrong credentials
4. Verify error message

### Test Authorization
1. Login as nurse
2. Try to access admin-only pages
3. Verify access denied

### Test SQL Injection
1. Try entering SQL in search fields:
   - `' OR '1'='1`
   - `'; DROP TABLE patients; --`
2. Verify Django ORM prevents injection

### Test XSS
1. Try entering JavaScript in text fields:
   - `<script>alert('XSS')</script>`
2. Verify output is escaped

## Monitoring and Logging

### View Application Logs

```bash
# Django logs
tail -f logs/django.log

# Access logs
tail -f logs/access.log

# Error logs
tail -f logs/error.log
```

### Monitor Database

```sql
-- PostgreSQL
SELECT * FROM pg_stat_activity;

-- Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## Conclusion

This testing guide covers the main functionality of the Ethiopian Hospital Management System. For production deployment, implement automated testing, continuous integration, and monitoring solutions.
