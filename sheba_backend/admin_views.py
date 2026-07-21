from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from system.models import HeroSlider
from system.serializers import HeroSliderSerializer
from users.serializers import UserSerializer
from classifieds.models import Job
from classifieds.serializers import JobSerializer
from community.models import Post
from community.serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from emergency.models import EmergencyService
from emergency.serializers import EmergencyServiceSerializer
from news.models import Article
from news.serializers import ArticleSerializer
from classifieds.models import Property, Vehicle, Service
from classifieds.serializers import PropertySerializer, VehicleSerializer, ServiceSerializer

User = get_user_model()

# Users Admin
class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

# Sliders Admin
class AdminSliderListCreateView(generics.ListCreateAPIView):
    queryset = HeroSlider.objects.all().order_by('order')
    serializer_class = HeroSliderSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminSliderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HeroSlider.objects.all()
    serializer_class = HeroSliderSerializer
    permission_classes = [permissions.IsAdminUser]

# Jobs Admin
class AdminJobListView(generics.ListAPIView):
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminJobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAdminUser]

# Community Posts Admin
class AdminPostListView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]

# Additional Classifieds Admin (Properties, Vehicles, Services)
class AdminPropertyListView(generics.ListAPIView):
    queryset = Property.objects.all().order_by('-created_at')
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAdminUser]

class AdminPropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAdminUser]

class AdminVehicleListView(generics.ListAPIView):
    queryset = Vehicle.objects.all().order_by('-created_at')
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminVehicleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminServiceListView(generics.ListAPIView):
    queryset = Service.objects.all().order_by('-created_at')
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAdminUser]

# News Articles Admin
class AdminArticleListView(generics.ListCreateAPIView):
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAdminUser]

# Emergency Services Admin
class AdminEmergencyServiceListView(generics.ListCreateAPIView):
    queryset = EmergencyService.objects.all().order_by('order', 'name')
    serializer_class = EmergencyServiceSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminEmergencyServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmergencyService.objects.all()
    serializer_class = EmergencyServiceSerializer
    permission_classes = [permissions.IsAdminUser]

# Dashboard Stats
class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        user_count = User.objects.count()
        job_count = Job.objects.count()
        property_count = Property.objects.count()
        vehicle_count = Vehicle.objects.count()
        service_count = Service.objects.count()
        total_classifieds = job_count + property_count + vehicle_count + service_count
        news_count = Article.objects.count()
        post_count = Post.objects.count()
        emergency_count = EmergencyService.objects.count()

        # Growth Data (Last 6 months users)
        six_months_ago = timezone.now() - timedelta(days=180)
        growth_data_raw = User.objects.filter(date_joined__gte=six_months_ago) \
            .annotate(month=TruncMonth('date_joined')) \
            .values('month') \
            .annotate(users=Count('id')) \
            .order_by('month')

        growth_data = []
        for item in growth_data_raw:
            growth_data.append({
                'name': item['month'].strftime('%b'),
                'users': item['users'],
                'jobs': 0  # We can optionally add jobs growth later, leaving as 0 to match UI structure
            })
            
        # Ensure we return at least some dummy structure for months if no users found
        if not growth_data:
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            growth_data = [{'name': m, 'users': 0, 'jobs': 0} for m in months]

        return Response({
            'user_count': user_count,
            'job_count': job_count,
            'property_count': property_count,
            'vehicle_count': vehicle_count,
            'service_count': service_count,
            'total_classifieds': total_classifieds,
            'news_count': news_count,
            'post_count': post_count,
            'emergency_count': emergency_count,
            'growth_data': growth_data
        })
