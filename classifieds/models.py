from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
import uuid


class ListingStatus(models.TextChoices):
    """Status for all listings"""
    DRAFT = 'DRAFT', _('Draft')
    PUBLISHED = 'PUBLISHED', _('Published')
    EXPIRED = 'EXPIRED', _('Expired')
    SOLD = 'SOLD', _('Sold')
    REMOVED = 'REMOVED', _('Removed')


class BaseClassified(models.Model):
    """Base model for all classified listings"""
    
    title = models.CharField(max_length=255)
    title_bn = models.CharField(max_length=255, blank=True, verbose_name='Bengali Title')
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    description = models.TextField()
    description_bn = models.TextField(blank=True, verbose_name='Bengali Description')
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_listings')
    
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default='OMR')
    price_negotiable = models.BooleanField(default=False)
    
    # Contact
    contact_name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField(blank=True)
    contact_whatsapp = models.CharField(max_length=20, blank=True)
    
    # Status & Visibility
    status = models.CharField(max_length=20, choices=ListingStatus.choices, default=ListingStatus.DRAFT)
    featured = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    
    # SEO
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    
    # Timestamps
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
        abstract = True
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['city']),
            models.Index(fields=['created_at']),
        ]


# ==========================================
# JOB PORTAL MODELS
# ==========================================

class JobType(models.TextChoices):
    """Job type choices"""
    FULL_TIME = 'FULL_TIME', _('Full Time')
    PART_TIME = 'PART_TIME', _('Part Time')
    CONTRACT = 'CONTRACT', _('Contract')
    TEMPORARY = 'TEMPORARY', _('Temporary')
    INTERNSHIP = 'INTERNSHIP', _('Internship')


class JobStatus(models.TextChoices):
    """Job status choices"""
    DRAFT = 'DRAFT', _('Draft')
    PUBLISHED = 'PUBLISHED', _('Published')
    CLOSED = 'CLOSED', _('Closed')
    EXPIRED = 'EXPIRED', _('Expired')


class JobCategory(models.Model):
    """Job categories with hierarchy support"""
    
    name = models.CharField(max_length=255)
    name_bn = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=300, unique=True)
    icon = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    
    # Hierarchy
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Job Categories'
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.name


class ServiceProviderStatus(models.TextChoices):
    """Status for service providers and companies"""
    PENDING = 'PENDING', _('Pending')
    APPROVED = 'APPROVED', _('Approved')
    REJECTED = 'REJECTED', _('Rejected')
    SUSPENDED = 'SUSPENDED', _('Suspended')


class Company(models.Model):
    """Company/Employer profiles"""
    
    name = models.CharField(max_length=255)
    name_bn = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    logo = models.ImageField(upload_to='companies/logos/', blank=True, null=True)
    cover = models.ImageField(upload_to='companies/covers/', blank=True, null=True)
    description = models.TextField(blank=True)
    description_bn = models.TextField(blank=True)
    
    # Contact
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    
    # Location
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='Oman')
    
    # Social
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    
    # Verification
    verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    # Statistics
    employee_count = models.CharField(max_length=50, blank=True)  # "10-50", "50-200"
    founded_year = models.IntegerField(null=True, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=ServiceProviderStatus.choices, default=ServiceProviderStatus.PENDING)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['verified']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.name


