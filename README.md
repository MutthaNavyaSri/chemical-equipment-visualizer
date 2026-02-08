# Chemical Equipment Parameter Visualizer

A hybrid Web + Desktop application for visualizing and analyzing chemical equipment parameters. The application features a Django REST API backend with React web frontend and PyQt5 desktop frontend, providing comprehensive data visualization, analysis, and PDF report generation.

## 🚀 Features

- **🔐 User Authentication**: Secure login and registration with JWT tokens
- **📤 CSV Upload**: Upload chemical equipment data files
- **📊 Data Visualization**: Interactive charts and graphs using Chart.js (Web) and Matplotlib (Desktop)
- **📈 Statistical Analysis**: Automatic calculation of averages and distributions
- **📄 PDF Reports**: Generate detailed PDF reports with charts and data tables
- **💾 Dataset History**: Store and manage up to 5 datasets per user
- **🎨 Modern UI**: Attractive gradient-based color palette with responsive design
- **🔄 Real-time Sync**: Both Web and Desktop apps use the same backend API

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend (Web)** | React.js + Chart.js | Web-based visualization |
| **Frontend (Desktop)** | PyQt5 + Matplotlib | Desktop application |
| **Backend** | Django + Django REST Framework | RESTful API |
| **Database** | SQLite | Data persistence |
| **Data Processing** | Pandas | CSV analysis |
| **Authentication** | JWT (Simple JWT) | Secure authentication |
| **Reports** | ReportLab | PDF generation |

## 📋 Prerequisites

- **Python 3.8+** (for backend and desktop app)
- **Node.js 16+** and npm (for web frontend)
- **Git** (for version control)

## 📁 Project Structure

```
apping/
├── backend/                    # Django Backend
│   ├── chemical_equipment/     # Django project settings
│   ├── api/                    # REST API app
│   ├── manage.py
│   └── requirements.txt
│
├── frontend-web/              # React Web Frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Auth/         # Login & Register
│   │   │   └── Dashboard/    # Dashboard & Charts
│   │   ├── context/          # Auth Context
│   │   ├── services/         # API Client
│   │   └── App.js
│   └── package.json
│
├── frontend-desktop/          # PyQt5 Desktop App
│   ├── api/                   # API Client
│   ├── ui/                    # UI Components
│   │   ├── main_window.py
│   │   ├── auth_widget.py
│   │   └── dashboard_widget.py
│   ├── main.py
│   └── requirements.txt
│
└── sample_equipment_data.csv  # Sample data file
```

## 🚀 Setup Instructions

### 1. Backend Setup (Django)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional, for admin panel)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### 2. Web Frontend Setup (React)

```bash
# Navigate to web frontend directory
cd frontend-web

# Install dependencies
npm install

# Start development server
npm start
```

The web app will open at `http://localhost:3000`

### 3. Desktop Frontend Setup (PyQt5)

```bash
# Navigate to desktop frontend directory
cd frontend-desktop

# Create virtual environment (if not using backend venv)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 📊 Sample Data

A sample CSV file (`sample_equipment_data.csv`) is provided with 20 equipment records. The CSV must have these columns:

- **Equipment Name**: Name of the equipment
- **Type**: Equipment type (Reactor, Heat Exchanger, Pump, Compressor, Distillation Column)
- **Flowrate**: Flow rate value
- **Pressure**: Pressure value
- **Temperature**: Temperature value

## 🎨 Color Palette

The application uses a modern gradient-based color scheme:

- **Primary**: `#667eea` (Purple-Blue)
- **Secondary**: `#764ba2` (Purple)
- **Success**: `#10b981` (Green)
- **Warning**: `#f59e0b` (Orange)
- **Danger**: `#ef4444` (Red)
- **Info**: `#3b82f6` (Blue)

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `GET /api/auth/profile/` - Get user profile

### Datasets
- `GET /api/datasets/` - List all datasets
- `POST /api/datasets/upload/` - Upload CSV file
- `GET /api/datasets/{id}/` - Get dataset details
- `DELETE /api/datasets/{id}/delete/` - Delete dataset
- `GET /api/datasets/{id}/report/` - Download PDF report

