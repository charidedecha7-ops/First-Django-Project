# Deployment Guide - Ethiopian Hospital Management System

## Prerequisites

- Python 3.9+
- PostgreSQL 12+ (or SQLite for development)
- Redis (for Celery tasks)
- Git

## Local Development Setup

### 1. Clone and Setup Environment

```bash
# Clone repository
git clone <repository-url>
cd hospital_system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env file with your settings
# For development, you can use SQLite (default)
```

### 3. Generate Datasets and Train ML Models

```bash
# Generate synthetic datasets
cd datasets
python generate_datasets.py
cd ..

# Train ML models
cd ml_models
python train_models.py
cd ..
```

### 4. Setup Database

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata sample_data.json
```

### 5. Run Development Server

```bash
# Start Django server
python manage.py runserver

# In another terminal, start Celery (optional)
celery -A hospital_system worker -l info
```

Visit: http://127.0.0.1:8000

## Production Deployment

### Option 1: PythonAnywhere

1. **Create Account**: Sign up at https://www.pythonanywhere.com

2. **Upload Code**:
```bash
git clone <your-repo-url>
cd hospital_system
```

3. **Setup Virtual Environment**:
```bash
mkvirtualenv --python=/usr/bin/python3.9 hospital_env
pip install -r requirements.txt
```

4. **Configure Web App**:
- Go to Web tab
- Add new web app
- Choose Manual configuration
- Python 3.9
- Set source code directory
- Set virtualenv path

5. **Configure WSGI**:
```python
import sys
import os

path = '/home/yourusername/hospital_system'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'hospital_system.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

6. **Setup Static Files**:
```bash
python manage.py collectstatic
```

7. **Setup Database**:
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Option 2: Railway

1. **Install Railway CLI**:
```bash
npm install -g @railway/cli
```

2. **Login and Initialize**:
```bash
railway login
railway init
```

3. **Add PostgreSQL**:
```bash
railway add postgresql
```

4. **Deploy**:
```bash
railway up
```

5. **Run Migrations**:
```bash
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

### Option 3: AWS EC2

1. **Launch EC2 Instance**:
- Ubuntu 22.04 LTS
- t2.medium or larger
- Open ports: 22, 80, 443

2. **Connect and Setup**:
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3-pip python3-venv postgresql nginx redis-server -y

# Clone repository
git clone <your-repo-url>
cd hospital_system

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

3. **Configure PostgreSQL**:
```bash
sudo -u postgres psql
CREATE DATABASE hospital_db;
CREATE USER hospital_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE hospital_db TO hospital_user;
\q
```

4. **Configure Environment**:
```bash
# Edit .env file
nano .env

# Set production values:
DEBUG=False
ALLOWED_HOSTS=your-domain.com,your-ec2-ip
DB_ENGINE=django.db.backends.postgresql
DB_NAME=hospital_db
DB_USER=hospital_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

5. **Setup Application**:
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Generate datasets and train models
cd datasets && python generate_datasets.py && cd ..
cd ml_models && python train_models.py && cd ..
```

6. **Configure Gunicorn**:
```bash
# Create systemd service
sudo nano /etc/systemd/system/hospital.service
```

```ini
[Unit]
Description=Hospital Management System
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/hospital_system
Environment="PATH=/home/ubuntu/hospital_system/venv/bin"
ExecStart=/home/ubuntu/hospital_system/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/home/ubuntu/hospital_system/hospital.sock \
          hospital_system.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl start hospital
sudo systemctl enable hospital
```

7. **Configure Nginx**:
```bash
sudo nano /etc/nginx/sites-available/hospital
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ubuntu/hospital_system;
    }
    
    location /media/ {
        root /home/ubuntu/hospital_system;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/hospital_system/hospital.sock;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/hospital /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

8. **Setup SSL (Optional)**:
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

## Database Schema (PostgreSQL)

```sql
-- Run this if you need to manually create tables
-- Django migrations will handle this automatically

-- Users table (extends Django's auth_user)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254),
    role VARCHAR(20),
    phone VARCHAR(15),
    address TEXT,
    kebele_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Patients table
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    gender CHAR(1),
    phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- See models.py for complete schema
```

## Monitoring and Maintenance

### Backup Database

```bash
# PostgreSQL backup
pg_dump -U hospital_user hospital_db > backup_$(date +%Y%m%d).sql

# Restore
psql -U hospital_user hospital_db < backup_20240101.sql
```

### Update Application

```bash
cd hospital_system
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart hospital
```

### Monitor Logs

```bash
# Application logs
sudo journalctl -u hospital -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

## Troubleshooting

### Issue: Static files not loading
```bash
python manage.py collectstatic --clear
sudo systemctl restart nginx
```

### Issue: Database connection error
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -U hospital_user -d hospital_db -h localhost
```

### Issue: ML models not found
```bash
cd ml_models
python train_models.py
```

## Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use strong database passwords
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall (UFW)
- [ ] Regular backups
- [ ] Update dependencies regularly
- [ ] Monitor logs for suspicious activity

## Support

For issues and questions:
- GitHub Issues: <repository-url>/issues
- Email: support@hospital.et
- Documentation: <repository-url>/wiki
