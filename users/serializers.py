from rest_framework import serializers
from .models import User, Favorite


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'name', 'phone', 'avatar', 'avatar_url', 'bio', 'city', 
                  'auth_provider', 'created_at', 'updated_at']
        read_only_fields = ['id', 'auth_provider', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 
                  'first_name', 'last_name', 'phone']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class GoogleAuthSerializer(serializers.Serializer):
    """Serializer for Google OAuth login request"""
    id_token = serializers.CharField(
        required=True,
        help_text='Google ID token received from Google Sign-In on the frontend'
    )


class TokenResponseSerializer(serializers.Serializer):
    """Serializer for JWT token response"""
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)
    created = serializers.BooleanField(
        read_only=True,
        help_text='True if user was newly registered'
    )


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'favorite_type', 'favorite_id', 'created_at']
        read_only_fields = ['id', 'created_at']

