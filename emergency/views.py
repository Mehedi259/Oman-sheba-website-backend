from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import EmergencyService, EmergencyContact
from .serializers import EmergencyServiceSerializer, EmergencyContactSerializer


class EmergencyServiceListView(generics.ListAPIView):
    """List all emergency services"""
    queryset = EmergencyService.objects.filter(is_active=True)
    serializer_class = EmergencyServiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['service_type', 'location', 'is_24_7']
    search_fields = ['name', 'description', 'address']


class EmergencyServiceDetailView(generics.RetrieveAPIView):
    """Retrieve emergency service details"""
    queryset = EmergencyService.objects.filter(is_active=True)
    serializer_class = EmergencyServiceSerializer


class EmergencyContactListCreateView(generics.ListCreateAPIView):
    """List and create user emergency contacts"""
    serializer_class = EmergencyContactSerializer
    
    def get_queryset(self):
        return EmergencyContact.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EmergencyContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete emergency contact"""
    serializer_class = EmergencyContactSerializer
    
    def get_queryset(self):
        return EmergencyContact.objects.filter(user=self.request.user)
