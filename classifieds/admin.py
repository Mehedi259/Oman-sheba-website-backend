from django.contrib import admin
from .models import Job, Property, Vehicle, Service, ClassifiedImage


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'job_type', 'location', 'status', 'created_at']
    list_filter = ['job_type', 'status', 'category']
    search_fields = ['title', 'company_name', 'description']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'listing_type', 'price', 'location', 'status']
    list_filter = ['property_type', 'listing_type', 'status']
    search_fields = ['title', 'description', 'location']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand', 'model', 'year', 'price', 'condition', 'status']
    list_filter = ['brand', 'condition', 'status', 'year']
    search_fields = ['title', 'brand', 'model']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'service_type', 'location', 'status']
    list_filter = ['category', 'status']
    search_fields = ['title', 'category', 'description']


@admin.register(ClassifiedImage)
class ClassifiedImageAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'content_id', 'is_primary', 'uploaded_at']
    list_filter = ['content_type', 'is_primary']
