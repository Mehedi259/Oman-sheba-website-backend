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

