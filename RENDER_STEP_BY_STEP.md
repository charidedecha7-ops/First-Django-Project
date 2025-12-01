# Deploy on Render - Complete Step-by-Step Guide with Screenshots

## Step 1: Create Render Account

### 1.1 Go to Render Website
- Open: https://render.com
- Click "Sign Up" button (top right)

### 1.2 Sign Up with GitHub
```
Option 1: GitHub (Recommended)
- Click "Continue with GitHub"
- Authorize Render to access your GitHub account
- Click "Authorize render-oss"

Option 2: Email
- Enter email
- Create password
- Verify email
```

### 1.3 Complete Setup
- Verify your email
- You're now logged in to Render dashboard

---

## Step 2: Create PostgreSQL Database

### 2.1 Navigate to Database Creation
```
Dashboard → New + (top right) → PostgreSQL
```

### 2.2 Fill Database Details
```
Name:              hospital-db
Database:          hospital_db
User:              hospital_user
Password:          (auto-generated, save it!)
Region:            Choose closest to you
Plan:              Free (for testing)
```

### 2.3 Create Database
- Click "Create Database"
- Wait for database to be created (2-3 minutes)

### 2.4 Save Database Credentials
Once created, you'll see:
```
Internal Database URL:
postgresql://hospital_user:PASSWORD@dpg-xxxxx.internal/hospital_db

External Database URL:
postgresql://hospital_user:PASSWORD@dpg-xxxxx.render.com:5432/hospital_db
```

