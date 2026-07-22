import os, sys, django
sys.path.append('/var/www/sheba')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheba_backend.settings')
django.setup()

from classifieds.models import Job, Property, Vehicle, Service, Company, JobCategory
from news.models import Article, ArticleCategory
from emergency.models import EmergencyService
from community.models import ForumPost, ForumCategory
from django.contrib.auth import get_user_model
User = get_user_model()
admin = User.objects.filter(is_superuser=True).first()

def add_data():
    if not admin:
        print("No admin user found.")
        return
        
    print("Creating Company and Job Category...")
    company, _ = Company.objects.get_or_create(name="Test Company")
    job_cat, _ = JobCategory.objects.get_or_create(name="Software Engineering", defaults={'slug': 'software-engineering'})
    
    print("Creating Job...")
    Job.objects.create(
        title="Test Software Engineer", 
        title_bn="সফটওয়্যার ইঞ্জিনিয়ার (টেস্ট)", 
        description="This is a test job description", 
        city="Muscat", 
        user=admin, 
        status="PUBLISHED",
        company=company,
        category=job_cat,
        type="FULL_TIME",
        experience="1-3 Years"
    )

    print("Creating Property...")
    Property.objects.create(
        title="Test Apartment", 
        title_bn="টেস্ট বাসা", 
        description="This is a test property description", 
        city="Muscat", 
        user=admin, 
        status="PUBLISHED", 
        type="RESIDENTIAL",
        category="HOUSE",
        purpose="RENT",
        price=150.00,
        bedrooms=2,
        bathrooms=1
    )

    print("Creating Vehicle...")
    Vehicle.objects.create(
        title="Test Toyota Corolla", 
        title_bn="টেস্ট টয়োটা করোলা", 
        description="This is a test vehicle description", 
        city="Muscat", 
        user=admin, 
        status="PUBLISHED", 
        type="CAR", 
        make="Toyota", 
        model="Corolla",
        year=2020,
        price=3000.00,
        condition="NEW",
        transmission="AUTOMATIC",
        fuel_type="PETROL"
    )
    
    print("Creating News...")
    news_cat, _ = ArticleCategory.objects.get_or_create(name="Local News", defaults={'slug': 'local-news', 'type': 'NEWS'})
    Article.objects.create(
        title="Test Breaking News", 
        content="This is a test news article for the community.", 
        author=admin,
        category=news_cat,
        status="PUBLISHED",
        type="NEWS"
    )

    print("Creating Services...")
    service_cats = [
        'Embassy', 'Specialist Doctor', 'Hospital', 'Ambulance', 'Lawyer', 
        'Travel Agency', 'Hotel', 'Money Exchange', 'Maktab Sanad', 
        'Tourist Place', 'Police Station', 'Medical Services'
    ]
    for cat in service_cats:
        backend_slug = cat.replace(' ', '-').lower()
        Service.objects.create(
            title=f"Test {cat}", 
            title_bn=f"টেস্ট {cat}", 
            description=f"Test description for {cat}", 
            city="Muscat", 
            user=admin, 
            status="PUBLISHED", 
            category=backend_slug,
            contact_phone="12345678",
            service_type="Test Service"
        )
    print("Done!")

if __name__ == "__main__":
    add_data()
