# Sheba API Endpoints

Base URL: `http://localhost:8000/api/`

## 📚 API Documentation
- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **Admin Panel**: http://localhost:8000/admin/

## 🔐 Authentication

### User Registration
```
POST /api/users/register/
Body: {
  "username": "string",
  "email": "email",
  "password": "string",
  "password_confirm": "string",
  "first_name": "string" (optional),
  "last_name": "string" (optional),
  "phone_number": "string" (optional)
}
```

### Login
```
POST /api/users/login/
Body: {
  "username": "string",
  "password": "string"
}
```

### Logout
```
POST /api/users/logout/
Headers: Authentication required
```

### User Profile
```
GET /api/users/profile/
PUT /api/users/profile/
PATCH /api/users/profile/
Headers: Authentication required
```

## 💼 Classifieds

### Jobs
```
GET    /api/classifieds/jobs/              # List all jobs
POST   /api/classifieds/jobs/              # Create job (auth required)
GET    /api/classifieds/jobs/{id}/         # Get job details
PUT    /api/classifieds/jobs/{id}/         # Update job (auth required)
DELETE /api/classifieds/jobs/{id}/         # Delete job (auth required)

Query params:
  ?job_type=full_time|part_time|contract|freelance
  ?category=string
  ?location=string
  ?search=keyword
  ?ordering=created_at|-created_at|price|-price
```

### Properties
```
GET    /api/classifieds/properties/        # List all properties
POST   /api/classifieds/properties/        # Create property (auth required)
GET    /api/classifieds/properties/{id}/   # Get property details
PUT    /api/classifieds/properties/{id}/   # Update property (auth required)
DELETE /api/classifieds/properties/{id}/   # Delete property (auth required)

Query params:
  ?property_type=apartment|house|commercial|land
  ?listing_type=sale|rent
  ?location=string
  ?bedrooms=number
  ?search=keyword
  ?ordering=created_at|-created_at|price|-price
```

### Vehicles
```
GET    /api/classifieds/vehicles/          # List all vehicles
POST   /api/classifieds/vehicles/          # Create vehicle (auth required)
GET    /api/classifieds/vehicles/{id}/     # Get vehicle details
PUT    /api/classifieds/vehicles/{id}/     # Update vehicle (auth required)
DELETE /api/classifieds/vehicles/{id}/     # Delete vehicle (auth required)

Query params:
  ?brand=string
  ?condition=new|used|reconditioned
  ?location=string
  ?year=number
  ?search=keyword
  ?ordering=created_at|-created_at|price|-price|year|-year
```

### Services
```
GET    /api/classifieds/services/          # List all services
POST   /api/classifieds/services/          # Create service (auth required)
GET    /api/classifieds/services/{id}/     # Get service details
PUT    /api/classifieds/services/{id}/     # Update service (auth required)
DELETE /api/classifieds/services/{id}/     # Delete service (auth required)

Query params:
  ?category=string
  ?location=string
  ?search=keyword
  ?ordering=created_at|-created_at|price|-price
```

## 🚨 Emergency

### Emergency Services
```
GET /api/emergency/services/              # List emergency services
GET /api/emergency/services/{id}/         # Get service details

Query params:
  ?service_type=ambulance|fire|police|hospital|pharmacy|blood_bank
  ?location=string
  ?is_24_7=true|false
  ?search=keyword
```

### Personal Emergency Contacts
```
GET    /api/emergency/contacts/           # List user's contacts (auth required)
POST   /api/emergency/contacts/           # Add contact (auth required)
GET    /api/emergency/contacts/{id}/      # Get contact details (auth required)
PUT    /api/emergency/contacts/{id}/      # Update contact (auth required)
DELETE /api/emergency/contacts/{id}/      # Delete contact (auth required)
```

## 📰 News

### News Articles
```
GET /api/news/                            # List all published news
GET /api/news/{slug}/                     # Get news by slug

Query params:
  ?category=local|national|community|event|announcement
  ?is_featured=true|false
  ?search=keyword
  ?ordering=published_at|-published_at|views|-views
```

### News Comments
```
GET  /api/news/{slug}/comments/          # List comments for news article
POST /api/news/{slug}/comments/          # Add comment (auth required)
```

## 👥 Community

### Posts
```
GET    /api/community/posts/              # List all posts
POST   /api/community/posts/              # Create post (auth required)
GET    /api/community/posts/{id}/         # Get post details
PUT    /api/community/posts/{id}/         # Update post (auth required)
DELETE /api/community/posts/{id}/         # Delete post (auth required)
```

### Comments
```
GET  /api/community/posts/{post_id}/comments/  # List comments
POST /api/community/posts/{post_id}/comments/  # Add comment (auth required)
```

### Like/Unlike
```
POST /api/community/posts/{post_id}/like/      # Toggle like (auth required)
```

## ⭐ Favorites

```
GET    /api/users/favorites/              # List user's favorites (auth required)
POST   /api/users/favorites/              # Add to favorites (auth required)
DELETE /api/users/favorites/{id}/         # Remove from favorites (auth required)

Body for POST:
{
  "content_type": "job|property|vehicle|service|news",
  "content_id": number
}
```

## 📊 Response Format

### Success Response
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/endpoint/?page=2",
  "previous": null,
  "results": [...]
}
```

### Error Response
```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```

## 🔑 Admin Credentials (for testing)
- Username: `admin`
- Email: `admin@sheba.com`
- Password: `admin123`

## 📝 Notes
- All endpoints support pagination (default: 20 items per page)
- Use `?page=2` for pagination
- Authentication uses Django sessions (cookies)
- CORS is enabled for `http://localhost:3000`
