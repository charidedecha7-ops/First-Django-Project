#!/usr/bin/env python
"""
Setup script for Ethiopian Hospital Management System
Run this after installing requirements to set up the system
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   Ethiopian Hospital Management System - Setup Script     ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("Error: manage.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Step 1: Generate datasets
    print("\n[1/5] Generating synthetic datasets...")
    os.chdir('datasets')
    if run_command('python generate_datasets.py', 'Generating datasets'):
        print("✓ Datasets generated successfully!")
    else:
        print("✗ Failed to generate datasets")
        sys.exit(1)
    os.chdir('..')
    
    # Step 2: Train ML models
    print("\n[2/5] Training machine learning models...")
    os.chdir('ml_models')
    if run_command('python train_models.py', 'Training ML models'):
        print("✓ ML models trained successfully!")
    else:
        print("✗ Failed to train ML models")
        sys.exit(1)
    os.chdir('..')
    
    # Step 3: Run migrations
    print("\n[3/5] Running database migrations...")
    if run_command('python manage.py migrate', 'Creating database tables'):
        print("✓ Database migrations completed!")
    else:
        print("✗ Failed to run migrations")
        sys.exit(1)
    
    # Step 4: Create directories
    print("\n[4/5] Creating required directories...")
    directories = ['media', 'media/patients', 'media/profiles', 'static', 'staticfiles']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("✓ Directories created!")
    
    # Step 5: Collect static files
    print("\n[5/5] Collecting static files...")
    if run_command('python manage.py collectstatic --noinput', 'Collecting static files'):
        print("✓ Static files collected!")
    else:
        print("⚠ Warning: Failed to collect static files (this is okay for development)")
    
    # Final instructions
    print(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║                    Setup Complete! 🎉                     ║
    ╚═══════════════════════════════════════════════════════════╝
    
    Next steps:
    
    1. Create a superuser account:
       python manage.py createsuperuser
    
    2. Start the development server:
       python manage.py runserver
    
    3. Visit http://127.0.0.1:8000 in your browser
    
    4. Login with your superuser credentials
    
    Default demo credentials (if you load sample data):
    - Admin: admin / admin123
    - Doctor: doctor / doctor123
    - Nurse: nurse / nurse123
    
    For production deployment, see DEPLOYMENT.md
    
    Happy coding! 🏥
    """)

if __name__ == '__main__':
    main()