class Job(BaseClassified):
    """Job listings with complete features"""
    
    # Company Information
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    
    # Job Details
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, related_name='jobs')
    type = models.CharField(max_length=20, choices=JobType.choices)
    experience = models.CharField(max_length=200, blank=True)  # "0-2 years", "3-5 years"
    education = models.CharField(max_length=200, blank=True)
    vacancy = models.PositiveIntegerField(default=1)
    
    # Salary
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=10, default='OMR')
    salary_period = models.CharField(max_length=20, default='MONTHLY')  # MONTHLY, YEARLY
    
    # Requirements (stored as JSON arrays)
    skills = models.JSONField(default=list, blank=True)
    benefits = models.JSONField(default=list, blank=True)
    
    # Application
    application_deadline = models.DateTimeField(null=True, blank=True)
    application_email = models.EmailField(blank=True)
    application_phone = models.CharField(max_length=20, blank=True)
    application_url = models.URLField(blank=True)
    
    # Override status from BaseClassified
    job_status = models.CharField(max_length=20, choices=JobStatus.choices, default=JobStatus.DRAFT, db_column='job_specific_status')
    
    def __str__(self):
        return f"{self.title} at {self.company.name}"
    
    class Meta(BaseClassified.Meta):
        indexes = BaseClassified.Meta.indexes + [
            models.Index(fields=['company']),
            models.Index(fields=['category']),
            models.Index(fields=['type']),
        ]


class ApplicationStatus(models.TextChoices):
    """Job application status"""
    PENDING = 'PENDING', _('Pending')
    REVIEWING = 'REVIEWING', _('Reviewing')
    SHORTLISTED = 'SHORTLISTED', _('Shortlisted')
    INTERVIEWED = 'INTERVIEWED', _('Interviewed')
    OFFERED = 'OFFERED', _('Offered')
    ACCEPTED = 'ACCEPTED', _('Accepted')
    REJECTED = 'REJECTED', _('Rejected')


