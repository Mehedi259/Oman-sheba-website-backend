from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from .models import User, Favorite
from .serializers import (
    UserSerializer, UserRegistrationSerializer, FavoriteSerializer,
    GoogleAuthSerializer
)
from .google_auth import verify_google_token, get_or_create_google_user, generate_tokens_for_user, GoogleAuthError


class UserRegistrationView(generics.CreateAPIView):
    """Register a new user"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class LoginView(APIView):
    """User login"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    """User logout"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'})


class GoogleLoginView(APIView):
    """
    Google OAuth Login / Auto-Registration
    
    Accepts a Google ID token from the frontend, verifies it,
    and returns JWT tokens. Creates a new user if one doesn't exist.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        id_token = serializer.validated_data['id_token']
        
        try:
            # Verify Google token
            google_data = verify_google_token(id_token)
            
            # Get or create user
            user, created = get_or_create_google_user(google_data)
            
            # Generate JWT tokens
            tokens = generate_tokens_for_user(user)
            
            # Return tokens and user data
            user_data = UserSerializer(user).data
            
            return Response({
                'access': tokens['access'],
                'refresh': tokens['refresh'],
                'user': user_data,
                'created': created,
            }, status=status.HTTP_200_OK)
            
        except GoogleAuthError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class CurrentUserView(APIView):
    """
    Get current authenticated user info (via JWT token)
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class FavoriteListCreateView(generics.ListCreateAPIView):
    """List and create favorites"""
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteDeleteView(generics.DestroyAPIView):
    """Delete a favorite"""
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    """List all notifications for the current user"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class NotificationUpdateView(generics.UpdateAPIView):
    """Update a notification (e.g. mark as read)"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


from .serializers import ChangePasswordSerializer

class ChangePasswordView(APIView):
    """Change current user password"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)


from classifieds.models import Job, Property, Vehicle, Service, JobApplication
from classifieds.serializers import JobSerializer, PropertySerializer, VehicleSerializer, ServiceSerializer

class UserMyPostsView(APIView):
    """Retrieve all posts created by the authenticated user"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        from django.db.models import Q
        user_filter = Q(user=user)
        if user.email:
            user_filter |= Q(contact_email__iexact=user.email)
        if user.phone:
            user_filter |= Q(contact_phone=user.phone)

        jobs = JobSerializer(Job.objects.filter(user_filter).distinct(), many=True, context={'request': request}).data
        properties = PropertySerializer(Property.objects.filter(user_filter).distinct(), many=True, context={'request': request}).data
        vehicles = VehicleSerializer(Vehicle.objects.filter(user_filter).distinct(), many=True, context={'request': request}).data
        services = ServiceSerializer(Service.objects.filter(user_filter).distinct(), many=True, context={'request': request}).data
        
        # Tag items with category type
        for item in jobs: item['post_type'] = 'job'
        for item in properties: item['post_type'] = 'property'
        for item in vehicles: item['post_type'] = 'vehicle'
        for item in services: item['post_type'] = 'service'
        
        all_posts = jobs + properties + vehicles + services
        all_posts.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return Response(all_posts)


class UserJobApplicationsView(APIView):
    """Retrieve job applications submitted by the current user"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        apps = JobApplication.objects.filter(user=user).select_related('job')
        res = []
        for app in apps:
            res.append({
                'id': app.id,
                'job_id': app.job.id,
                'job_title': app.job.title_bn or app.job.title,
                'company_name': app.job.company.name if app.job.company else '',
                'status': app.status,
                'created_at': app.created_at,
            })
        return Response(res)

