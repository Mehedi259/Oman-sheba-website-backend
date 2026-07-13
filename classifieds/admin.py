from django.contrib import admin
from .models import Job, Property, Vehicle, Service, ClassifiedImage


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'type', 'city', 'status', 'created_at']
    list_filter = ['type', 'status', 'category']
    search_fields = ['title', 'company__name', 'description']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'listing', 'price', 'city', 'status']
    list_filter = ['type', 'listing', 'status']
    search_fields = ['title', 'description', 'city']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['title', 'make', 'model', 'year', 'price', 'condition', 'status']
    list_filter = ['make', 'condition', 'status', 'year']
    search_fields = ['title', 'make', 'model']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'service_type', 'city', 'status']
    list_filter = ['category', 'status']
    search_fields = ['title', 'category', 'description']


@admin.register(ClassifiedImage)
class ClassifiedImageAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'content_id', 'is_primary', 'uploaded_at']
    list_filter = ['content_type', 'is_primary']
