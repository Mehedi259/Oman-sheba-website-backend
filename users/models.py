from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Enhanced custom user model for Sheba platform"""
    
    # Role & Status
    class UserRole(models.TextChoices):
        USER = 'USER', _('User')
        SERVICE_PROVIDER = 'SERVICE_PROVIDER', _('Service Provider')
        RECRUITER = 'RECRUITER', _('Recruiter')
        ADMIN = 'ADMIN', _('Admin')
        SUPER_ADMIN = 'SUPER_ADMIN', _('Super Admin')
    
    class UserStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', _('Active')
        INACTIVE = 'INACTIVE', _('Inactive')
        SUSPENDED = 'SUSPENDED', _('Suspended')
        DELETED = 'DELETED', _('Deleted')
    
    class Gender(models.TextChoices):
        MALE = 'MALE', _('Male')
        FEMALE = 'FEMALE', _('Female')
        OTHER = 'OTHER', _('Other')
    
    # Contact Information
    phone = models.CharField(max_length=20, blank=True, unique=True, null=True)
    phone_verified = models.BooleanField(default=False)
    email_verified = models.DateTimeField(null=True, blank=True)
    
    # Profile Information
    name = models.CharField(max_length=255, blank=True)
    name_bn = models.CharField(max_length=255, blank=True, verbose_name='Bengali Name')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True)
    nationality = models.CharField(max_length=100, default='Bangladesh')
    passport_no = models.CharField(max_length=50, blank=True)
    oman_id = models.CharField(max_length=50, blank=True)
    
    # OAuth / Social Login
    google_id = models.CharField(max_length=255, blank=True, unique=True, null=True, 
                                  help_text='Google unique user ID')
    auth_provider = models.CharField(max_length=20, default='email', 
                                      choices=[('email', 'Email'), ('google', 'Google')],
                                      help_text='How the user registered')
    avatar_url = models.URLField(max_length=500, blank=True, 
                                  help_text='Profile picture URL from OAuth provider')
    
    # Location
    city = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100, blank=True)
    
    # Preferences
    language = models.CharField(max_length=10, default='bn')
    
    # Role & Status
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.USER)
    status = models.CharField(max_length=20, choices=UserStatus.choices, default=UserStatus.ACTIVE)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name or self.username
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
            models.Index(fields=['role']),
            models.Index(fields=['status']),
        ]


class Favorite(models.Model):
    """User favorites for any content"""
    
    CONTENT_TYPES = [
        ('job', 'Job'),
        ('property', 'Property'),
        ('vehicle', 'Vehicle'),
        ('service', 'Service'),
        ('service_provider', 'Service Provider'),
        ('news', 'News'),
        ('article', 'Article'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    favorite_type = models.CharField(max_length=30, choices=CONTENT_TYPES, db_column='content_type')
    favorite_id = models.PositiveIntegerField(db_column='content_id')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'favorite_type', 'favorite_id']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.favorite_type} #{self.favorite_id}"


class Notification(models.Model):
    """User notifications"""
    
    class NotificationType(models.TextChoices):
        JOB_APPLICATION = 'JOB_APPLICATION', _('Job Application')
        JOB_ALERT = 'JOB_ALERT', _('Job Alert')
        MESSAGE = 'MESSAGE', _('Message')
        BOOKING = 'BOOKING', _('Booking')
        REVIEW = 'REVIEW', _('Review')
        SYSTEM = 'SYSTEM', _('System')
        ANNOUNCEMENT = 'ANNOUNCEMENT', _('Announcement')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=NotificationType.choices)
    title = models.CharField(max_length=255)
    title_bn = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    message_bn = models.TextField(blank=True)
    
    # Link/Action
    link = models.CharField(max_length=500, blank=True)
    action_type = models.CharField(max_length=50, blank=True)
    action_id = models.CharField(max_length=100, blank=True)
    
    # Status
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'read']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Message(models.Model):
    """User messaging system"""
    
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    
    # Thread/Conversation
    thread_id = models.CharField(max_length=100, db_index=True)
    
    # Status
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Attachments (stored as JSON array of URLs)
    attachments = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['thread_id']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Message from {self.sender.username} - {self.created_at}"
