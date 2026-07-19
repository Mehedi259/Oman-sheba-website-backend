from rest_framework import generics
from .models import HeroSlider
from .serializers import HeroSliderSerializer


class HeroSliderListView(generics.ListAPIView):
    """List all active hero sliders, ordered by 'order' field"""
    queryset = HeroSlider.objects.filter(is_active=True)
    serializer_class = HeroSliderSerializer
    pagination_class = None  # No pagination for sliders
