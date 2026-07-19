from django.contrib import admin
from django.utils.html import format_html
from .models import Advertisement, PageView, Setting, AuditLog, HeroSlider


@admin.register(HeroSlider)
class HeroSliderAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'image_preview', 'cta_text', 'is_active', 'is_external', 'created_at']
    list_filter = ['is_active', 'is_external']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'title_bn', 'subtitle']
    ordering = ['order']
    
    fieldsets = (
        ('কন্টেন্ট', {
            'fields': ('title', 'title_bn', 'subtitle', 'subtitle_bn')
        }),
        ('মিডিয়া ও লিঙ্ক', {
            'fields': ('image', 'cta_text', 'link', 'is_external')
        }),
        ('ডিজাইন', {
            'fields': ('overlay_gradient',),
            'classes': ('collapse',),
        }),
        ('সেটিংস', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:120px;height:40px;object-fit:cover;border-radius:4px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'প্রিভিউ'


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
