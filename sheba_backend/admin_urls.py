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
]
