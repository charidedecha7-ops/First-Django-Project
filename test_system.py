import requests

print("=" * 60)
print("TESTING ETHIOPIAN HOSPITAL SYSTEM")
print("=" * 60)

urls = [
    ('Main Page', 'http://127.0.0.1:8000'),
    ('Login Page', 'http://127.0.0.1:8000/login/'),
    ('Dashboard', 'http://127.0.0.1:8000/dashboard/'),
    ('Patients', 'http://127.0.0.1:8000/patients/'),
    ('Doctors', 'http://127.0.0.1:8000/doctors/'),
    ('Appointments', 'http://127.0.0.1:8000/appointments/'),
    ('Laboratory', 'http://127.0.0.1:8000/laboratory/'),
    ('Pharmacy', 'http://127.0.0.1:8000/pharmacy/'),
    ('Billing', 'http://127.0.0.1:8000/billing/'),
    ('Admin', 'http://127.0.0.1:8000/admin/'),
]

print("\nTesting URLs...\n")

all_ok = True
for name, url in urls:
    try:
        response = requests.get(url, allow_redirects=False, timeout=5)
        if response.status_code in [200, 302]:
            print(f"✅ {name:20} - OK (Status: {response.status_code})")
        else:
            print(f"❌ {name:20} - Error (Status: {response.status_code})")
            all_ok = False
    except Exception as e:
        print(f"❌ {name:20} - Error: {str(e)}")
        all_ok = False

print("\n" + "=" * 60)
if all_ok:
    print("✅ ALL TESTS PASSED! System is working perfectly!")
else:
    print("⚠️ Some tests failed. Check the errors above.")
print("=" * 60)

print("\n🌐 Access the system at: http://127.0.0.1:8000")
print("🔐 Login: chari / chari123")
print("\n📄 Or open: OPEN_SYSTEM.html in your browser")
