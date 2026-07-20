from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from system.models import HeroSlider
from system.serializers import HeroSliderSerializer
from users.serializers import UserSerializer
from classifieds.models import Job
from classifieds.serializers import JobSerializer
from community.models import Post
from community.serializers import PostSerializer

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
