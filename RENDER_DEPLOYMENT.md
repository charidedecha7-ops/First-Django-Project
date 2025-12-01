# Deploy Ethiopian Hospital Management System on Render - Step by Step

## Prerequisites

- GitHub account with the repository pushed
- Render account (free tier available)
- PostgreSQL database (Render provides free tier)

---

## Step 1: Prepare Your Repository

### 1.1 Ensure All Files Are Committed
```bash
git status
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 1.2 Verify Key Files Exist
- ✅ `Procfile` - Process file for Render
- ✅ `requirements.txt` - Python dependencies
- ✅ `runtime.txt` - Python version
- ✅ `render.yaml` - Render configuration

---

## Step 2: Create Render Account

1. Go to https://render.com
2. Click "Sign Up"
3. Sign up with GitHub (recommended)
4. Authorize Render to access your GitHub account

---

## Step 3: Create PostgreSQL Database

### 3.1 Create Database
1. In Render dashboard, click "New +"
2. Select "PostgreSQL"
3. Fill in details:
   - **Name**: `hospital-db`
   - **Database**: `hospital_db`
   - **User**: `hospital_user`
   - **Region**: Choose closest to you
   - **Plan**: Free (for testing)
4. Click "Create Database"

### 3.2 Save Database Credentials
Copy and save:
- **Internal Database URL** (for internal connections)
- **External Database URL** (for external connections)

Example format:
```
postgresql://user:password@host:5432/database
```

---

## Step 4: Create Web Service

### 4.1 Create New Web Service
1. In Render dashboard, click "New +"
2. Select "Web Service"
3. Connect your GitHub repository:
   - Click "Connect account" if needed
   - Select `Ethiopia-Hospital` repository
   - Click "Connect"

### 4.2 Configure Web Service
Fill in the following:

**Basic Settings:**
- **Name**: `hospital-system` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Same as database
- **Branch**: `main`
- **Build Command**: 
  ```
  pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
  ```
- **Start Command**: 
  ```
  gunicorn hospital_system.wsgi:application
  ```

### 4.3 Add Environment Variables
Click "Advanced" and add these environment variables:

```
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host:5432/database
REDIS_URL=redis://localhost:6379/0
```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4.4 Select Plan
- Choose "Free" for testing
- Click "Create Web Service"

---

## Step 5: Configure Django Settings

### 5.1 Update `hospital_system/settings.py`

Add/Update these settings:

```python
import os
import dj_database_url

# Security
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CORS
CSRF_TRUSTED_ORIGINS = [
    'https://your-app-name.onrender.com',
]

# Email (optional)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### 5.2 Update `requirements.txt`

Ensure these are included:
```
Django>=4.2,<5.0
djangorestframework>=3.14
gunicorn>=21.0
whitenoise>=6.0
dj-database-url>=2.0
psycopg2-binary>=2.9
python-decouple>=3.8
Pillow>=10.0
scikit-learn>=1.3
pandas>=2.0
numpy>=1.24
joblib>=1.3
django-cors-headers>=4.0
django-filter>=23.0
```

### 5.3 Verify `Procfile`

Should contain:
```
web: gunicorn hospital_system.wsgi:application
```

### 5.4 Verify `runtime.txt`

Should contain:
```
python-3.11.7
```

---

## Step 6: Deploy

### 6.1 Push Changes to GitHub
```bash
git add .
git commit -m "Configure for Render deployment"
git push origin main
```

### 6.2 Render Auto-Deploy
Render will automatically:
1. Detect the push
2. Build the application
3. Run migrations
4. Collect static files
5. Start the web service

### 6.3 Monitor Deployment
1. Go to your Web Service in Render
2. Click "Logs" to see deployment progress
3. Wait for "Build successful" message

---

## Step 7: Run Initial Setup

### 7.1 Access Shell
1. In Render dashboard, go to your Web Service
2. Click "Shell" tab
3. Run these commands:

```bash
# Create superuser
python manage.py createsuperuser

# Load sample data
python manage.py load_sample_data

# Add doctors
python manage.py add_doctors

# Add patients
python manage.py add_patients

# Add appointments
python manage.py add_appointments

# Add lab tests
python manage.py add_lab_tests

# Add medicines
python manage.py add_medicines

# Add bills
python manage.py add_bills
```

---

## Step 8: Access Your Application

