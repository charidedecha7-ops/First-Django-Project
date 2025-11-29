from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Region, Woreda
from doctors.models import Doctor, Nurse
from patients.models import Patient
from datetime import date, datetime, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Load sample data for Ethiopian Hospital System'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Loading sample data...'))
        
        # Create regions and woredas
        self.stdout.write('Creating regions and woredas...')
        regions_data = {
            'Oromia': ['Adama', 'Jimma', 'Nekemte', 'Dire Dawa'],
            'Amhara': ['Bahir Dar', 'Gondar', 'Debre Markos'],
            'Tigray': ['Mekelle', 'Axum', 'Shire'],
            'SNNPR': ['Hawassa', 'Arba Minch', 'Wolaita'],
            'Addis Ababa': ['Bole', 'Kirkos', 'Yeka', 'Arada'],
        }
        
        for region_name, woredas in regions_data.items():
            region, _ = Region.objects.get_or_create(
                name=region_name,
                code=region_name[:3].upper()
            )
            for woreda_name in woredas:
                Woreda.objects.get_or_create(
                    region=region,
                    name=woreda_name,
                    code=f"{region.code}-{woreda_name[:3].upper()}"
                )
        
        # Create users
        self.stdout.write('Creating users...')
        
        # Admin
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@hospital.et',
                password='admin123',
                first_name='System',
                last_name='Administrator',
                role='admin',
                phone='+251911000000'
            )
            self.stdout.write(self.style.SUCCESS('✓ Admin user created'))
        
        # Doctors
        doctor_data = [
            ('doctor', 'doctor123', 'Abebe', 'Kebede', 'general', 'MD, MBBS', 10, 500),
            ('doctor2', 'doctor123', 'Tigist', 'Haile', 'pediatrics', 'MD, Pediatrics', 8, 600),
            ('doctor3', 'doctor123', 'Dawit', 'Tesfaye', 'surgery', 'MD, FRCS', 15, 1000),
        ]
        
        for username, password, first_name, last_name, spec, qual, exp, fee in doctor_data:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@hospital.et',
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    role='doctor',
                    phone=f'+25191100{random.randint(1000, 9999)}'
                )
                Doctor.objects.create(
                    user=user,
                    license_number=f'ETH-DOC-{random.randint(10000, 99999)}',
                    specialization=spec,
                    qualification=qual,
                    experience_years=exp,
                    consultation_fee=fee,
                    available_days='Mon,Tue,Wed,Thu,Fri',
                    available_time_start='08:00',
                    available_time_end='17:00'
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Doctor {first_name} {last_name} created'))
        
        # Nurses
        nurse_data = [
            ('nurse', 'nurse123', 'Almaz', 'Girma', 'Emergency', 'morning'),
            ('nurse2', 'nurse123', 'Hanna', 'Bekele', 'Pediatrics', 'afternoon'),
        ]
        
        for username, password, first_name, last_name, dept, shift in nurse_data:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@hospital.et',
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    role='nurse',
                    phone=f'+25191100{random.randint(1000, 9999)}'
                )
                Nurse.objects.create(
                    user=user,
                    license_number=f'ETH-NUR-{random.randint(10000, 99999)}',
                    qualification='BSc Nursing',
                    department=dept,
                    shift=shift
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Nurse {first_name} {last_name} created'))
        
        # Lab Technician
        if not User.objects.filter(username='lab').exists():
            User.objects.create_user(
                username='lab',
                email='lab@hospital.et',
                password='lab123',
                first_name='Yohannes',
                last_name='Tadesse',
                role='lab_technician',
                phone='+251911005000'
            )
            self.stdout.write(self.style.SUCCESS('✓ Lab technician created'))
        
        # Pharmacist
        if not User.objects.filter(username='pharmacy').exists():
            User.objects.create_user(
                username='pharmacy',
                email='pharmacy@hospital.et',
                password='pharmacy123',
                first_name='Marta',
                last_name='Solomon',
                role='pharmacist',
                phone='+251911006000'
            )
            self.stdout.write(self.style.SUCCESS('✓ Pharmacist created'))
        
        # Create sample patients
        self.stdout.write('Creating sample patients...')
        first_names = ['Abebe', 'Tigist', 'Dawit', 'Almaz', 'Kebede', 'Hanna', 'Yohannes', 'Marta']
        last_names = ['Tesfaye', 'Haile', 'Girma', 'Bekele', 'Tadesse', 'Solomon', 'Kebede', 'Abera']
        
        woredas = list(Woreda.objects.all())
        receptionist = User.objects.filter(role='admin').first()
        
        for i in range(20):
            if not Patient.objects.filter(first_name=first_names[i % len(first_names)], 
                                         last_name=last_names[i % len(last_names)]).exists():
                Patient.objects.create(
                    first_name=first_names[i % len(first_names)],
                    last_name=last_names[i % len(last_names)],
                    father_name=random.choice(first_names),
                    date_of_birth=date(random.randint(1950, 2010), random.randint(1, 12), random.randint(1, 28)),
                    gender=random.choice(['M', 'F']),
                    blood_group=random.choice(['A+', 'B+', 'O+', 'AB+']),
                    phone=f'+25191{random.randint(1000000, 9999999)}',
                    woreda=random.choice(woredas),
                    address=f'House {random.randint(100, 999)}, Kebele {random.randint(1, 20)}',
                    kebele_id=f'KB-{random.randint(100000, 999999)}',
                    emergency_contact_name=random.choice(first_names),
                    emergency_contact_phone=f'+25191{random.randint(1000000, 9999999)}',
                    registered_by=receptionist
                )
        
        self.stdout.write(self.style.SUCCESS(f'✓ {Patient.objects.count()} patients created'))
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  Doctor: doctor / doctor123')
        self.stdout.write('  Nurse: nurse / nurse123')
        self.stdout.write('  Lab: lab / lab123')
        self.stdout.write('  Pharmacy: pharmacy / pharmacy123')
