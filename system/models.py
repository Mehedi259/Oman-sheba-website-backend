from django.db import models
from django.utils.translation import gettext_lazy as _


# ==========================================
# ADVERTISEMENT SYSTEM
# ==========================================

class AdType(models.TextChoices):
    """Advertisement type choices"""
    BANNER = 'BANNER', _('Banner')
    SIDEBAR = 'SIDEBAR', _('Sidebar')
    INLINE = 'INLINE', _('Inline')
    POPUP = 'POPUP', _('Popup')


class AdStatus(models.TextChoices):
    """Advertisement status choices"""
    PENDING = 'PENDING', _('Pending')
    ACTIVE = 'ACTIVE', _('Active')
    PAUSED = 'PAUSED', _('Paused')
    EXPIRED = 'EXPIRED', _('Expired')


class Advertisement(models.Model):
    """Advertisement management"""
    
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='ads/')
    link = models.URLField(blank=True)
    position = models.CharField(max_length=100)  # "banner_top", "sidebar_right", etc.
    type = models.CharField(max_length=20, choices=AdType.choices)
    
    # Targeting (stored as JSON arrays)
    pages = models.JSONField(default=list)  # ["home", "jobs", "property"]
    cities = models.JSONField(default=list)
    
    # Schedule
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    # Status
    status = models.CharField(max_length=20, choices=AdStatus.choices, default=AdStatus.PENDING)
    
    # Statistics
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    
    # Client
    client_name = models.CharField(max_length=255, blank=True)
    client_email = models.EmailField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['position']),
            models.Index(fields=['status']),
            models.Index(fields=['start_date', 'end_date']),
        ]
    
    def __str__(self):
        return self.title


# ==========================================
# ANALYTICS & TRACKING
# ==========================================

class PageView(models.Model):
    """Page view tracking"""
    
    path = models.CharField(max_length=500)
    referrer = models.CharField(max_length=500, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    # User (optional, if logged in)
    user_id = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['path']),
            models.Index(fields=['user_id']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.path} - {self.created_at}"


# ==========================================
# SYSTEM CONFIGURATION
# ==========================================

class Setting(models.Model):
    """System settings/configuration"""
    
    TYPE_CHOICES = [
        ('string', 'String'),
        ('number', 'Number'),
        ('boolean', 'Boolean'),
        ('json', 'JSON'),
    ]
    
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='string')
    description = models.TextField(blank=True)
    group = models.CharField(max_length=100, blank=True)  # "general", "email", "payment"
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['group', 'key']
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['group']),
        ]
    
    def __str__(self):
        return self.key


class AuditLog(models.Model):
    """Audit log for tracking changes"""
    
    user_id = models.CharField(max_length=100, blank=True)
    action = models.CharField(max_length=100)
    entity = models.CharField(max_length=100)
    entity_id = models.CharField(max_length=100, blank=True)
    changes = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['entity']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.action} on {self.entity} - {self.created_at}"
