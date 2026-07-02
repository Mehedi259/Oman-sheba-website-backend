"""
URL configuration for sheba_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


def api_root(request):
    """API root endpoint with links to all available endpoints"""
    return JsonResponse({
        'message': 'Welcome to Sheba API',
        'version': '1.0',
        'documentation': {
            'swagger': request.build_absolute_uri('/swagger/'),
            'redoc': request.build_absolute_uri('/redoc/'),
        },
        'endpoints': {
            'users': {
                'register': request.build_absolute_uri('/api/users/register/'),
                'login': request.build_absolute_uri('/api/users/login/'),
                'logout': request.build_absolute_uri('/api/users/logout/'),
                'profile': request.build_absolute_uri('/api/users/profile/'),
                'favorites': request.build_absolute_uri('/api/users/favorites/'),
            },
            'classifieds': {
                'jobs': request.build_absolute_uri('/api/classifieds/jobs/'),
                'properties': request.build_absolute_uri('/api/classifieds/properties/'),
                'vehicles': request.build_absolute_uri('/api/classifieds/vehicles/'),
                'services': request.build_absolute_uri('/api/classifieds/services/'),
            },
            'emergency': {
                'services': request.build_absolute_uri('/api/emergency/services/'),
                'contacts': request.build_absolute_uri('/api/emergency/contacts/'),
            },
            'news': request.build_absolute_uri('/api/news/'),
            'community': {
                'posts': request.build_absolute_uri('/api/community/posts/'),
            },
        },
        'admin': request.build_absolute_uri('/admin/'),
    })


schema_view = get_schema_view(
    openapi.Info(
        title="Sheba API",
        default_version='v1',
        description="REST API for Sheba Community Platform",
        contact=openapi.Contact(email="contact@sheba.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API endpoints
    path('api/users/', include('users.urls')),
    path('api/classifieds/', include('classifieds.urls')),
    path('api/emergency/', include('emergency.urls')),
    path('api/news/', include('news.urls')),
    path('api/community/', include('community.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
