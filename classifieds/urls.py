from django.urls import path
from . import views

urlpatterns = [
    # Jobs
    path('jobs/', views.JobListCreateView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    path('jobs/<int:pk>/apply/', views.JobApplyView.as_view(), name='job-apply'),
    
    # Properties
    path('properties/', views.PropertyListCreateView.as_view(), name='property-list'),
    path('properties/<int:pk>/', views.PropertyDetailView.as_view(), name='property-detail'),
    
    # Vehicles
    path('vehicles/', views.VehicleListCreateView.as_view(), name='vehicle-list'),
    path('vehicles/<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle-detail'),
    
    # Services
    path('services/', views.ServiceListCreateView.as_view(), name='service-list'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service-detail'),
    # Images
    path('images/', views.ClassifiedImageListCreateView.as_view(), name='image-list-create'),
]