### 8.1 Get Your URL
1. In Render dashboard, find your Web Service
2. Copy the URL (e.g., `https://hospital-system.onrender.com`)

### 8.2 Access Application
- **Main Site**: `https://hospital-system.onrender.com`
- **Admin Panel**: `https://hospital-system.onrender.com/admin`
- **API**: `https://hospital-system.onrender.com/api`

### 8.3 Login
Use the superuser credentials you created:
- **Username**: admin
- **Password**: (your chosen password)

---

## Step 9: Configure Custom Domain (Optional)

### 9.1 Add Custom Domain
1. In Web Service settings, go to "Custom Domains"
2. Click "Add Custom Domain"
3. Enter your domain (e.g., `hospital.example.com`)
4. Follow DNS configuration instructions

---

## Step 10: Troubleshooting

### Issue: Build Failed
**Solution:**
1. Check logs for errors
2. Verify `requirements.txt` syntax
3. Ensure all dependencies are listed
4. Check Python version compatibility

### Issue: Database Connection Error
**Solution:**
1. Verify `DATABASE_URL` environment variable
2. Check database is running
3. Ensure credentials are correct
4. Test connection string locally

### Issue: Static Files Not Loading
**Solution:**
1. Run `python manage.py collectstatic`
2. Verify `STATIC_ROOT` setting
3. Check `STATICFILES_STORAGE` setting
4. Ensure WhiteNoise is installed

### Issue: 500 Error
**Solution:**
1. Check application logs
2. Verify `DEBUG=False` settings
3. Check `ALLOWED_HOSTS` configuration
4. Verify database migrations ran

### Issue: Media Files Not Uploading
**Solution:**
1. Use cloud storage (AWS S3, Cloudinary)
2. Configure storage backend
3. Set environment variables
4. Test upload functionality

---

## Step 11: Production Checklist

- ✅ `DEBUG = False`
- ✅ `SECRET_KEY` set via environment variable
- ✅ `ALLOWED_HOSTS` configured
- ✅ Database migrations applied
- ✅ Static files collected
- ✅ Superuser created
- ✅ Sample data loaded
- ✅ HTTPS enabled
- ✅ Email configured (optional)
- ✅ Backups configured

---

## Step 12: Monitor Application

### 12.1 View Logs
1. Go to Web Service
2. Click "Logs" tab
3. Monitor for errors

### 12.2 Set Up Alerts
1. Go to Web Service settings
2. Configure notifications
3. Set alert thresholds

### 12.3 Monitor Performance
1. Check CPU usage
2. Monitor memory usage
3. Track response times

---

## Step 13: Backup & Maintenance

### 13.1 Database Backups
1. In Render dashboard, go to PostgreSQL
2. Click "Backups"
3. Configure automatic backups

### 13.2 Update Dependencies
Regularly update `requirements.txt`:
```bash
pip list --outdated
pip install --upgrade package-name
```

### 13.3 Monitor Logs
Check logs regularly for:
- Errors
- Warnings
- Performance issues

---

## Environment Variables Reference

```
DEBUG=False
SECRET_KEY=your-generated-secret-key
ALLOWED_HOSTS=hospital-system.onrender.com
DATABASE_URL=postgresql://user:password@host:5432/database
REDIS_URL=redis://localhost:6379/0
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## Useful Commands

### Deploy Latest Changes
```bash
git push origin main
# Render auto-deploys
```

### View Logs
```bash
# In Render Shell
tail -f /var/log/app.log
```

### Run Management Commands
```bash
# In Render Shell
python manage.py command_name
```

### Create Backup
```bash
# In Render Shell
python manage.py dumpdata > backup.json
```

---

## Support & Resources

- **Render Docs**: https://render.com/docs
- **Django Docs**: https://docs.djangoproject.com
- **PostgreSQL Docs**: https://www.postgresql.org/docs
- **GitHub**: https://github.com/charidedecha7-ops/Ethiopia-Hospital

---

## Summary

Your Ethiopian Hospital Management System is now deployed on Render! 🎉

- **URL**: `https://hospital-system.onrender.com`
- **Admin**: `https://hospital-system.onrender.com/admin`
- **API**: `https://hospital-system.onrender.com/api`

**Next Steps:**
1. Test all features
2. Configure custom domain
3. Set up monitoring
4. Configure backups
5. Monitor performance

---

**Deployment Complete!** ✅