**IMPORTANT**: Copy and save the **External Database URL** (you'll need it later)

---

## Step 3: Create Web Service

### 3.1 Navigate to Web Service Creation
```
Dashboard → New + (top right) → Web Service
```

### 3.2 Connect GitHub Repository
```
Step 1: Click "Connect account" (if needed)
Step 2: Authorize Render to access GitHub
Step 3: Select repository: "Ethiopia-Hospital"
Step 4: Click "Connect"
```

### 3.3 Configure Web Service

Fill in the following fields:

```
Name:              hospital-system
Environment:       Python 3
Region:            Same as database (important!)
Branch:            main
Root Directory:    (leave empty)
Build Command:     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
Start Command:     gunicorn hospital_system.wsgi:application
Plan:              Free
```

### 3.4 Add Environment Variables

Click "Advanced" and add these variables:

```
DEBUG                  False
SECRET_KEY             (generate below)
ALLOWED_HOSTS          hospital-system.onrender.com
DATABASE_URL           (paste from Step 2.4)
RENDER_EXTERNAL_HOSTNAME  (auto-filled by Render)
```

### 3.5 Generate SECRET_KEY

Run this command locally:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it as SECRET_KEY value.

### 3.6 Create Web Service
- Click "Create Web Service"
- Render will start building your application

---

## Step 4: Monitor Deployment

### 4.1 Watch Build Progress
```
Dashboard → Your Web Service → Logs
```

You should see:
```
Building...
Installing dependencies...
Running migrations...
Collecting static files...
Build successful!
Starting server...
```

### 4.2 Wait for Deployment
- Build takes 3-5 minutes
- Look for: "Build successful" message
- Server will start automatically

### 4.3 Check Status
```
Dashboard → Your Web Service
Status should show: "Live"
```

---

## Step 5: Access Your Application

### 5.1 Get Your URL
```
Dashboard → Your Web Service
Copy the URL (e.g., https://hospital-system.onrender.com)
```

### 5.2 Test Application
```
Main Site:    https://hospital-system.onrender.com
Admin Panel:  https://hospital-system.onrender.com/admin
API:          https://hospital-system.onrender.com/api
```

### 5.3 First Access
- You'll see the Django application
- Admin panel will be empty (no users yet)

---

## Step 6: Initialize Data via Shell

### 6.1 Open Render Shell
```
Dashboard → Your Web Service → Shell
```

### 6.2 Create Superuser
```bash
python manage.py createsuperuser
```

Follow prompts:
```
Username: admin
Email: admin@hospital.et
Password: (enter password)
Password (again): (confirm)
```

### 6.3 Load Sample Data
Run these commands one by one:

```bash
# Load core sample data
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

Each command will show:
```
✓ Data loaded successfully!
```

---

## Step 7: Login and Test

### 7.1 Go to Admin Panel
```
https://hospital-system.onrender.com/admin
```

### 7.2 Login
```
Username: admin
Password: (your password from Step 6.2)
```

### 7.3 Verify Data
You should see:
- ✅ 5 Doctors
- ✅ 13 Patients
- ✅ 8 Appointments
- ✅ 6 Lab Tests
- ✅ 8 Medicines
- ✅ 5 Prescriptions
- ✅ 5 Bills

### 7.4 Test Features
- Go to: https://hospital-system.onrender.com/doctors/
- See all doctors with image upload capability
- Click "View Profile" to see doctor details
- Try uploading an image

---

## Step 8: Configure Custom Domain (Optional)

### 8.1 Add Custom Domain
```
Dashboard → Your Web Service → Settings → Custom Domains
```

### 8.2 Enter Your Domain
```
Domain: hospital.example.com
```

### 8.3 Configure DNS
Render will show DNS records to add to your domain provider:
```
Type: CNAME
Name: hospital
Value: hospital-system.onrender.com
```

### 8.4 Wait for SSL
- Render automatically generates SSL certificate
- Takes 5-10 minutes
- Your domain will be live with HTTPS

---

## Step 9: Monitor Application

### 9.1 View Logs
```
Dashboard → Your Web Service → Logs
```

Monitor for:
- Errors
- Warnings
- Performance issues

### 9.2 Check Metrics
```
Dashboard → Your Web Service → Metrics
```

Monitor:
- CPU usage
- Memory usage
- Response times

### 9.3 Set Up Alerts (Optional)
```
Dashboard → Your Web Service → Settings → Notifications
```

---

## Step 10: Troubleshooting

### Issue: Build Failed

**Check logs:**
```
Dashboard → Your Web Service → Logs
Look for error messages
```

**Common causes:**
- Missing dependencies in requirements.txt
- Python version mismatch
- Syntax errors in code

**Solution:**
```
1. Fix the error locally
2. Commit to GitHub
3. Render auto-redeploys
```

### Issue: Database Connection Error

**Check DATABASE_URL:**
```
Dashboard → Your Web Service → Environment
Verify DATABASE_URL is correct
```

**Solution:**
```
1. Copy correct URL from PostgreSQL database
2. Update environment variable
3. Redeploy
```

### Issue: Static Files Not Loading

**Run in Shell:**
```bash
python manage.py collectstatic --noinput
```

**Check settings:**
```
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Issue: 500 Error

**Check logs:**
```
Dashboard → Your Web Service → Logs
Look for error details
```

**Common causes:**
- DEBUG = True (should be False)
- ALLOWED_HOSTS not configured
- Database not connected

---

## Step 11: Backup & Maintenance

### 11.1 Database Backups
```
Dashboard → PostgreSQL Database → Backups
Configure automatic backups
```

### 11.2 Update Application
```
1. Make changes locally
2. Commit to GitHub
3. Render auto-deploys
```

### 11.3 Monitor Performance
```
Dashboard → Your Web Service → Metrics
Check CPU, memory, response times
```

---

## Quick Reference

### Important URLs
```
Render Dashboard:     https://render.com/dashboard
Your Web Service:     https://hospital-system.onrender.com
Admin Panel:          https://hospital-system.onrender.com/admin
API:                  https://hospital-system.onrender.com/api
```

### Important Commands
```
Create superuser:     python manage.py createsuperuser
Load sample data:     python manage.py load_sample_data
Add doctors:          python manage.py add_doctors
Add patients:         python manage.py add_patients
Add appointments:     python manage.py add_appointments
Add lab tests:        python manage.py add_lab_tests
Add medicines:        python manage.py add_medicines
Add bills:            python manage.py add_bills
```

### Environment Variables
```
DEBUG=False
SECRET_KEY=<generated-key>
ALLOWED_HOSTS=hospital-system.onrender.com
DATABASE_URL=<postgres-url>
RENDER_EXTERNAL_HOSTNAME=<auto-filled>
```

---

## Deployment Checklist

- [ ] Render account created
- [ ] PostgreSQL database created
- [ ] Database URL saved
- [ ] Web Service created
- [ ] Environment variables added
- [ ] Build successful
- [ ] Application live
- [ ] Superuser created
- [ ] Sample data loaded
- [ ] Admin panel accessible
- [ ] Features tested
- [ ] Custom domain configured (optional)
- [ ] Monitoring set up

---

## Success Indicators

✅ Application is live at https://hospital-system.onrender.com
✅ Admin panel accessible at /admin
✅ All sample data loaded
✅ Doctors visible with image upload
✅ Patients, appointments, lab tests visible
✅ Pharmacy and billing data loaded
✅ API endpoints working
✅ No errors in logs

---

## Support

If you encounter issues:

1. **Check Render Logs**
   - Dashboard → Your Web Service → Logs

2. **Check Environment Variables**
   - Dashboard → Your Web Service → Environment

3. **Verify Database Connection**
   - Dashboard → PostgreSQL Database → Connection

4. **Review Documentation**
   - RENDER_DEPLOYMENT.md - Full guide
   - RENDER_QUICK_START.md - Quick reference
   - PRE_DEPLOYMENT_CHECKLIST.md - Verification

---

## Summary

Your Ethiopian Hospital Management System is now deployed on Render! 🎉

- **Live URL**: https://hospital-system.onrender.com
- **Admin**: https://hospital-system.onrender.com/admin
- **API**: https://hospital-system.onrender.com/api

**Next Steps:**
1. Share the URL with your team
2. Test all features
3. Configure custom domain
4. Set up monitoring
5. Configure backups

---

**Deployment Complete!** ✅
