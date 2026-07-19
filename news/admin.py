from django.contrib import admin
from django.utils.html import format_html
from .models import News, NewsComment, Article, ArticleCategory


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_bn', 'type', 'order']
    list_filter = ['type']
    search_fields = ['name', 'name_bn']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_preview', 'type', 'category', 'status', 'featured', 'views', 'published_at']
    list_filter = ['type', 'status', 'featured', 'category']
    search_fields = ['title', 'title_bn', 'content', 'content_bn']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'featured']
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('কন্টেন্ট (English)', {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('কন্টেন্ট (বাংলা)', {
            'fields': ('title_bn', 'excerpt_bn', 'content_bn'),
            'classes': ('collapse',),
        }),
        ('টাইপ ও ক্যাটাগরি', {
            'fields': ('type', 'category', 'tags')
        }),
        ('মিডিয়া', {
            'fields': ('featured_image', 'images')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
        ('লেখক ও সোর্স', {
            'fields': ('author_name', 'author', 'source', 'source_url'),
            'classes': ('collapse',),
        }),
        ('পাবলিশ সেটিংস', {
            'fields': ('status', 'featured', 'published_at')
        }),
    )
    
    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="width:80px;height:50px;object-fit:cover;border-radius:4px;" />', obj.featured_image.url)
        return '-'
    image_preview.short_description = 'ছবি'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_published', 'is_featured', 'published_at']
    list_filter = ['category', 'is_published', 'is_featured']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'news', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'user__username', 'news__title']
