from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model for Sheba platform"""
    
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ['-created_at']


class Favorite(models.Model):
    """User favorites for any content"""
    
    CONTENT_TYPES = [
        ('job', 'Job'),
        ('property', 'Property'),
        ('vehicle', 'Vehicle'),
        ('service', 'Service'),
        ('news', 'News'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    content_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'content_type', 'content_id']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.content_type} #{self.content_id}"
