@echo off
echo ================================================
echo Ethiopian Hospital Management System
echo ================================================
echo.
echo Starting server...
echo.

start "" "OPEN_SYSTEM.html"

python manage.py runserver

pause
