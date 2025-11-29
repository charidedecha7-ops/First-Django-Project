-- Ethiopian Hospital Management System - Database Schema
-- PostgreSQL/MySQL Compatible

-- ============================================================================
-- CORE TABLES
-- ============================================================================

-- Users table (extends Django's auth_user)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    email VARCHAR(254),
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Custom fields
    role VARCHAR(20) NOT NULL DEFAULT 'receptionist',
    phone VARCHAR(15),
    address TEXT,
    kebele_id VARCHAR(50),
    profile_picture VARCHAR(100),
    is_active_staff BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_username ON users(username);

-- Regions table
CREATE TABLE regions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    name_am VARCHAR(100),
    name_om VARCHAR(100),
    code VARCHAR(10) UNIQUE NOT NULL
);

-- Woredas table
CREATE TABLE woredas (
    id SERIAL PRIMARY KEY,
    region_id INTEGER NOT NULL REFERENCES regions(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    name_am VARCHAR(100),
    name_om VARCHAR(100),
    code VARCHAR(20) UNIQUE NOT NULL
);

CREATE INDEX idx_woredas_region ON woredas(region_id);

-- Audit logs table
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    object_id INTEGER NOT NULL,
    changes JSONB,
    ip_address INET,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);

-- ============================================================================
-- PATIENT MANAGEMENT
-- ============================================================================

-- Patients table
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100),
    date_of_birth DATE NOT NULL,
    gender CHAR(1) NOT NULL CHECK (gender IN ('M', 'F')),
    blood_group VARCHAR(3),
    phone VARCHAR(15) NOT NULL,
    email VARCHAR(254),
    woreda_id INTEGER REFERENCES woredas(id) ON DELETE SET NULL,
    address TEXT NOT NULL,
    kebele_id VARCHAR(50),
    emergency_contact_name VARCHAR(100) NOT NULL,
    emergency_contact_phone VARCHAR(15) NOT NULL,
    photo VARCHAR(100),
    registered_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patients_patient_id ON patients(patient_id);
CREATE INDEX idx_patients_phone ON patients(phone);
CREATE INDEX idx_patients_created_at ON patients(created_at);

-- Medical histories table
CREATE TABLE medical_histories (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    doctor_id INTEGER REFERENCES doctors(id) ON DELETE SET NULL,
    diagnosis VARCHAR(200) NOT NULL,
    symptoms TEXT NOT NULL,
    treatment TEXT NOT NULL,
    notes TEXT,
    visit_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Vitals
    blood_pressure VARCHAR(20),
    temperature DECIMAL(4, 1),
    heart_rate INTEGER,
    weight DECIMAL(5, 2),
    height DECIMAL(5, 2),
    glucose_level DECIMAL(5, 2),
    
    -- ML predictions
    predicted_disease VARCHAR(100),
    risk_score DECIMAL(3, 2),
    
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_medical_histories_patient ON medical_histories(patient_id);
CREATE INDEX idx_medical_histories_visit_date ON medical_histories(visit_date);

-- Allergies table
CREATE TABLE allergies (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    allergen VARCHAR(100) NOT NULL,
    reaction TEXT NOT NULL,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('mild', 'moderate', 'severe')),
    diagnosed_date DATE NOT NULL,
    notes TEXT
);

CREATE INDEX idx_allergies_patient ON allergies(patient_id);

-- ============================================================================
-- DOCTOR & STAFF MANAGEMENT
-- ============================================================================

