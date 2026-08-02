import os
import django
import sys
import uuid

sys.path.append('/Users/mehedihasanmridul/Backend/ShebaWebsiteBackend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheba_backend.settings')
django.setup()

from classifieds.models import Job, JobCategory, Company
from django.contrib.auth import get_user_model

User = get_user_model()
admin_user = User.objects.filter(is_superuser=True).first()
if not admin_user:
    admin_user = User.objects.first()

Job.objects.all().delete()

# Get existing categories
categories = list(JobCategory.objects.all()[:3])
if not categories:
    print("No categories found.")
    sys.exit(1)

def get_cat(idx):
    return categories[idx % len(categories)]

comp1, _ = Company.objects.get_or_create(
    name="Tech Solutions Oman",
    defaults={"name_bn": "টেক সলিউশনস ওমান", "slug": "tech-solutions-oman-" + str(uuid.uuid4())[:8]}
)
comp2, _ = Company.objects.get_or_create(
    name="Oman Builders LLC",
    defaults={"name_bn": "ওমান বিল্ডার্স এলএলসি", "slug": "oman-builders-llc-" + str(uuid.uuid4())[:8]}
)
comp3, _ = Company.objects.get_or_create(
    name="Bengal Dine",
    defaults={"name_bn": "বেঙ্গল ডাইন", "slug": "bengal-dine-" + str(uuid.uuid4())[:8]}
)
comp4, _ = Company.objects.get_or_create(
    name="Global Tech Services",
    defaults={"name_bn": "গ্লোবাল টেক সার্ভিসেস", "slug": "global-tech-services-" + str(uuid.uuid4())[:8]}
)

jobs_data = [
    {
        "title": "Senior Software Engineer",
        "title_bn": "সিনিয়র সফটওয়্যার ইঞ্জিনিয়ার",
        "description": "We are looking for an experienced developer...",
        "description_bn": "আমরা একজন অভিজ্ঞ ডেভেলপার খুঁজছি। ফাস্ট-পেসড পরিবেশে কাজ করার অভিজ্ঞতা থাকতে হবে।",
        "company": comp1,
        "category": get_cat(0),
        "city": "Muscat",
        "area": "Ruwi",
        "salary_min": 500,
        "salary_max": 800,
        "salary_currency": "OMR",
        "type": "FULL_TIME",
        "status": "PUBLISHED",
        "featured": True
    },
    {
        "title": "Civil Engineer",
        "title_bn": "সিভিল ইঞ্জিনিয়ার",
        "description": "Looking for a Civil Engineer with 5 years experience.",
        "description_bn": "৫ বছরের অভিজ্ঞতাসম্পন্ন একজন সিভিল ইঞ্জিনিয়ার প্রয়োজন। কনস্ট্রাকশন প্রজেক্ট তদারকি করতে হবে।",
        "company": comp2,
        "category": get_cat(1),
        "city": "Salalah",
        "area": "Awqad",
        "salary_min": 400,
        "salary_max": 600,
        "salary_currency": "OMR",
        "type": "FULL_TIME",
        "status": "PUBLISHED",
        "featured": False
    },
    {
        "title": "Restaurant Manager",
        "title_bn": "রেস্টুরেন্ট ম্যানেজার",
        "description": "Need an experienced restaurant manager for a busy Bangladeshi restaurant.",
        "description_bn": "ব্যস্ত একটি বাংলাদেশী রেস্টুরেন্টের জন্য অভিজ্ঞ ম্যানেজার প্রয়োজন। কাস্টমার সার্ভিস ও টিম ম্যানেজমেন্টে দক্ষ হতে হবে।",
        "company": comp3,
        "category": get_cat(2),
        "city": "Muscat",
        "area": "Muttrah",
        "salary_min": 250,
        "salary_max": 350,
        "salary_currency": "OMR",
        "type": "FULL_TIME",
        "status": "PUBLISHED",
        "featured": True
    },
    {
        "title": "IT Support Specialist",
        "title_bn": "আইটি সাপোর্ট স্পেশালিস্ট",
        "description": "IT support staff needed.",
        "description_bn": "আমাদের কর্পোরেট অফিসের জন্য আইটি সাপোর্ট স্পেশালিস্ট প্রয়োজন। হার্ডওয়্যার এবং নেটওয়ার্কিং এ জ্ঞান থাকতে হবে।",
        "company": comp4,
        "category": get_cat(0),
        "city": "Sohar",
        "area": "Sohar Industrial",
        "salary_min": 300,
        "salary_max": 450,
        "salary_currency": "OMR",
        "type": "FULL_TIME",
        "status": "PUBLISHED",
        "featured": False
    }
]

for jd in jobs_data:
    Job.objects.create(user=admin_user, **jd)

print("Added 4 realistic jobs successfully.")
