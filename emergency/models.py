from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class EmergencyService(models.Model):
    """Emergency service providers"""
    
    SERVICE_TYPE_CHOICES = [
        ('ambulance', 'Ambulance'),
        ('fire', 'Fire Service'),
        ('police', 'Police'),
        ('hospital', 'Hospital'),
        ('pharmacy', 'Pharmacy'),
        ('blood_bank', 'Blood Bank'),
    ]
    
    name = models.CharField(max_length=255)
    name_bn = models.CharField(max_length=255, blank=True, verbose_name='Bengali Name')
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES)
    phone_number = models.CharField(max_length=20)
    alternative_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    location = models.CharField(max_length=200)
    is_24_7 = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    description_bn = models.TextField(blank=True, verbose_name='Bengali Description')
    
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'service_type', 'name']
        indexes = [
            models.Index(fields=['service_type']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()}"


class EmergencyContact(models.Model):
    """User saved emergency contacts"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    alternative_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"
