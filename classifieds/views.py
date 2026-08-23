from rest_framework import generics, filters
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job, Property, Vehicle, Service, ClassifiedImage, Review
from .serializers import JobSerializer, PropertySerializer, VehicleSerializer, ServiceSerializer, ClassifiedImageSerializer, ReviewSerializer


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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import JobApplication

class JobApplyView(APIView):
    """Apply for a job or check application status"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            job = Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        
        cover_letter = request.data.get('cover_letter', '')
        application, created = JobApplication.objects.get_or_create(
            job=job,
            user=request.user,
            defaults={'cover_letter': cover_letter}
        )
        if not created:
            return Response({'message': 'You have already applied for this job', 'applied': True}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Application submitted successfully', 'id': application.id, 'applied': True}, status=status.HTTP_201_CREATED)

    def get(self, request, pk):
        applied = JobApplication.objects.filter(job_id=pk, user=request.user).exists()
        return Response({'applied': applied})


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


class ReviewListCreateView(generics.ListCreateAPIView):
    """Submit and list reviews for classifieds"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reviewable_type', 'reviewable_id']

    def perform_create(self, serializer):
        # Save the review
        review = serializer.save(user=self.request.user)
        
        # Update the aggregated rating on the target object
        try:
            target_model = None
            if review.reviewable_type == 'job': target_model = Job
            elif review.reviewable_type == 'property': target_model = Property
            elif review.reviewable_type == 'vehicle': target_model = Vehicle
            elif review.reviewable_type == 'service': target_model = Service
            
            if target_model:
                target = target_model.objects.get(id=review.reviewable_id)
                # Recalculate average
                reviews = Review.objects.filter(reviewable_type=review.reviewable_type, reviewable_id=review.reviewable_id)
                total_rating = sum(r.rating for r in reviews)
                count = reviews.count()
                
                target.rating = total_rating / count if count > 0 else 0
                target.review_count = count
                target.save(update_fields=['rating', 'review_count'])
        except Exception as e:
            print("Failed to update aggregate rating:", e)
