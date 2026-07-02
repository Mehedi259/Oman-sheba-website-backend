from django.urls import path
from . import views

urlpatterns = [
    path('services/', views.EmergencyServiceListView.as_view(), name='emergency-service-list'),
    path('services/<int:pk>/', views.EmergencyServiceDetailView.as_view(), name='emergency-service-detail'),
    path('contacts/', views.EmergencyContactListCreateView.as_view(), name='emergency-contact-list'),
    path('contacts/<int:pk>/', views.EmergencyContactDetailView.as_view(), name='emergency-contact-detail'),
]
