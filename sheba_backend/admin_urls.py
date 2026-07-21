from django.urls import path
from . import admin_views

urlpatterns = [
    # Users
    path('users/', admin_views.AdminUserListView.as_view(), name='admin-user-list'),
    path('users/<int:pk>/', admin_views.AdminUserDetailView.as_view(), name='admin-user-detail'),
    
    # Sliders
    path('sliders/', admin_views.AdminSliderListCreateView.as_view(), name='admin-slider-list'),
    path('sliders/<int:pk>/', admin_views.AdminSliderDetailView.as_view(), name='admin-slider-detail'),
    
    # Jobs
    path('jobs/', admin_views.AdminJobListView.as_view(), name='admin-job-list'),
    path('jobs/<int:pk>/', admin_views.AdminJobDetailView.as_view(), name='admin-job-detail'),
    
    # Posts
    path('posts/', admin_views.AdminPostListView.as_view(), name='admin-post-list'),
    path('posts/<int:pk>/', admin_views.AdminPostDetailView.as_view(), name='admin-post-detail'),
    
    # Additional Classifieds
    path('properties/', admin_views.AdminPropertyListView.as_view(), name='admin-property-list'),
    path('properties/<int:pk>/', admin_views.AdminPropertyDetailView.as_view(), name='admin-property-detail'),
    path('vehicles/', admin_views.AdminVehicleListView.as_view(), name='admin-vehicle-list'),
    path('vehicles/<int:pk>/', admin_views.AdminVehicleDetailView.as_view(), name='admin-vehicle-detail'),
    path('services/', admin_views.AdminServiceListView.as_view(), name='admin-service-list'),
    path('services/<int:pk>/', admin_views.AdminServiceDetailView.as_view(), name='admin-service-detail'),
    
    # News Articles
    path('articles/', admin_views.AdminArticleListView.as_view(), name='admin-article-list'),
    path('articles/<int:pk>/', admin_views.AdminArticleDetailView.as_view(), name='admin-article-detail'),
    
    # Emergency Services
    path('emergency-services/', admin_views.AdminEmergencyServiceListView.as_view(), name='admin-emergency-service-list'),
    path('emergency-services/<int:pk>/', admin_views.AdminEmergencyServiceDetailView.as_view(), name='admin-emergency-service-detail'),
    
    # Dashboard Stats
    path('dashboard-stats/', admin_views.DashboardStatsView.as_view(), name='admin-dashboard-stats'),
]