class JobApplication(models.Model):
    """Job applications"""
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_applications')
    
    # Application Data
    cover_letter = models.TextField(blank=True)
    cv_url = models.FileField(upload_to='cvs/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.PENDING)
    
    # Tracking
    viewed_at = models.DateTimeField(null=True, blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['job', 'user']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['job']),
            models.Index(fields=['user']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} applied to {self.job.title}"


class SavedJob(models.Model):
    """Saved/Bookmarked jobs"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'job']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"


# ==========================================
# PROPERTY MODELS
# ==========================================

class PropertyType(models.TextChoices):
    """Property type choices"""
    RESIDENTIAL = 'RESIDENTIAL', _('Residential')
    COMMERCIAL = 'COMMERCIAL', _('Commercial')
    LAND = 'LAND', _('Land')


class PropertyCategory(models.TextChoices):
    """Property category choices"""
    HOUSE = 'HOUSE', _('House')
    FLAT = 'FLAT', _('Flat')
    APARTMENT = 'APARTMENT', _('Apartment')
    VILLA = 'VILLA', _('Villa')
    ROOM = 'ROOM', _('Room')
    BED_SPACE = 'BED_SPACE', _('Bed Space')
    OFFICE = 'OFFICE', _('Office')
    SHOP = 'SHOP', _('Shop')
    WAREHOUSE = 'WAREHOUSE', _('Warehouse')
    SHOWROOM = 'SHOWROOM', _('Showroom')
    LAND = 'LAND', _('Land')
    BUILDING = 'BUILDING', _('Building')


class PropertyPurpose(models.TextChoices):
    """Property purpose choices"""
    RENT = 'RENT', _('For Rent')
    SALE = 'SALE', _('For Sale')
    BOTH = 'BOTH', _('Both')


class FurnishedStatus(models.TextChoices):
    """Furnished status choices"""
    FURNISHED = 'FURNISHED', _('Furnished')
    SEMI_FURNISHED = 'SEMI_FURNISHED', _('Semi Furnished')
    UNFURNISHED = 'UNFURNISHED', _('Unfurnished')


class Property(BaseClassified):
    """Property listings with enhanced features"""
    
    # Type & Category
    type = models.CharField(max_length=20, choices=PropertyType.choices)
    category = models.CharField(max_length=20, choices=PropertyCategory.choices)
    purpose = models.CharField(max_length=20, choices=PropertyPurpose.choices)
    
    # Location
    address = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # Details
    bedrooms = models.PositiveIntegerField(null=True, blank=True)
    bathrooms = models.PositiveIntegerField(null=True, blank=True)
    size = models.FloatField(null=True, blank=True)  # sqft or sqm
    size_unit = models.CharField(max_length=10, default='sqft')
    floor = models.IntegerField(null=True, blank=True)
    total_floors = models.IntegerField(null=True, blank=True)
    furnished = models.CharField(max_length=20, choices=FurnishedStatus.choices, blank=True)
    
    # Amenities (stored as JSON array)
    amenities = models.JSONField(default=list, blank=True)
    
    # Media (stored as JSON arrays)
    images = models.JSONField(default=list, blank=True)
    videos = models.JSONField(default=list, blank=True)
    virtual_tour = models.URLField(blank=True)
    
    # Availability
    available_from = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_category_display()} - {self.title}"
    
    class Meta(BaseClassified.Meta):
        verbose_name_plural = 'Properties'
        indexes = BaseClassified.Meta.indexes + [
            models.Index(fields=['type']),
            models.Index(fields=['category']),
            models.Index(fields=['purpose']),
        ]


# ==========================================
# VEHICLE MODELS
# ==========================================

class VehicleType(models.TextChoices):
    """Vehicle type choices"""
    CAR = 'CAR', _('Car')
    MOTORCYCLE = 'MOTORCYCLE', _('Motorcycle')
    TRUCK = 'TRUCK', _('Truck')
    VAN = 'VAN', _('Van')
    BUS = 'BUS', _('Bus')
    BICYCLE = 'BICYCLE', _('Bicycle')
    OTHER = 'OTHER', _('Other')


class VehicleCondition(models.TextChoices):
    """Vehicle condition choices"""
    NEW = 'NEW', _('New')
    USED_LIKE_NEW = 'USED_LIKE_NEW', _('Used - Like New')
    USED_GOOD = 'USED_GOOD', _('Used - Good')
    USED_FAIR = 'USED_FAIR', _('Used - Fair')
    NEEDS_REPAIR = 'NEEDS_REPAIR', _('Needs Repair')


class TransmissionType(models.TextChoices):
    """Transmission type choices"""
    AUTOMATIC = 'AUTOMATIC', _('Automatic')
    MANUAL = 'MANUAL', _('Manual')


class FuelType(models.TextChoices):
    """Fuel type choices"""
    PETROL = 'PETROL', _('Petrol')
    DIESEL = 'DIESEL', _('Diesel')
    ELECTRIC = 'ELECTRIC', _('Electric')
    HYBRID = 'HYBRID', _('Hybrid')
    CNG = 'CNG', _('CNG')


class VehiclePurpose(models.TextChoices):
    """Vehicle purpose choices"""
    SALE = 'SALE', _('For Sale')
    RENT = 'RENT', _('For Rent')


class Vehicle(BaseClassified):
    """Vehicle listings with enhanced features"""
    
    # Vehicle Details
    type = models.CharField(max_length=20, choices=VehicleType.choices)
    make = models.CharField(max_length=100)  # Toyota, Nissan, etc.
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=50, blank=True)
    mileage = models.PositiveIntegerField(null=True, blank=True)  # in KM
    condition = models.CharField(max_length=20, choices=VehicleCondition.choices)
    transmission = models.CharField(max_length=20, choices=TransmissionType.choices)
    fuel_type = models.CharField(max_length=20, choices=FuelType.choices)
    
    # Specifications
    engine_capacity = models.CharField(max_length=20, blank=True)  # "2.0L"
    seats = models.PositiveIntegerField(null=True, blank=True)
    doors = models.PositiveIntegerField(null=True, blank=True)
    
    # Documents
    registration_no = models.CharField(max_length=100, blank=True)
    chassis_no = models.CharField(max_length=100, blank=True)
    insurance = models.BooleanField(default=False)
    insurance_expiry = models.DateTimeField(null=True, blank=True)
    
    # Purpose & Price
    purpose = models.CharField(max_length=20, choices=VehiclePurpose.choices)
    
    # Rental (if applicable)
    rent_per_day = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rent_per_month = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Media (stored as JSON array)
    images = models.JSONField(default=list, blank=True)
    
    # Sold flag
    sold = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.year} {self.make} {self.model}"
    
    class Meta(BaseClassified.Meta):
        indexes = BaseClassified.Meta.indexes + [
            models.Index(fields=['type']),
            models.Index(fields=['purpose']),
            models.Index(fields=['year']),
        ]


# ==========================================
# SERVICE MODELS
# ==========================================

class Service(BaseClassified):
    """Service listings"""
    
    category = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100)
    availability = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.category}"


# ==========================================
# SERVICE PROVIDER MODELS
# ==========================================

class ServiceCategory(models.Model):
    """Service provider categories with hierarchy"""
    
    name = models.CharField(max_length=255)
    name_bn = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=300, unique=True)
    icon = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    
    # Hierarchy
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    order = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Service Categories'
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.name


class ServiceProvider(models.Model):
    """Service provider profiles"""
    
    name = models.CharField(max_length=255)
    name_bn = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    logo = models.ImageField(upload_to='service_providers/logos/', blank=True, null=True)
    cover = models.ImageField(upload_to='service_providers/covers/', blank=True, null=True)
    description = models.TextField(blank=True)
    description_bn = models.TextField(blank=True)
    
    # Category
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, related_name='providers')
    
    # Contact
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    
    # Location
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # Business Info
    license_no = models.CharField(max_length=100, blank=True)
    cr_no = models.CharField(max_length=100, blank=True)  # Commercial Registration
    
    # Availability
    business_hours = models.JSONField(default=dict, blank=True)
    
    # Services Offered (stored as JSON array)
    services = models.JSONField(default=list, blank=True)
    
    # Media (stored as JSON arrays)
    images = models.JSONField(default=list, blank=True)
    videos = models.JSONField(default=list, blank=True)
    
    # Social
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    
    # Verification & Status
    verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ServiceProviderStatus.choices, default=ServiceProviderStatus.PENDING)
    
    # Statistics
    rating = models.FloatField(default=0.0)
    review_count = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    
    # SEO
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
            models.Index(fields=['city']),
            models.Index(fields=['verified']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.name


# ==========================================
# BOOKING SYSTEM
# ==========================================

class BookingStatus(models.TextChoices):
    """Booking status choices"""
    PENDING = 'PENDING', _('Pending')
    CONFIRMED = 'CONFIRMED', _('Confirmed')
    COMPLETED = 'COMPLETED', _('Completed')
    CANCELLED = 'CANCELLED', _('Cancelled')
    NO_SHOW = 'NO_SHOW', _('No Show')


class Booking(models.Model):
    """Service bookings"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='bookings')
    
    # Booking Details
    service_type = models.CharField(max_length=255)
    date = models.DateField()
    time = models.CharField(max_length=10, blank=True)
    notes = models.TextField(blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.PENDING)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['service_provider']),
            models.Index(fields=['status']),
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.service_provider.name} ({self.date})"


# ==========================================
# REVIEWS & RATINGS
# ==========================================

class ReviewStatus(models.TextChoices):
    """Review status choices"""
    PENDING = 'PENDING', _('Pending')
    APPROVED = 'APPROVED', _('Approved')
    REJECTED = 'REJECTED', _('Rejected')
    FLAGGED = 'FLAGGED', _('Flagged')


class Review(models.Model):
    """Reviews and ratings"""
    
    rating = models.PositiveSmallIntegerField()  # 1-5
    comment = models.TextField(blank=True)
    
    # Reviewable (Polymorphic)
    reviewable_type = models.CharField(max_length=50)  # "Company", "ServiceProvider", etc.
    reviewable_id = models.PositiveIntegerField()
    
    # Author
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    
    # Relations (optional, for specific types)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    
    # Status
    status = models.CharField(max_length=20, choices=ReviewStatus.choices, default=ReviewStatus.PENDING)
    helpful = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['reviewable_type', 'reviewable_id']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.rating} stars"


# ==========================================
# CLASSIFIED IMAGES
# ==========================================

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