## 🎯 Usage Guide

### Web Application

1. **Register/Login**: Create an account or login with existing credentials
2. **Upload CSV**: Click "Select & Upload CSV File" and choose your data file
3. **View Datasets**: Select a dataset from the list to view details
4. **Visualize Data**: View interactive charts showing equipment distribution and trends
5. **Download Reports**: Click "Download PDF" to generate a detailed report
6. **Delete Datasets**: Remove old datasets using the delete button

### Desktop Application

1. **Launch**: Run `python main.py` from the frontend-desktop directory
2. **Authentication**: Use the Login/Register tabs to access your account
3. **Upload Data**: Click "Select & Upload CSV File" button
4. **Select Dataset**: Choose a dataset from the dropdown menu
5. **View Details**: Click "View Details" to see charts and data table
6. **Download Report**: Use "Download PDF" button to save reports
7. **Manage Data**: Delete unwanted datasets with the "Delete" button

## 📈 Features Details

### Data Visualization

**Web (Chart.js)**:
- Pie chart for equipment type distribution
- Bar chart for parameter comparison
- Line chart for trend analysis
- Responsive and interactive charts

**Desktop (Matplotlib)**:
- Pie chart for type distribution
- Multi-bar chart for parameters
- Line chart with filled area
- Scatter plot for correlation analysis

### PDF Reports

Generated reports include:
- Dataset information and metadata
- Summary statistics table
- Equipment type distribution
- Detailed equipment records table
- Professional styling with colors

### Data Management

- Automatic storage of last 5 datasets per user
- Older datasets automatically deleted
- Full CRUD operations on datasets
- Secure user-specific data isolation

## 🔒 Security Features

- JWT-based authentication
- Password hashing with Django's auth system
- Token refresh mechanism
- CORS enabled for frontend communication
- User-specific data access control

## 🐛 Troubleshooting

### Backend Issues

**Port already in use**:
```bash
python manage.py runserver 8001
```

**Database errors**:
```bash
# Delete db.sqlite3 and re-run migrations
rm db.sqlite3
python manage.py migrate
```

### Frontend Issues

**Web app not connecting to backend**:
- Ensure backend is running on port 8000
- Check `proxy` in package.json

**Desktop app connection error**:
- Verify backend URL in `api/client.py`
- Check firewall settings

### Common Errors

**CSV Upload fails**:
- Verify CSV has correct column names (case-sensitive)
- Check file is valid CSV format
- Ensure file size is reasonable

**Charts not displaying**:
- Web: Check browser console for errors
- Desktop: Ensure matplotlib is installed correctly

## 🚀 Deployment

### Backend Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Set up environment variables for secrets
4. Use PostgreSQL instead of SQLite
5. Serve with Gunicorn + Nginx

### Web Frontend Deployment

```bash
npm run build
# Deploy the build folder to hosting service
```

Recommended platforms:
- Vercel
- Netlify
- GitHub Pages (with router configuration)

### Desktop Application

Package as executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

## 📝 Development Notes

### Adding New Features

1. **Backend**: Add views in `api/views.py` and URLs in `api/urls.py`
2. **Web**: Create components in `src/components/`
3. **Desktop**: Add widgets in `ui/` directory

### Database Schema

**Dataset Model**:
- User (ForeignKey)
- Filename
- Upload timestamp
- Aggregated statistics
- Equipment types (JSON)

**EquipmentRecord Model**:
- Dataset (ForeignKey)
- Equipment details
- Parameters (flowrate, pressure, temperature)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

This project is created for educational purposes as part of an internship screening task.

## 👨‍💻 Author

Created as part of the Chemical Equipment Parameter Visualizer internship task.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API endpoint documentation
3. Examine console/terminal output for errors

## 🎉 Demo Video

Create a 2-3 minute demo video showing:
1. User registration/login
2. CSV file upload
3. Data visualization in both Web and Desktop apps
4. PDF report generation
5. Dataset management features

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://react.dev/)
- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Chart.js Documentation](https://www.chartjs.org/)
- [Matplotlib Documentation](https://matplotlib.org/)

---

**Note**: Make sure to keep the backend server running while using either frontend application!
