# 🌟 Sheba Backend API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![DRF](https://img.shields.io/badge/DRF-3.15-orange)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

**Enterprise-grade REST API backend for Sheba community platform**

*Connecting Bangladeshi expatriates in Oman with essential services*

</div>

---

## 📖 Overview

Sheba Backend is a comprehensive Django REST Framework API that powers the Sheba community platform. Built with scalability, security, and performance in mind, it provides a complete suite of services for job hunting, property search, service providers, community engagement, and emergency assistance.

### 🎯 Key Features

- ✅ **Multi-role Authentication** - User, Service Provider, Recruiter, Admin
- ✅ **Complete Job Portal** - Jobs, Companies, Applications, Categories
- ✅ **Property Marketplace** - Residential, Commercial, Land listings
- ✅ **Vehicle Marketplace** - Buy, Sell, Rent vehicles
- ✅ **Service Provider Directory** - Verified service providers with booking
- ✅ **Community Platform** - Forum, Posts, Comments, Classifieds
- ✅ **Content Management** - News, Articles, Blogs, Announcements
- ✅ **Emergency Services** - Quick access emergency contacts
- ✅ **Notification System** - Real-time user notifications
- ✅ **Messaging System** - User-to-user messaging
- ✅ **Review & Rating** - Universal review system
- ✅ **Advertisement Management** - Ad placement with analytics
- ✅ **Bilingual Support** - English and Bengali (বাংলা)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip & virtualenv
- PostgreSQL (production) / SQLite (development)

### Automated Setup (Recommended)

```bash
# Clone repository
git clone <repository-url>
cd ShebaWebsiteBackend

# Run setup script
chmod +x migrate_and_setup.sh
./migrate_and_setup.sh

# Start server
python manage.py runserver
```

### Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your settings

# 4. Run migrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Start server
python manage.py runserver
```

### Access Points

- **API Base**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Docs**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

---

## 🏗️ Architecture

### Project Structure

```
ShebaWebsiteBackend/
├── sheba_backend/          # Project configuration
├── users/                  # User management & authentication
├── classifieds/            # Jobs, Properties, Vehicles, Services
├── community/              # Forum, Posts, Classifieds
├── news/                   # News & Articles
├── emergency/              # Emergency services
├── system/                 # Advertisements, Analytics, Settings
├── static/                 # Static files
├── media/                  # User uploads
└── templates/              # Templates
```

### Technology Stack

- **Framework**: Django 4.2.16
- **API**: Django REST Framework 3.15.1
- **Database**: PostgreSQL / SQLite
- **Admin UI**: Django Grappelli 3.0.9
- **Image Processing**: Pillow 10.3.0
- **API Docs**: drf-yasg 1.21.7

---

## 🔌 API Reference

### Core Endpoints

#### Authentication
```http
POST /api/users/register/      # Register new user
POST /api/users/login/          # User login
POST /api/users/logout/         # User logout
GET  /api/users/profile/        # Get/Update profile
```

#### Jobs
```http
GET    /api/classifieds/jobs/               # List jobs
POST   /api/classifieds/jobs/               # Create job
GET    /api/classifieds/jobs/{id}/          # Job details
POST   /api/classifieds/jobs/{id}/apply/    # Apply to job
GET    /api/classifieds/companies/          # List companies
```

#### Properties
```http
GET    /api/classifieds/properties/         # List properties
POST   /api/classifieds/properties/         # Create property
GET    /api/classifieds/properties/{id}/    # Property details
```

#### Vehicles
```http
GET    /api/classifieds/vehicles/           # List vehicles
POST   /api/classifieds/vehicles/           # Create vehicle
GET    /api/classifieds/vehicles/{id}/      # Vehicle details
```

#### Service Providers
```http
GET    /api/classifieds/service-providers/           # List providers
POST   /api/classifieds/service-providers/           # Create provider
POST   /api/classifieds/service-providers/{id}/book/ # Book service
```

#### Community
```http
GET    /api/community/posts/               # List posts
GET    /api/community/forum/               # Forum posts
GET    /api/community/classifieds/         # Classified ads
```

#### News & Emergency
```http
GET    /api/news/                          # List news/articles
GET    /api/emergency/services/            # Emergency services
```

### Query Parameters

All list endpoints support:
- `page` - Page number
- `page_size` - Items per page (default: 20)
- `search` - Search query
- `ordering` - Sort field (e.g., `-created_at`)
- Field filters (e.g., `?city=Muscat`)

**Complete API Documentation**: http://localhost:8000/swagger/

---

## 🗄️ Database Models

### Models Overview (34 total)

- **Users** (4): User, Notification, Message, Favorite
- **Classifieds** (13): Job, Company, Property, Vehicle, ServiceProvider, Review, Booking, etc.
- **Community** (8): ForumPost, ForumComment, Classified, Post, Comment, Like
- **News** (3): Article, News, NewsComment
- **Emergency** (2): EmergencyService, EmergencyContact
- **System** (4): Advertisement, PageView, Setting, AuditLog

All models include:
- ✅ Bengali language support (`_bn` fields)
- ✅ Auto-generated unique slugs
- ✅ Proper indexing for performance
- ✅ Timestamp tracking
- ✅ Status management

---

## 🔒 Security

- ✅ Session-based authentication
- ✅ Role-based access control (RBAC)
- ✅ CSRF protection
- ✅ SQL injection prevention (Django ORM)
- ✅ XSS protection
- ✅ Password hashing (PBKDF2)
- ✅ CORS configuration
- ✅ Secure cookie settings

---

## 🚀 Deployment

### Development

```bash
python manage.py runserver
```

### Production Quick Steps

```bash
# 1. Configure environment
export DEBUG=False
export ALLOWED_HOSTS=yourdomain.com

