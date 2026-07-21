from rest_framework import generics, filters
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job, Property, Vehicle, Service, ClassifiedImage
from .serializers import JobSerializer, PropertySerializer, VehicleSerializer, ServiceSerializer, ClassifiedImageSerializer


class JobListCreateView(generics.ListCreateAPIView):
    """List all jobs or create new job"""
    queryset = Job.objects.filter(status='PUBLISHED')
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'category', 'city']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price', 'views']
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a job"""
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        return super().retrieve(request, *args, **kwargs)


class PropertyListCreateView(generics.ListCreateAPIView):
    """List all properties or create new property"""
    queryset = Property.objects.filter(status='PUBLISHED')
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'purpose', 'city', 'bedrooms']
    search_fields = ['title', 'description', 'city']
    ordering_fields = ['created_at', 'price', 'views']
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a property"""
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        return super().retrieve(request, *args, **kwargs)


class VehicleListCreateView(generics.ListCreateAPIView):
    """List all vehicles or create new vehicle"""
    queryset = Vehicle.objects.filter(status='PUBLISHED')
    serializer_class = VehicleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['make', 'condition', 'city', 'year']
    search_fields = ['title', 'description', 'make', 'model']
    ordering_fields = ['created_at', 'price', 'views', 'year']
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VehicleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a vehicle"""
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        return super().retrieve(request, *args, **kwargs)


class ServiceFilter(django_filters.FilterSet):
    category__slug = django_filters.CharFilter(field_name='category', lookup_expr='iexact')
    
    class Meta:
        model = Service
        fields = ['category', 'city']


class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.filter(status='PUBLISHED')
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ServiceFilter
    search_fields = ['title', 'description', 'category', 'service_type']
    ordering_fields = ['created_at', 'price', 'views']
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a service"""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        return super().retrieve(request, *args, **kwargs)


class ClassifiedImageListCreateView(generics.ListCreateAPIView):
    """Upload and list classified images"""
    queryset = ClassifiedImage.objects.all()
    serializer_class = ClassifiedImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['content_type', 'content_id']
