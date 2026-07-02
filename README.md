# Sheba Website Backend

Django REST API backend for Sheba community platform.

## Features

- **Classifieds API**: Jobs, Properties, Vehicles, Services
- **Emergency Services API**
- **News API**
- **Community API**
- **User Management & Authentication**
- **Favorites System**

## Tech Stack

- Django 4.2
- Django REST Framework
- SQLite (development) / PostgreSQL (production)
- Session Authentication

## Quick Setup

### Option 1: Automatic Setup (Recommended)
```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

1. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create admin user (optional):
```bash
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

API will be available at `http://localhost:8000/api/`

### Default Admin Account (for testing)
- Username: `admin`
- Email: `admin@sheba.com`
- Password: `admin123`

## Current Status

✅ Backend server is running at http://localhost:8000/
✅ All database migrations completed
✅ Admin user created
✅ API endpoints ready for frontend integration

## API Documentation

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`
- Admin Panel: `http://localhost:8000/admin/`

**📋 Complete API Endpoints:** See [API_ENDPOINTS.md](./API_ENDPOINTS.md) for detailed endpoint documentation.

## Project Structure

```
sheba_backend/
├── classifieds/      # Jobs, Properties, Vehicles, Services
├── emergency/        # Emergency services
├── news/            # News management
├── community/       # Community features
├── users/           # User management
└── core/            # Core settings and utilities
```
