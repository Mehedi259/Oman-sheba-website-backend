from django.db import models
from django.conf import settings


class BaseClassified(models.Model):
    """Base model for all classified listings"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('expired', 'Expired'),
        ('deleted', 'Deleted'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    views = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ['-created_at']


class Job(BaseClassified):
    """Job listings"""
    
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
    ]
    
    company_name = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    category = models.CharField(max_length=100)
    experience_required = models.CharField(max_length=100, blank=True)
    salary_range = models.CharField(max_length=100, blank=True)
    deadline = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} at {self.company_name}"


class Property(BaseClassified):
    """Property listings"""
    
    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('commercial', 'Commercial'),
        ('land', 'Land'),
    ]
    
    LISTING_TYPE_CHOICES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    ]
    
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPE_CHOICES)
    bedrooms = models.PositiveIntegerField(null=True, blank=True)
    bathrooms = models.PositiveIntegerField(null=True, blank=True)
    area_sqft = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.property_type} - {self.title}"


class Vehicle(BaseClassified):
    """Vehicle listings"""
    
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
        ('reconditioned', 'Reconditioned'),
    ]
    
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    mileage = models.PositiveIntegerField(null=True, blank=True)
    fuel_type = models.CharField(max_length=50, blank=True)
    transmission = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.year} {self.brand} {self.model}"


class Service(BaseClassified):
    """Service listings"""
    
    category = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100)
    availability = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.category}"


class ClassifiedImage(models.Model):
    """Images for classified listings"""
    
    CONTENT_TYPE_CHOICES = [
        ('job', 'Job'),
        ('property', 'Property'),
        ('vehicle', 'Vehicle'),
        ('service', 'Service'),
    ]
    
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    content_id = models.PositiveIntegerField()
    image = models.ImageField(upload_to='classifieds/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', 'uploaded_at']
    
    def __str__(self):
        return f"{self.content_type} #{self.content_id} - Image"
