from rest_framework import serializers
from .models import User, Favorite, Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


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


from classifieds.models import Job, Property, Vehicle, Service
from community.models import Classified as CommunityClassified

class FavoriteSerializer(serializers.ModelSerializer):
    item_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Favorite
        fields = ['id', 'favorite_type', 'favorite_id', 'created_at', 'item_details']
        read_only_fields = ['id', 'created_at']

    def get_item_details(self, obj):
        try:
            item = None
            icon = ''
            if obj.favorite_type == 'job':
                item = Job.objects.get(id=obj.favorite_id)
                icon = '💼'
            elif obj.favorite_type == 'property':
                item = Property.objects.get(id=obj.favorite_id)
                icon = '🏠'
            elif obj.favorite_type == 'vehicle':
                item = Vehicle.objects.get(id=obj.favorite_id)
                icon = '🚗'
            elif obj.favorite_type == 'service':
                item = Service.objects.get(id=obj.favorite_id)
                icon = '🛠️'
            elif obj.favorite_type == 'classified':
                item = CommunityClassified.objects.get(id=obj.favorite_id)
                icon = '🛒'
                
            if item:
                return {
                    'title': item.title,
                    'title_bn': getattr(item, 'title_bn', ''),
                    'description': item.description[:100] + '...' if item.description else '',
                    'location': item.city,
                    'price': str(item.price) if getattr(item, 'price', None) else '',
                    'icon': icon,
                    'status': item.status
                }
        except Exception:
            pass
        return None

