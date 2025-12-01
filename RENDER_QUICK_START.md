# Render Deployment - Quick Start (5 Minutes)

## Quick Steps

### 1. GitHub Setup
```bash
git push origin main
```

### 2. Render Dashboard
1. Go to https://render.com
2. Sign in with GitHub
3. Click "New +" → "PostgreSQL"
4. Create database (save credentials)

### 3. Create Web Service
1. Click "New +" → "Web Service"
2. Connect GitHub repository
3. Fill in:
   - **Name**: `hospital-system`
   - **Build Command**: 
     ```
     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
     ```
   - **Start Command**: 
     ```
     gunicorn hospital_system.wsgi:application
     ```

### 4. Environment Variables
Add these in Web Service settings:
```
DEBUG=False
SECRET_KEY=<generate-random-key>
ALLOWED_HOSTS=hospital-system.onrender.com
DATABASE_URL=<from-postgres-database>
```

### 5. Deploy
Click "Create Web Service" and wait for deployment

### 6. Initialize Data
In Render Shell:
```bash
python manage.py createsuperuser
python manage.py load_sample_data
python manage.py add_doctors
python manage.py add_patients
python manage.py add_appointments
python manage.py add_lab_tests
python manage.py add_medicines
python manage.py add_bills
```

### 7. Access
- **Site**: https://hospital-system.onrender.com
- **Admin**: https://hospital-system.onrender.com/admin
- **API**: https://hospital-system.onrender.com/api

---

## Generate SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails | Check logs, verify requirements.txt |
| Database error | Verify DATABASE_URL environment variable |
| Static files missing | Run collectstatic in shell |
| 500 error | Check DEBUG setting, verify ALLOWED_HOSTS |

---

## Files Needed

- ✅ `Procfile` - Already included
- ✅ `requirements.txt` - Already included
- ✅ `runtime.txt` - Already included
- ✅ `render.yaml` - Already included

---

**Done!** Your app is live on Render 🚀
