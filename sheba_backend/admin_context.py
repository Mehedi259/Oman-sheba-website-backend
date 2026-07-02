"""
Custom admin context processor for dashboard
"""
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model

User = get_user_model()


def admin_dashboard_context(request):
    """
    Provide context data for custom admin dashboard
    """
    if not request.path.startswith('/admin/'):
        return {}
    
    context = {}
    
    # Get user count
    context['user_count'] = User.objects.count()
    
    # Get recent activity (last 10 actions)
    context['admin_log'] = LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:10]
    
    # Get model counts for stats
    from classifieds.models import Job, Property, Vehicle, Service
    from news.models import News
    from community.models import Post
    
    context['job_count'] = Job.objects.count()
    context['property_count'] = Property.objects.count()
    context['vehicle_count'] = Vehicle.objects.count()
    context['service_count'] = Service.objects.count()
    context['news_count'] = News.objects.count()
    context['post_count'] = Post.objects.count()
    
    # Total classifieds
    context['total_classifieds'] = (
        context['job_count'] + 
        context['property_count'] + 
        context['vehicle_count'] + 
        context['service_count']
    )
    
    return context
