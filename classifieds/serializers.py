from rest_framework import serializers
from .models import Job, Property, Vehicle, Service, ClassifiedImage, Company


class ClassifiedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifiedImage
        fields = ['id', 'content_type', 'content_id', 'image', 'is_primary', 'uploaded_at']


class JobSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    company_name_en = serializers.CharField(write_only=True, required=False)
    company_name_bn = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['id', 'user', 'views', 'created_at', 'updated_at']
        extra_kwargs = {
            'company': {'required': False, 'allow_null': True},
            'contact_name': {'required': False, 'allow_blank': True},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None

        # Auto-fill contact_name
        if not validated_data.get('contact_name') and user:
            validated_data['contact_name'] = getattr(user, 'name', user.first_name) or user.username

        # Handle company creation
        company_en = validated_data.pop('company_name_en', None)
        company_bn = validated_data.pop('company_name_bn', None)
        
        if not validated_data.get('company') and company_en:
            company, _ = Company.objects.get_or_create(
                name=company_en,
                defaults={'name_bn': company_bn or ''}
            )
            validated_data['company'] = company

        return super().create(validated_data)


class PropertySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ['id', 'user', 'views', 'created_at', 'updated_at']
        extra_kwargs = {
            'contact_name': {'required': False, 'allow_blank': True},
            'category': {'required': False, 'allow_blank': True},
            'type': {'required': False, 'allow_blank': True},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None

        if not validated_data.get('contact_name') and user:
            validated_data['contact_name'] = getattr(user, 'name', user.first_name) or user.username

        return super().create(validated_data)


class VehicleSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ['id', 'user', 'views', 'created_at', 'updated_at']
        extra_kwargs = {
            'contact_name': {'required': False, 'allow_blank': True},
            'purpose': {'required': False, 'allow_blank': True},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None

        if not validated_data.get('contact_name') and user:
            validated_data['contact_name'] = getattr(user, 'name', user.first_name) or user.username
            
        # Default purpose if missing
        if not validated_data.get('purpose'):
            validated_data['purpose'] = 'SALE'

        return super().create(validated_data)


class ServiceSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ['id', 'user', 'views', 'created_at', 'updated_at']
        extra_kwargs = {
            'contact_name': {'required': False, 'allow_blank': True},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None

        if not validated_data.get('contact_name') and user:
            validated_data['contact_name'] = getattr(user, 'name', user.first_name) or user.username

        return super().create(validated_data)