-- Doctors table
CREATE TABLE doctors (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    specialization VARCHAR(50) NOT NULL,
    qualification VARCHAR(200) NOT NULL,
    experience_years INTEGER NOT NULL DEFAULT 0,
    consultation_fee DECIMAL(10, 2) NOT NULL,
    available_days VARCHAR(100),
    available_time_start TIME NOT NULL,
    available_time_end TIME NOT NULL,
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_doctors_specialization ON doctors(specialization);
CREATE INDEX idx_doctors_is_available ON doctors(is_available);

-- Nurses table
CREATE TABLE nurses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    qualification VARCHAR(200) NOT NULL,
    department VARCHAR(100) NOT NULL,
    shift VARCHAR(20) NOT NULL CHECK (shift IN ('morning', 'afternoon', 'night')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_nurses_department ON nurses(department);

-- ============================================================================
-- APPOINTMENT MANAGEMENT
-- ============================================================================

-- Appointments table
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    appointment_id VARCHAR(20) UNIQUE NOT NULL,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    doctor_id INTEGER NOT NULL REFERENCES doctors(id) ON DELETE CASCADE,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'scheduled',
    notes TEXT,
    
    -- ML prediction fields
    distance_from_hospital DECIMAL(5, 2),
    weather_condition VARCHAR(50),
    sms_sent BOOLEAN NOT NULL DEFAULT FALSE,
    no_show_probability DECIMAL(3, 2),
    
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_appointments_appointment_id ON appointments(appointment_id);
CREATE INDEX idx_appointments_patient ON appointments(patient_id);
CREATE INDEX idx_appointments_doctor ON appointments(doctor_id);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);
CREATE INDEX idx_appointments_status ON appointments(status);

-- ============================================================================
-- LABORATORY MANAGEMENT
-- ============================================================================

-- Lab tests table
CREATE TABLE lab_tests (
    id SERIAL PRIMARY KEY,
    test_id VARCHAR(20) UNIQUE NOT NULL,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    doctor_id INTEGER REFERENCES doctors(id) ON DELETE SET NULL,
    test_name VARCHAR(200) NOT NULL,
    test_type VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    requested_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_date TIMESTAMP,
    results TEXT,
    notes TEXT,
    cost DECIMAL(10, 2) NOT NULL,
    
    -- Common test results
    malaria_test VARCHAR(20),
    rdt_result VARCHAR(20),
    blood_glucose DECIMAL(5, 2),
    hemoglobin DECIMAL(4, 1),
    
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_lab_tests_test_id ON lab_tests(test_id);
CREATE INDEX idx_lab_tests_patient ON lab_tests(patient_id);
CREATE INDEX idx_lab_tests_status ON lab_tests(status);
CREATE INDEX idx_lab_tests_requested_date ON lab_tests(requested_date);

-- ============================================================================
-- PHARMACY MANAGEMENT
-- ============================================================================

-- Medicines table
CREATE TABLE medicines (
    id SERIAL PRIMARY KEY,
    medicine_id VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    generic_name VARCHAR(200),
    manufacturer VARCHAR(200) NOT NULL,
    category VARCHAR(100) NOT NULL,
    unit VARCHAR(50) NOT NULL DEFAULT 'tablet',
    quantity INTEGER NOT NULL DEFAULT 0,
    reorder_level INTEGER NOT NULL DEFAULT 50,
    unit_price DECIMAL(10, 2) NOT NULL,
    expiry_date DATE NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_medicines_medicine_id ON medicines(medicine_id);
CREATE INDEX idx_medicines_name ON medicines(name);
CREATE INDEX idx_medicines_category ON medicines(category);
CREATE INDEX idx_medicines_quantity ON medicines(quantity);

-- Prescriptions table
CREATE TABLE prescriptions (
    id SERIAL PRIMARY KEY,
    prescription_id VARCHAR(20) UNIQUE NOT NULL,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    doctor_id INTEGER REFERENCES doctors(id) ON DELETE SET NULL,
    diagnosis VARCHAR(200) NOT NULL,
    notes TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dispensed_at TIMESTAMP
);

CREATE INDEX idx_prescriptions_prescription_id ON prescriptions(prescription_id);
CREATE INDEX idx_prescriptions_patient ON prescriptions(patient_id);
CREATE INDEX idx_prescriptions_status ON prescriptions(status);

-- Prescription items table
CREATE TABLE prescription_items (
    id SERIAL PRIMARY KEY,
    prescription_id INTEGER NOT NULL REFERENCES prescriptions(id) ON DELETE CASCADE,
    medicine_id INTEGER NOT NULL REFERENCES medicines(id) ON DELETE CASCADE,
    dosage VARCHAR(100) NOT NULL,
    frequency VARCHAR(100) NOT NULL,
    duration VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    instructions TEXT
);

CREATE INDEX idx_prescription_items_prescription ON prescription_items(prescription_id);

-- ============================================================================
-- BILLING MANAGEMENT
-- ============================================================================

-- Bills table
CREATE TABLE bills (
    id SERIAL PRIMARY KEY,
    bill_id VARCHAR(20) UNIQUE NOT NULL,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    appointment_id INTEGER REFERENCES appointments(id) ON DELETE SET NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    paid_amount DECIMAL(10, 2) NOT NULL DEFAULT 0,
    discount DECIMAL(10, 2) NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    payment_method VARCHAR(20),
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_bills_bill_id ON bills(bill_id);
CREATE INDEX idx_bills_patient ON bills(patient_id);
CREATE INDEX idx_bills_status ON bills(status);
CREATE INDEX idx_bills_created_at ON bills(created_at);

-- Bill items table
CREATE TABLE bill_items (
    id SERIAL PRIMARY KEY,
    bill_id INTEGER NOT NULL REFERENCES bills(id) ON DELETE CASCADE,
    description VARCHAR(200) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL
);

CREATE INDEX idx_bill_items_bill ON bill_items(bill_id);

-- Payments table
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    bill_id INTEGER NOT NULL REFERENCES bills(id) ON DELETE CASCADE,
    amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    transaction_id VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_payments_bill ON payments(bill_id);
CREATE INDEX idx_payments_created_at ON payments(created_at);

-- ============================================================================
-- SAMPLE DATA INSERTS
-- ============================================================================

-- Insert sample regions
INSERT INTO regions (name, name_am, name_om, code) VALUES
('Oromia', 'ኦሮሚያ', 'Oromiyaa', 'ORM'),
('Amhara', 'አማራ', 'Amara', 'AMH'),
('Tigray', 'ትግራይ', 'Tigray', 'TIG'),
('SNNPR', 'ደቡብ ብሔሮች', 'SNNPR', 'SNN'),
('Addis Ababa', 'አዲስ አበባ', 'Finfinnee', 'ADD');

-- Insert sample woredas
INSERT INTO woredas (region_id, name, code) VALUES
(1, 'Adama', 'ORM-ADA'),
(1, 'Jimma', 'ORM-JIM'),
(2, 'Bahir Dar', 'AMH-BAH'),
(2, 'Gondar', 'AMH-GON'),
(3, 'Mekelle', 'TIG-MEK'),
(4, 'Hawassa', 'SNN-HAW'),
(5, 'Bole', 'ADD-BOL'),
(5, 'Kirkos', 'ADD-KIR');
