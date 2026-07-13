from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
import uuid


class ArticleType(models.TextChoices):
    """Article type choices"""
    NEWS = 'NEWS', _('News')
    BLOG = 'BLOG', _('Blog')
    ANNOUNCEMENT = 'ANNOUNCEMENT', _('Announcement')
    GUIDE = 'GUIDE', _('Guide')
    PAGE = 'PAGE', _('Page')


class PostStatus(models.TextChoices):
    """Post status choices"""
    DRAFT = 'DRAFT', _('Draft')
    PUBLISHED = 'PUBLISHED', _('Published')
    HIDDEN = 'HIDDEN', _('Hidden')
    DELETED = 'DELETED', _('Deleted')


class ArticleCategory(models.Model):
    """Article/News categories"""
    
    name = models.CharField(max_length=255)
    name_bn = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=300, unique=True)
    type = models.CharField(max_length=20, choices=ArticleType.choices)
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Article Categories'
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['type']),
        ]
    
    def __str__(self):
        return self.name


class Article(models.Model):
    """Articles (News, Blog, Announcements, etc.)"""
    
    title = models.CharField(max_length=500)
    title_bn = models.CharField(max_length=500, blank=True)
    slug = models.SlugField(max_length=600, unique=True, blank=True)
    excerpt = models.TextField(blank=True)
    excerpt_bn = models.TextField(blank=True)
    content = models.TextField()
    content_bn = models.TextField(blank=True)
    
    # Type
    type = models.CharField(max_length=20, choices=ArticleType.choices)
    
    # Category
    category = models.ForeignKey(ArticleCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    
    # Media
    featured_image = models.ImageField(upload_to='articles/', blank=True, null=True)
    images = models.JSONField(default=list, blank=True)  # Additional images
    
    # Tags (stored as JSON array)
    tags = models.JSONField(default=list, blank=True)
    
    # SEO
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    
    # Author
    author_name = models.CharField(max_length=255, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    
    # Status & Visibility
    status = models.CharField(max_length=20, choices=PostStatus.choices, default=PostStatus.DRAFT)
    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    
    # Source (for news)
    source = models.CharField(max_length=255, blank=True)
    source_url = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['type']),
            models.Index(fields=['category']),
            models.Index(fields=['status']),
            models.Index(fields=['-published_at']),
        ]
    
    def __str__(self):
        return self.title


# Keep the old News model for backward compatibility
class News(models.Model):
    """News articles (Legacy - for backward compatibility)"""
    
    CATEGORY_CHOICES = [
        ('local', 'Local'),
        ('national', 'National'),
        ('community', 'Community'),
        ('event', 'Event'),
        ('announcement', 'Announcement'),
    ]
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news_articles')
    featured_image = models.ImageField(upload_to='news/', blank=True, null=True)
    
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name_plural = 'News'
    
    def __str__(self):
        return self.title


class NewsComment(models.Model):
    """Comments on news articles"""
    
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.news.title}"
