# Setup Instructions for Windows

## Step 1: Install Python
- Download Python 3.8+ from https://www.python.org/downloads/
- During installation, check "Add Python to PATH"
- Verify: Open Command Prompt and type `python --version`

## Step 2: Install Node.js
- Download Node.js 16+ from https://nodejs.org/
- Install with default options
- Verify: Open Command Prompt and type `node --version` and `npm --version`

## Step 3: Setup Backend

```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Keep this terminal open!

## Step 4: Setup Web Frontend

Open a NEW Command Prompt:

```cmd
cd frontend-web
npm install
npm start
```

Your browser will open automatically at http://localhost:3000

## Step 5: Setup Desktop App

Open a NEW Command Prompt:

```cmd
cd frontend-desktop
pip install -r requirements.txt
python main.py
```

## Troubleshooting

### "python is not recognized"
- Reinstall Python with "Add to PATH" checked
- Or manually add Python to system PATH

### "npm is not recognized"
- Restart Command Prompt after Node.js installation
- Or reinstall Node.js

### Port 8000 already in use
```cmd
# Find process using port
netstat -ano | findstr :8000
# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Cannot connect to backend
- Ensure backend is running (Step 3)
- Check http://localhost:8000/admin to verify server is up
- Disable antivirus/firewall temporarily if blocking connection

## Quick Test

1. Open web app: http://localhost:3000
2. Click "Register" and create an account
3. Upload sample_equipment_data.csv from the root folder
4. View the visualizations
5. Download PDF report
6. Test the desktop app with the same credentials

## Need More Help?

See README.md for detailed documentation.
