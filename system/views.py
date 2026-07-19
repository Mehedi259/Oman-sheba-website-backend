from rest_framework import generics
from .models import HeroSlider
from .serializers import HeroSliderSerializer


class HeroSliderListView(generics.ListAPIView):
    """List all active hero sliders, ordered by 'order' field"""
    queryset = HeroSlider.objects.filter(is_active=True)
    serializer_class = HeroSliderSerializer
    pagination_class = None  # No pagination for sliders


from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from classifieds.models import Job, Property, Vehicle, Service
from community.models import Classified as CommunityClassified

class GlobalSearchView(APIView):
    """Global search across multiple models"""
    permission_classes = []
    
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response([])
            
        results = []
        
        # Helper to format results
        def add_results(queryset, item_type, icon_str):
            for item in queryset[:5]: # Limit 5 per category
                results.append({
                    'id': item.id,
                    'type': item_type,
                    'title': item.title,
                    'title_bn': getattr(item, 'title_bn', ''),
                    'description': item.description[:100] + '...' if item.description else '',
                    'location': item.city,
                    'price': str(item.price) if getattr(item, 'price', None) else '',
                    'icon': icon_str,
                })
                
        # Search Jobs
        jobs = Job.objects.filter(
            Q(title__icontains=query) | 
            Q(title_bn__icontains=query) | 
            Q(description__icontains=query)
        ).filter(status='PUBLISHED')
        add_results(jobs, 'job', '💼')
        
        # Search Properties
        properties = Property.objects.filter(
            Q(title__icontains=query) | 
            Q(title_bn__icontains=query) | 
            Q(description__icontains=query)
        ).filter(status='PUBLISHED')
        add_results(properties, 'property', '🏠')
        
        # Search Vehicles
        vehicles = Vehicle.objects.filter(
            Q(title__icontains=query) | 
            Q(title_bn__icontains=query) | 
            Q(description__icontains=query)
        ).filter(status='PUBLISHED')
        add_results(vehicles, 'vehicle', '🚗')
        
        # Search Services
        services = Service.objects.filter(
            Q(title__icontains=query) | 
            Q(title_bn__icontains=query) | 
            Q(description__icontains=query)
        ).filter(status='PUBLISHED')
        add_results(services, 'service', '🛠️')
        
        # Search Classifieds (Market)
        classifieds = CommunityClassified.objects.filter(
            Q(title__icontains=query) | 
            Q(title_bn__icontains=query) | 
            Q(description__icontains=query)
        ).filter(status='PUBLISHED')
        add_results(classifieds, 'classified', '🛒')
        
        return Response(results)
