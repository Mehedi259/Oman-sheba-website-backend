from django.contrib import admin
from .models import News, NewsComment


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
