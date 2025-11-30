web: gunicorn hospital_system.wsgi:application
release: python manage.py migrate && python manage.py collectstatic --noinput
