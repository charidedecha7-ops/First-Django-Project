# Ethiopian Hospital Management System - API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Authentication
All API endpoints require authentication using Django's session authentication or basic auth.

```bash
# Using basic auth
curl -u username:password http://localhost:8000/api/patients/

# Using session (login first)
curl -X POST http://localhost:8000/login/ -d "username=admin&password=admin123"
```

## API Endpoints

### 1. Patients API

#### List All Patients
```http
GET /api/patients/
```

**Response:**
```json
{
  "count": 20,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "patient_id": "PAT-000001",
      "first_name": "Abebe",
      "last_name": "Tesfaye",
      "full_name": "Abebe Tesfaye",
      "age": 34,
      "gender": "M",
      "phone": "+251911234567",
      "blood_group": "A+",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Get Single Patient
```http
GET /api/patients/{id}/
```

#### Create Patient
```http
POST /api/patients/
Content-Type: application/json

{
  "first_name": "Tigist",
  "last_name": "Haile",
  "date_of_birth": "1995-05-20",
  "gender": "F",
  "phone": "+251911234567",
  "address": "Addis Ababa, Bole",
  "emergency_contact_name": "Almaz Haile",
  "emergency_contact_phone": "+251911234568"
}
```

#### Update Patient
```http
PUT /api/patients/{id}/
PATCH /api/patients/{id}/
```

#### Delete Patient
```http
DELETE /api/patients/{id}/
```

### 2. Disease Prediction API (ML)

#### Predict Disease
```http
POST /api/patients/{id}/predict_disease/
Content-Type: application/json

{
  "blood_pressure": "120/80",
  "glucose_level": 95,
  "temperature": 37.5
}
```

**Response:**
```json
{
  "patient_id": "PAT-000001",
  "predicted_disease": "Malaria",
  "confidence": 0.85
}
```

**Example with cURL:**
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

**Example with Python:**
```python
import requests

url = "http://localhost:8000/api/patients/1/predict_disease/"
data = {
    "blood_pressure": "120/80",
    "glucose_level": 95,
    "temperature": 37.5
}

response = requests.post(url, json=data, auth=('doctor', 'doctor123'))
print(response.json())
```

### 3. Risk Scoring API (ML)

#### Calculate Patient Risk
```http
POST /api/patients/{id}/calculate_risk/
Content-Type: application/json

{
  "pregnancy": 0,
  "glucose": 180,
  "blood_pressure": 160,
  "heart_rate": 85,
  "weight": 80
}
```

**Response:**
```json
{
  "patient_id": "PAT-000001",
  "risk_score": 0.75,
  "risk_level": "High"
}
```

**Risk Levels:**
- `High`: risk_score > 0.7
- `Medium`: 0.4 < risk_score ≤ 0.7
- `Low`: risk_score ≤ 0.4

**Example:**
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

### 4. Appointments API

#### List Appointments
```http
GET /api/appointments/
```

**Query Parameters:**
- `patient_id`: Filter by patient
- `doctor_id`: Filter by doctor
- `status`: Filter by status (scheduled, confirmed, completed, cancelled, no_show)
- `appointment_date`: Filter by date (YYYY-MM-DD)

**Example:**
```http
GET /api/appointments/?status=scheduled&appointment_date=2024-01-20
```

#### Create Appointment
```http
POST /api/appointments/
Content-Type: application/json