# 2. Use PostgreSQL
# Configure DATABASE_URL in .env

# 3. Collect static files
python manage.py collectstatic --noinput

# 4. Run with Gunicorn
gunicorn sheba_backend.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Deployment Platforms

- **VPS/Cloud**: Ubuntu, Debian, CentOS with Nginx/Apache
- **Railway**: `railway up`
- **Heroku**: `git push heroku main`
- **DigitalOcean**: App Platform or Droplet
- **AWS**: EC2, Elastic Beanstalk

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL
- [ ] Set strong `SECRET_KEY`
- [ ] Configure HTTPS/SSL
- [ ] Set up reverse proxy
- [ ] Configure CORS for production
- [ ] Set up backups
- [ ] Configure logging
- [ ] Set up monitoring

---

## ⚙️ Configuration

### Environment Variables (.env)

```env
# Django Core
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL)
DB_NAME=sheba_db
DB_USER=sheba_user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com

# Email (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

See `.env.example` for complete configuration options.

---

## 🛠️ Common Commands

```bash
# Database
python manage.py makemigrations    # Create migrations
python manage.py migrate           # Apply migrations

# Users
python manage.py createsuperuser   # Create admin user

# Development
python manage.py runserver         # Start dev server
python manage.py shell             # Django shell

# Static Files
python manage.py collectstatic     # Collect static files

# Testing
python manage.py test              # Run tests
python manage.py check             # Check for issues
python manage.py check --deploy    # Check deployment readiness
```

---

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users
python manage.py test classifieds

# With coverage
coverage run --source='.' manage.py test
coverage report
```

---

## � Performance Features

- ✅ Optimized database queries with proper indexing
- ✅ Pagination for all list endpoints
- ✅ Static file compression
- ✅ Connection pooling ready
- ✅ Caching configuration ready (Redis)
- ✅ Query optimization with select_related/prefetch_related

---

## 📝 License

**Proprietary License** - All Rights Reserved

This software is proprietary and confidential. Unauthorized copying, distribution, modification, or use is strictly prohibited.

Copyright © 2024 Sheba Platform. All rights reserved.

---

## 👥 Team

**Sheba Development Team**
- Target: Bangladeshi Expatriates in Oman
- Platform: Community Services & Marketplace

---

## 🎯 API Status

| Module | Status | Endpoints |
|--------|--------|-----------|
| Authentication | ✅ Ready | 4 |
| Jobs | ✅ Ready | 8+ |
| Properties | ✅ Ready | 5+ |
| Vehicles | ✅ Ready | 5+ |
| Service Providers | ✅ Ready | 6+ |
| Community | ✅ Ready | 10+ |
| News | ✅ Ready | 5+ |
| Emergency | ✅ Ready | 3+ |

**Total**: 40+ API endpoints

---

## 📞 Support

For issues or questions:
- Check API documentation at `/swagger/`
- Review error logs in console
- Verify environment configuration
- Test with Postman/Thunder Client

---

<div align="center">

**Made with ❤️ for Bangladeshi Expatriates in Oman**

**🌟 স্বপ্ন দেখুন, এগিয়ে যান, সফল হন 🌟**

---

**Version 2.0** | **Production Ready** | **Deployment Ready**

</div>
