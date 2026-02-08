# Deployment Guide

## GitHub Repository Setup

1. Create a new GitHub repository at https://github.com/new
2. Name it: `chemical-equipment-visualizer`
3. Keep it public or private based on your preference
4. Don't initialize with README (we already have one)

5. Push to GitHub:
```bash
git remote add origin https://github.com/YOUR_USERNAME/chemical-equipment-visualizer.git
git branch -M main
git push -u origin main
```

## Deployment Options

### Option 1: Deploy Backend on Render.com (Free)

#### Backend Deployment

1. Sign up at https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: chemical-equipment-backend
   - **Root Directory**: backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn chemical_equipment.wsgi:application`
   
5. Add Environment Variables:
   ```
   PYTHON_VERSION=3.11.0
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app.onrender.com
   ```

6. Click "Create Web Service"

#### Frontend Deployment on Netlify/Vercel

**For Netlify:**
1. Sign up at https://netlify.com
2. Click "Add new site" → "Import an existing project"
3. Connect GitHub repository
4. Configure:
   - **Base directory**: frontend-web
   - **Build command**: `npm run build`
   - **Publish directory**: frontend-web/build
   - **Environment variables**: 
     ```
     REACT_APP_API_URL=https://your-backend.onrender.com
     ```

**For Vercel:**
1. Sign up at https://vercel.com
2. Click "New Project"
3. Import your GitHub repository
4. Configure:
   - **Root Directory**: frontend-web
   - **Build Command**: `npm run build`
   - **Output Directory**: build
   - **Environment variables**: 
     ```
     REACT_APP_API_URL=https://your-backend.onrender.com
     ```

### Option 2: Deploy on Railway.app

1. Sign up at https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository

#### Backend Service:
- **Root Directory**: backend
- **Start Command**: `python manage.py migrate && gunicorn chemical_equipment.wsgi:application`
- **Environment Variables**:
  ```
  PORT=8000
  SECRET_KEY=your-secret-key
  DEBUG=False
  ```

#### Frontend Service:
- **Root Directory**: frontend-web
- **Build Command**: `npm install && npm run build`
- **Start Command**: `npm install -g serve && serve -s build`
- **Environment Variables**:
  ```
  REACT_APP_API_URL=https://your-backend.railway.app
  ```

### Option 3: Deploy on Heroku

#### Backend:
```bash
cd backend
heroku create chemical-equipment-backend
heroku addons:create heroku-postgresql:mini
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

#### Frontend:
```bash
cd frontend-web
# Update .env.production with backend URL
npm run build
# Deploy to Netlify or Vercel
```

### Option 4: VPS Deployment (DigitalOcean, Linode, AWS EC2)

#### Prerequisites:
- Ubuntu 22.04 server
- Domain name (optional)

#### Backend Setup:
```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Clone repository
git clone https://github.com/YOUR_USERNAME/chemical-equipment-visualizer.git
cd chemical-equipment-visualizer/backend

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Run migrations
python manage.py migrate
python manage.py collectstatic

# Create systemd service
sudo nano /etc/systemd/system/chemical-equipment.service
```

Service file content:
```ini
[Unit]
Description=Chemical Equipment Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/chemical-equipment-visualizer/backend
Environment="PATH=/path/to/chemical-equipment-visualizer/backend/venv/bin"
ExecStart=/path/to/chemical-equipment-visualizer/backend/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/path/to/chemical-equipment-visualizer/backend/chemical_equipment.sock \
          chemical_equipment.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl start chemical-equipment
sudo systemctl enable chemical-equipment

# Configure Nginx
sudo nano /etc/nginx/sites-available/chemical-equipment
```

Nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api/ {
        include proxy_params;
        proxy_pass http://unix:/path/to/chemical-equipment-visualizer/backend/chemical_equipment.sock;
    }

    location /static/ {
        alias /path/to/chemical-equipment-visualizer/backend/staticfiles/;
    }

    location /media/ {
        alias /path/to/chemical-equipment-visualizer/backend/media/;
    }

    location / {
        root /path/to/chemical-equipment-visualizer/frontend-web/build;
        try_files $uri $uri/ /index.html;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/chemical-equipment /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

#### Frontend Setup:
```bash
cd frontend-web
npm install
npm run build
```

## Post-Deployment

1. **Update CORS settings** in backend/chemical_equipment/settings.py:
```python
CORS_ALLOWED_ORIGINS = [
    'https://your-frontend-domain.com',
]
```

2. **Update API URL** in frontend-web/src/services/api.js:
```javascript
const API_URL = process.env.REACT_APP_API_URL || 'https://your-backend-url.com';
```

3. **Create superuser** on production:
```bash
python manage.py createsuperuser
```

4. **Test endpoints**:
- Backend health: https://your-backend-url.com/api/
- Frontend: https://your-frontend-url.com

## Environment Variables Reference

### Backend (.env):
```
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
CORS_ALLOWED_ORIGINS=https://your-frontend.com
```

### Frontend (.env.production):
```
REACT_APP_API_URL=https://your-backend-url.com
```

## Monitoring and Maintenance

1. **Check logs**:
   - Render: Dashboard → Logs
   - Railway: Dashboard → Deploy logs
   - Heroku: `heroku logs --tail`
   - VPS: `sudo journalctl -u chemical-equipment -f`

2. **Database backups**:
   - Render/Railway: Automatic backups enabled
   - VPS: Setup cron job for regular backups

3. **SSL Certificate**:
   - Most platforms provide automatic SSL
   - For VPS: Use Let's Encrypt with Certbot

## Troubleshooting

### Backend Issues:
- Check environment variables are set correctly
- Verify database migrations are applied
- Check ALLOWED_HOSTS includes your domain
- Review CORS settings

### Frontend Issues:
- Ensure API_URL is correct
- Check browser console for errors
- Verify build process completed successfully

### Database Issues:
- Run migrations: `python manage.py migrate`
- Check database credentials
- Verify database is accessible
