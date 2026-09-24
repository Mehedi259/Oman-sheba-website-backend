from rest_framework import serializers
from .models import HeroSlider


class HeroSliderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = HeroSlider
        fields = [
            'id', 'title', 'title_bn', 'subtitle', 'subtitle_bn',
            'image', 'cta_text', 'link', 'is_external',
            'overlay_gradient', 'order', 'is_active',
            'created_at', 'updated_at'
        ]
