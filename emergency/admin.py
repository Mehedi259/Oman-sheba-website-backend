from django.contrib import admin
from .models import EmergencyService, EmergencyContact


@admin.register(EmergencyService)
class EmergencyServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_type', 'phone_number', 'location', 'is_24_7', 'is_active']
    list_filter = ['service_type', 'is_24_7', 'is_active', 'location']
    search_fields = ['name', 'phone_number', 'description']


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'relationship', 'phone_number']
    list_filter = ['relationship']
    search_fields = ['name', 'phone_number', 'user__username']
