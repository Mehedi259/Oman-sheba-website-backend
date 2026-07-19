from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
import uuid


class PostStatus(models.TextChoices):
    """Post status choices"""
    DRAFT = 'DRAFT', _('Draft')
    PUBLISHED = 'PUBLISHED', _('Published')
    HIDDEN = 'HIDDEN', _('Hidden')
    DELETED = 'DELETED', _('Deleted')


# ==========================================
# COMMUNITY FORUM MODELS
# ==========================================

class ForumCategory(models.Model):
    """Forum categories"""
    
    name = models.CharField(max_length=255)
    name_bn = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=300, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Forum Categories'
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.name


class ForumPost(models.Model):
    """Forum posts with enhanced features"""
    
    title = models.CharField(max_length=500)
    title_bn = models.CharField(max_length=500, blank=True)
    slug = models.SlugField(max_length=600, unique=True, blank=True)
    content = models.TextField()
    content_bn = models.TextField(blank=True)
    
    # Author
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forum_posts')
    
    # Category
    category = models.ForeignKey(ForumCategory, on_delete=models.SET_NULL, null=True, related_name='posts')
    
    # Tags (stored as JSON array)
    tags = models.JSONField(default=list, blank=True)
    
    # Image (optional)
    image = models.ImageField(upload_to='forum_posts/', null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=PostStatus.choices, default=PostStatus.PUBLISHED)
    pinned = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    
    # Statistics
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-pinned', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['author']),
            models.Index(fields=['category']),
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.title


class ForumComment(models.Model):
    """Comments on forum posts with nested replies"""
    
    content = models.TextField()
    
    # Author
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forum_comments')
    
    # Post
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    
    # Parent Comment (for replies)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    
    # Status
    status = models.CharField(max_length=20, choices=PostStatus.choices, default=PostStatus.PUBLISHED)
    likes = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['post']),
            models.Index(fields=['parent']),
        ]
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title[:50]}"


class ForumLike(models.Model):
    """Likes on forum posts"""
    
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='forum_likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['post', 'user']
    
    def __str__(self):
        return f"{self.user.username} likes ForumPost #{self.post.id}"


# ==========================================
# SIMPLE COMMUNITY POSTS (Original)
# ==========================================

class Post(models.Model):
    """Simple community posts"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='community/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"


class Comment(models.Model):
    """Comments on community posts"""
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on Post #{self.post.id}"


class Like(models.Model):
    """Likes on posts"""
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['post', 'user']
    
    def __str__(self):
        return f"{self.user.username} likes Post #{self.post.id}"


# ==========================================
# CLASSIFIEDS SYSTEM
# ==========================================

class ItemCondition(models.TextChoices):
    """Item condition choices"""
    NEW = 'NEW', _('New')
    LIKE_NEW = 'LIKE_NEW', _('Like New')
    GOOD = 'GOOD', _('Good')
    FAIR = 'FAIR', _('Fair')
    POOR = 'POOR', _('Poor')


class ClassifiedCategory(models.Model):
    """Classified categories"""
    
    name = models.CharField(max_length=255)
    name_bn = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=300, unique=True)
    icon = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Classified Categories'
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.name


class Classified(models.Model):
    """Classified ads"""
    
    class ListingStatus(models.TextChoices):
        DRAFT = 'DRAFT', _('Draft')
        PUBLISHED = 'PUBLISHED', _('Published')
        EXPIRED = 'EXPIRED', _('Expired')
        SOLD = 'SOLD', _('Sold')
        REMOVED = 'REMOVED', _('Removed')
    
    title = models.CharField(max_length=500)
    title_bn = models.CharField(max_length=500, blank=True)
    slug = models.SlugField(max_length=600, unique=True, blank=True)
    description = models.TextField()
    description_bn = models.TextField(blank=True)
    
    # Category
    category = models.ForeignKey(ClassifiedCategory, on_delete=models.SET_NULL, null=True, related_name='classifieds')
    
    # Price
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default='OMR')
    price_negotiable = models.BooleanField(default=False)
    
    # Condition
    condition = models.CharField(max_length=20, choices=ItemCondition.choices, blank=True)
    
    # Location
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100, blank=True)
    
    # Media (stored as JSON array)
    images = models.JSONField(default=list, blank=True)
    
    # Contact
    contact_name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=20)
    contact_whatsapp = models.CharField(max_length=20, blank=True)
    
    # Owner
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='classifieds')
    
    # Status
    status = models.CharField(max_length=20, choices=ListingStatus.choices, default=ListingStatus.DRAFT)
    featured = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['owner']),
            models.Index(fields=['category']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.title
