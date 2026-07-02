from rest_framework import serializers
from .models import Job, Property, Vehicle, Service, ClassifiedImage


class ClassifiedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifiedImage
        fields = ['id', 'image', 'is_primary', 'uploaded_at']


class JobSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['id', 'user', 'views', 'created_at', 'updated_at']


class PropertySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ['id', 'user', 'views', 'created_at', 'updated_at']


class VehicleSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ['id', 'user', 'views', 'created_at', 'updated_at']


class ServiceSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ['id', 'user', 'views', 'created_at', 'updated_at']
