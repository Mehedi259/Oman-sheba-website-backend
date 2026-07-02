"""
Django settings for sheba_backend project.
"""

from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'unfold',  # Must be before django.contrib.admin
    'unfold.contrib.filters',  # Optional, for advanced filters
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'django_filters',
    'drf_yasg',
    
    # Local apps
    'users',
    'classifieds',
    'emergency',
    'news',
    'community',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sheba_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sheba_backend.wsgi.application'

# Database
# Using SQLite for development (change to PostgreSQL in production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# For PostgreSQL, uncomment below and comment SQLite above:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME', default='sheba_db'),
#         'USER': config('DB_USER', default='postgres'),
#         'PASSWORD': config('DB_PASSWORD', default='password'),
#         'HOST': config('DB_HOST', default='localhost'),
#         'PORT': config('DB_PORT', default='5432'),
#     }
# }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'users.User'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# CORS settings
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://127.0.0.1:3000'
).split(',')

CORS_ALLOW_CREDENTIALS = True

# Swagger settings
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
    },
    'USE_SESSION_AUTH': True,
}


# Django Unfold Admin Theme Configuration
UNFOLD = {
    "SITE_TITLE": "Sheba Admin",
    "SITE_HEADER": "Sheba Community Platform",
    "SITE_URL": "/",
    "SITE_ICON": None,  # SVG icon or path to image
    
    "SITE_LOGO": {
        "light": None,  # Path to light logo
        "dark": None,   # Path to dark logo
    },
    
    "SITE_SYMBOL": "speed",  # Google Material icon name
    
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    
    "COLORS": {
        "primary": {
            "50": "255 251 235",
            "100": "254 243 199",
            "200": "253 230 138",
            "300": "252 211 77",
            "400": "251 191 36",
            "500": "245 158 11",
            "600": "217 119 6",
            "700": "180 83 9",
            "800": "146 64 14",
            "900": "120 53 15",
            "950": "69 26 3",
        },
    },
    
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "bn": "🇧🇩",
            },
        },
    },
    
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Navigation",
                "separator": True,
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": lambda request: "/admin/",
                    },
                ],
            },
            {
                "title": "User Management",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "person",
                        "link": lambda request: "/admin/users/user/",
                    },
                    {
                        "title": "Favorites",
                        "icon": "favorite",
                        "link": lambda request: "/admin/users/favorite/",
                    },
                ],
            },
            {
                "title": "Classifieds",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Jobs",
                        "icon": "work",
                        "link": lambda request: "/admin/classifieds/job/",
                    },
                    {
                        "title": "Properties",
                        "icon": "home",
                        "link": lambda request: "/admin/classifieds/property/",
                    },
                    {
                        "title": "Vehicles",
                        "icon": "directions_car",
                        "link": lambda request: "/admin/classifieds/vehicle/",
                    },
                    {
                        "title": "Services",
                        "icon": "build",
                        "link": lambda request: "/admin/classifieds/service/",
                    },
                ],
            },
            {
                "title": "Emergency",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Emergency Services",
                        "icon": "local_hospital",
                        "link": lambda request: "/admin/emergency/emergencyservice/",
                    },
                    {
                        "title": "Emergency Contacts",
                        "icon": "contact_phone",
                        "link": lambda request: "/admin/emergency/emergencycontact/",
                    },
                ],
            },
            {
                "title": "Content",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "News",
                        "icon": "article",
                        "link": lambda request: "/admin/news/news/",
                    },
                    {
                        "title": "Community Posts",
                        "icon": "forum",
                        "link": lambda request: "/admin/community/post/",
                    },
                ],
            },
            {
                "title": "Tools",
                "separator": True,
                "items": [
                    {
                        "title": "API Documentation",
                        "icon": "api",
                        "link": lambda request: "/swagger/",
                        "target": "_blank",
                    },
                ],
            },
        ],
    },
    
    "TABS": [],
}
