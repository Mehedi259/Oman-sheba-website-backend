from django.contrib import admin
from .models import Advertisement, PageView, Setting, AuditLog


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'position', 'status', 'start_date', 'end_date', 'impressions', 'clicks']
    list_filter = ['type', 'status', 'position']
    search_fields = ['title', 'client_name']
    date_hierarchy = 'start_date'


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['path', 'user_id', 'country', 'city', 'created_at']
    list_filter = ['country', 'city', 'created_at']
    search_fields = ['path', 'user_id']
    date_hierarchy = 'created_at'


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'type', 'group', 'updated_at']
    list_filter = ['type', 'group']
    search_fields = ['key', 'description']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'action', 'entity', 'entity_id', 'created_at']
    list_filter = ['action', 'entity', 'created_at']
    search_fields = ['user_id', 'entity', 'entity_id']
    date_hierarchy = 'created_at'
