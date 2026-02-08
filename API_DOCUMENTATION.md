# API Documentation

Base URL: `http://localhost:8000/api`

## Authentication

### Register User
**POST** `/auth/register/`

Request:
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe"
}
```

Response:
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbG...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbG..."
}
```

### Login
**POST** `/auth/login/`

Request:
```json
{
  "username": "johndoe",
  "password": "password123"
}
```

Response: Same as register

### Get Profile
**GET** `/auth/profile/`

Headers:
```
Authorization: Bearer <access_token>
```

Response:
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

## Datasets

### List Datasets
**GET** `/datasets/`

Headers:
```
Authorization: Bearer <access_token>
```

Response:
```json
[
  {
    "id": 1,
    "filename": "equipment_data.csv",
    "uploaded_at": "2024-02-08T10:30:00Z",
    "username": "johndoe",
    "total_count": 20,
    "avg_flowrate": 185.5,
    "avg_pressure": 6.2,
    "avg_temperature": 85.3,
    "equipment_types": {
      "Reactor": 4,
      "Heat Exchanger": 4,
      "Pump": 4,
      "Compressor": 4,
      "Distillation Column": 4
    }
  }
]
```

### Upload CSV
**POST** `/datasets/upload/`

Headers:
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

Form Data:
- `file`: CSV file

Response:
```json
{
  "id": 1,
  "filename": "equipment_data.csv",
  "uploaded_at": "2024-02-08T10:30:00Z",
  "username": "johndoe",
  "total_count": 20,
  "avg_flowrate": 185.5,
  "avg_pressure": 6.2,
  "avg_temperature": 85.3,
  "equipment_types": {...},
  "records": [
    {
      "id": 1,
      "equipment_name": "Reactor A1",
      "equipment_type": "Reactor",
      "flowrate": 150.5,
      "pressure": 5.2,
      "temperature": 85.3
    }
  ]
}
```

### Get Dataset Detail
**GET** `/datasets/{id}/`

Headers:
```
Authorization: Bearer <access_token>
```

Response: Same as upload response

### Delete Dataset
**DELETE** `/datasets/{id}/delete/`

Headers:
```
Authorization: Bearer <access_token>
```

Response:
```json
{
  "message": "Dataset deleted successfully"
}
```

### Download PDF Report
**GET** `/datasets/{id}/report/`

Headers:
```
Authorization: Bearer <access_token>
```

Response: PDF file (application/pdf)

## Error Responses

### 400 Bad Request
```json
{
  "error": "CSV must contain columns: Equipment Name, Type, Flowrate, Pressure, Temperature"
}
```

### 401 Unauthorized
```json
{
  "error": "Invalid credentials"
}
```

### 404 Not Found
```json
{
  "error": "Dataset not found"
}
```

## CSV Format

Required columns:
- Equipment Name
- Type
- Flowrate
- Pressure
- Temperature

Example:
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor A1,Reactor,150.5,5.2,85.3
Heat Exchanger B2,Heat Exchanger,200.3,3.8,120.5
```

## Rate Limiting

No rate limiting is currently implemented. For production, consider adding rate limiting using Django REST Framework throttling.

## CORS

CORS is enabled for all origins in development. For production, configure `CORS_ALLOWED_ORIGINS` in settings.py.