{
  "patient": 1,
  "doctor": 1,
  "appointment_date": "2024-01-20",
  "appointment_time": "10:00:00",
  "reason": "Regular checkup",
  "distance_from_hospital": 15.5,
  "weather_condition": "sunny",
  "sms_sent": true
}
```

**Response:**
```json
{
  "id": 1,
  "appointment_id": "APT-000001",
  "patient": 1,
  "patient_name": "Abebe Tesfaye",
  "doctor": 1,
  "doctor_name": "Dr. Tigist Haile",
  "appointment_date": "2024-01-20",
  "appointment_time": "10:00:00",
  "status": "scheduled",
  "no_show_probability": 0.25,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 5. No-Show Prediction API (ML)

#### Predict Appointment No-Show
```http
POST /api/appointments/{id}/predict_noshow/
```

**Response:**
```json
{
  "appointment_id": "APT-000001",
  "no_show_probability": 0.35,
  "risk_level": "Low"
}
```

**Risk Levels:**
- `High`: probability > 0.7 (Send reminder!)
- `Medium`: 0.4 < probability ≤ 0.7
- `Low`: probability ≤ 0.4

**Example:**
```bash
curl -X POST http://localhost:8000/api/appointments/1/predict_noshow/ \
  -H "Content-Type: application/json" \
  --user admin:admin123
```

### 6. Medical History API

#### List Medical Histories
```http
GET /api/patients/medical-history/
```

**Query Parameters:**
- `patient_id`: Filter by patient

#### Create Medical History
```http
POST /api/patients/medical-history/
Content-Type: application/json

{
  "patient": 1,
  "doctor": 1,
  "diagnosis": "Malaria",
  "symptoms": "Fever, headache, fatigue",
  "treatment": "Artemether-Lumefantrine",
  "blood_pressure": "120/80",
  "temperature": 38.5,
  "glucose_level": 95
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid data provided",
  "details": {
    "field_name": ["This field is required."]
  }
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "error": "An error occurred while processing your request."
}
```

## ML Model Details

### Disease Prediction Model

**Input Features:**
- `age`: Patient age (integer)
- `gender`: M or F
- `fever`: 0 or 1
- `headache`: 0 or 1
- `fatigue`: 0 or 1
- `cough`: 0 or 1
- `vomiting`: 0 or 1
- `diarrhea`: 0 or 1
- `joint_pain`: 0 or 1
- `rash`: 0 or 1
- `blood_pressure_systolic`: integer (e.g., 120)
- `blood_pressure_diastolic`: integer (e.g., 80)
- `glucose_level`: float (e.g., 95.5)

**Output:**
- `disease`: One of [Malaria, Typhoid, TB, Pneumonia, Diabetes, Hypertension]
- `confidence`: Float between 0 and 1

**Accuracy:** ~85%+ (varies by disease)

### Risk Scoring Model

**Input Features:**
- `age`: Patient age (integer)
- `pregnancy`: 0 or 1
- `glucose`: Blood glucose level (float)
- `blood_pressure_systolic`: Systolic BP (integer)
- `blood_pressure_diastolic`: Diastolic BP (integer)
- `heart_rate`: Heart rate (integer)
- `weight`: Weight in kg (float)
- `bmi`: Body Mass Index (float, optional)

**Output:**
- `risk_score`: Float between 0 and 1
- `risk_level`: Low, Medium, or High

### No-Show Prediction Model

**Input Features:**
- `distance_from_hospital`: Distance in km (float)
- `weather_condition`: sunny, rainy, or cloudy
- `previous_no_shows`: Number of previous no-shows (integer)
- `sms_sent`: 0 or 1

**Output:**
- `no_show_probability`: Float between 0 and 1
- `risk_level`: Low, Medium, or High

## Rate Limiting

Currently no rate limiting is implemented. For production, consider:
- 100 requests per hour for authenticated users
- 10 requests per hour for unauthenticated users

## Pagination

All list endpoints support pagination:

```http
GET /api/patients/?page=2&page_size=20
```

**Default page size:** 20

## Filtering and Searching

### Patients
```http
GET /api/patients/?search=Abebe
GET /api/patients/?gender=M
GET /api/patients/?blood_group=A+
```

### Appointments
```http
GET /api/appointments/?status=scheduled
GET /api/appointments/?appointment_date=2024-01-20
GET /api/appointments/?patient_id=1
```

## Ordering

```http
GET /api/patients/?ordering=-created_at
GET /api/appointments/?ordering=appointment_date,appointment_time
```

## Complete Example: Patient Journey

### 1. Register Patient
```bash
curl -X POST http://localhost:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Abebe",
    "last_name": "Tesfaye",
    "date_of_birth": "1990-01-15",
    "gender": "M",
    "phone": "+251911234567",
    "address": "Addis Ababa",
    "emergency_contact_name": "Tigist Tesfaye",
    "emergency_contact_phone": "+251911234568"
  }' \
  --user admin:admin123
```

### 2. Book Appointment
```bash
curl -X POST http://localhost:8000/api/appointments/ \
  -H "Content-Type: application/json" \
  -d '{
    "patient": 1,
    "doctor": 1,
    "appointment_date": "2024-01-20",
    "appointment_time": "10:00:00",
    "reason": "Fever and headache",
    "distance_from_hospital": 10,
    "weather_condition": "sunny",
    "sms_sent": true
  }' \
  --user admin:admin123
```

### 3. Check No-Show Risk
```bash
curl -X POST http://localhost:8000/api/appointments/1/predict_noshow/ \
  --user admin:admin123
```

### 4. Add Medical History
```bash
curl -X POST http://localhost:8000/api/patients/medical-history/ \
  -H "Content-Type: application/json" \
  -d '{
    "patient": 1,
    "doctor": 1,
    "diagnosis": "Suspected Malaria",
    "symptoms": "Fever, headache, fatigue, joint pain",
    "treatment": "Pending lab results",
    "blood_pressure": "120/80",
    "temperature": 38.5,
    "glucose_level": 95
  }' \
  --user doctor:doctor123
```

### 5. Get Disease Prediction
```bash
curl -X POST http://localhost:8000/api/patients/1/predict_disease/ \
  -H "Content-Type: application/json" \
  -d '{
    "blood_pressure": "120/80",
    "glucose_level": 95,
    "temperature": 38.5
  }' \
  --user doctor:doctor123
```

### 6. Calculate Risk Score
```bash
curl -X POST http://localhost:8000/api/patients/1/calculate_risk/ \
  -H "Content-Type: application/json" \
  -d '{
    "pregnancy": 0,
    "glucose": 95,
    "blood_pressure": 120,
    "heart_rate": 75,
    "weight": 70
  }' \
  --user doctor:doctor123
```

## Testing with Postman

1. Import the following collection:
   - Base URL: `http://localhost:8000/api/`
   - Auth: Basic Auth (username/password)

2. Set environment variables:
   - `base_url`: http://localhost:8000
   - `username`: admin
   - `password`: admin123

3. Test endpoints in order:
   - Create patient
   - Create appointment
   - Predict no-show
   - Add medical history
   - Predict disease
   - Calculate risk

## WebSocket Support (Future)

Real-time updates for:
- New appointments
- Lab test results
- Emergency alerts

## API Versioning

Current version: v1 (default)

Future versions will use URL versioning:
```
/api/v2/patients/
```

## Support

For API issues:
- Check authentication credentials
- Verify request format (JSON)
- Check required fields
- Review error messages
- Consult TESTING.md

---

**API Version:** 1.0  
**Last Updated:** 2024  
**Status:** Production Ready
