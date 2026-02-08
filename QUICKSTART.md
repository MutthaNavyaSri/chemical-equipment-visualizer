# Quick Start Guide

## For Backend (Django)

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Backend runs at: http://localhost:8000

## For Web Frontend (React)

```bash
cd frontend-web
npm install
npm start
```

Web app opens at: http://localhost:3000

## For Desktop App (PyQt5)

```bash
cd frontend-desktop
pip install -r requirements.txt
python main.py
```

## First Time Setup

1. Start backend server first
2. Open web app and create an account
3. Upload sample_equipment_data.csv
4. View visualizations and download reports
5. Try the desktop app with the same credentials

## Default Test Credentials

After running the app, create your own credentials through the registration page.

## Need Help?

Check README.md for detailed instructions and troubleshooting.
