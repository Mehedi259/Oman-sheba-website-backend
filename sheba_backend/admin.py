"""
Custom admin site configuration
"""
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

User = get_user_model()


@method_decorator(staff_member_required, name='dispatch')
class CustomAdminIndexView(TemplateView):
    template_name = 'admin/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Import models here to avoid circular imports
        from classifieds.models import Job, Property, Vehicle, Service
        from news.models import News
        from community.models import Post
        
        # Get counts
        context['user_count'] = User.objects.count()
        context['job_count'] = Job.objects.count()
        context['property_count'] = Property.objects.count()
        context['vehicle_count'] = Vehicle.objects.count()
        context['service_count'] = Service.objects.count()
        context['news_count'] = News.objects.count()
        context['post_count'] = Post.objects.count()
        context['total_classifieds'] = (
            context['job_count'] + 
            context['property_count'] + 
            context['vehicle_count'] + 
            context['service_count']
        )
        
        # Get recent activity
        context['admin_log'] = LogEntry.objects.select_related(
            'user', 'content_type'
        ).order_by('-action_time')[:10]
        
        # Add admin site context
        context.update(admin.site.each_context(self.request))
        context['title'] = 'Dashboard'
        
        return context


class ShebaAdminSite(AdminSite):
    site_header = 'Sheba Administration'
    site_title = 'Sheba Admin'
    index_title = 'Dashboard'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', CustomAdminIndexView.as_view(), name='index'),
        ]
        return custom_urls + urls


# Create custom admin site instance
admin_site = ShebaAdminSite(name='admin')
