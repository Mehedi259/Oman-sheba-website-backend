import os
import django
import sys
import requests
from django.core.files.base import ContentFile
import random

sys.path.append('/var/www/sheba')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheba_backend.settings')
django.setup()

from system.models import HeroSlider
from classifieds.models import Property, Vehicle, Service
from classifieds.models import PropertyType, PropertyCategory, PropertyPurpose
from classifieds.models import VehicleType, VehicleCondition, TransmissionType, VehiclePurpose
from django.contrib.auth import get_user_model

User = get_user_model()
admin_user = User.objects.filter(is_superuser=True).first()
if not admin_user:
    print("No admin user found. Creating one...")
    admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password')

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        file_name = url.split('/')[-1].split('?')[0] + '.jpg'
        return ContentFile(response.content, name=file_name)
    return None

# --- 1. SLIDERS ---
print("Updating Sliders...")
new_sliders = [
    {
        "title": "Oman's Best Platform for Bangladeshis",
        "title_bn": "ওমানে বাংলাদেশীদের সেরা প্ল্যাটফর্ম",
        "subtitle": "Everything you need in one place",
        "subtitle_bn": "আপনার প্রয়োজনীয় সবকিছু এক ঠিকানায়",
        "cta_text": "বিস্তারিত দেখুন",
        "link": "/",
        "image_url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=1200&h=400&fit=crop"
    },
    {
        "title": "Find your dream home",
        "title_bn": "ওমানে আপনার স্বপ্নের বাসা খুঁজুন",
        "subtitle": "Thousands of properties for rent and sale",
        "subtitle_bn": "ভাড়া এবং বিক্রয়ের জন্য হাজারো প্রপার্টি",
        "cta_text": "বাসা দেখুন",
        "link": "/properties",
        "image_url": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?q=80&w=1200&h=400&fit=crop"
    },
    {
        "title": "Buy and Sell Cars Easily",
        "title_bn": "গাড়ি কেনা-বেচা এখন আরো সহজ",
        "subtitle": "Get the best deals on new and used cars",
        "subtitle_bn": "নতুন এবং ব্যবহৃত গাড়ির সেরা ডিলগুলো লুফে নিন",
        "cta_text": "গাড়ি দেখুন",
        "link": "/vehicles",
        "image_url": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?q=80&w=1200&h=400&fit=crop"
    }
]

for s in new_sliders:
    slider = HeroSlider(
        title=s['title'],
        title_bn=s['title_bn'],
        subtitle=s['subtitle'],
        subtitle_bn=s['subtitle_bn'],
        cta_text=s['cta_text'],
        link=s['link'],
        is_active=True,
        order=HeroSlider.objects.count() + 1
    )
    img_content = download_image(s['image_url'])
    if img_content:
        slider.image.save(f"slider_{random.randint(1000,9999)}.jpg", img_content)
    slider.save()

# --- 2. PROPERTIES ---
print("Updating Properties...")
Property.objects.all().delete()

new_properties = [
    {
        "title": "Modern Apartment in Muscat",
        "title_bn": "মাস্কাটে আধুনিক অ্যাপার্টমেন্ট",
        "description": "A beautiful and spacious modern apartment in the heart of Muscat.",
        "description_bn": "মাস্কাটের কেন্দ্রস্থলে একটি সুন্দর এবং প্রশস্ত আধুনিক অ্যাপার্টমেন্ট। সম্পূর্ণ ফার্নিশড।",
        "price": 250,
        "purpose": "RENT",
        "type": "RESIDENTIAL",
        "category": "APARTMENT",
        "city": "Muscat",
        "area": "Ruwi",
        "image_url": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?q=80&w=800&fit=crop"
    },
    {
        "title": "Luxury Villa in Salalah",
        "title_bn": "সালালাহতে লাক্সারি ভিলা",
        "description": "A beautiful and spacious modern villa.",
        "description_bn": "সালালাহতে একটি সুন্দর এবং প্রশস্ত আধুনিক ভিলা। সম্পূর্ণ ফার্নিশড।",
        "price": 120000,
        "purpose": "SALE",
        "type": "RESIDENTIAL",
        "category": "VILLA",
        "city": "Salalah",
        "area": "Al Hafa",
        "image_url": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?q=80&w=800&fit=crop"
    },
    {
        "title": "Affordable Bed Space",
        "title_bn": "বড় বেড স্পেস ভাড়া",
        "description": "Affordable bed space for bachelors.",
        "description_bn": "ব্যাচেলরদের জন্য সাশ্রয়ী মূল্যে বেড স্পেস ভাড়া দেওয়া হবে।",
        "price": 30,
        "purpose": "RENT",
        "type": "RESIDENTIAL",
        "category": "BED_SPACE",
        "city": "Muscat",
        "area": "Seeb",
        "image_url": "https://images.unsplash.com/photo-1502672260266-1c1de2d96645?q=80&w=800&fit=crop"
    },
    {
        "title": "Family House",
        "title_bn": "ফ্যামিলি বাসা ভাড়া",
        "description": "Nice family house with great environment.",
        "description_bn": "সুন্দর পরিবেশের একটি চমৎকার ফ্যামিলি বাসা ভাড়া দেওয়া হবে।",
        "price": 180,
        "purpose": "RENT",
        "type": "RESIDENTIAL",
        "category": "HOUSE",
        "city": "Sohar",
        "area": "Falaj Al Qabail",
        "image_url": "https://images.unsplash.com/photo-1484154218962-a197022b5858?q=80&w=800&fit=crop"
    }
]

for p in new_properties:
    prop = Property(
        user=admin_user,
        title=p['title'],
        title_bn=p['title_bn'],
        description=p['description'],
        description_bn=p['description_bn'],
        price=p['price'],
        currency='OMR',
        purpose=p['purpose'],
        type=p['type'],
        category=p['category'],
        city=p['city'],
        area=p['area'],
        images=[p['image_url']]
    )
    prop.status = 'PUBLISHED' # Status from BaseClassified
    prop.save()

# --- 3. VEHICLES ---
print("Updating Vehicles...")
Vehicle.objects.all().delete()

new_vehicles = [
    {
        "title": "Toyota Camry 2020",
        "title_bn": "টয়োটা ক্যামরি ২০২০",
        "description": "Excellent condition Toyota Camry. Low mileage.",
        "description_bn": "চমৎকার কন্ডিশনের টয়োটা ক্যামরি ২০২০। খুব কম মাইলেজ।",
        "price": 4500,
        "type": "CAR",
        "make": "Toyota",
        "model": "Camry",
        "year": 2020,
        "mileage": 45000,
        "condition": "USED_GOOD",
        "city": "Muscat",
        "image_url": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?q=80&w=800&fit=crop"
    },
    {
        "title": "Nissan Patrol SUV",
        "title_bn": "নিসান প্যাট্রোল এসইউভি",
        "description": "Great SUV for family trips.",
        "description_bn": "পারিবারিক ভ্রমণের জন্য দারুণ একটি এসইউভি গাড়ি।",
        "price": 8500,
        "type": "CAR",
        "make": "Nissan",
        "model": "Patrol",
        "year": 2018,
        "mileage": 80000,
        "condition": "USED_GOOD",
        "city": "Salalah",
        "image_url": "https://images.unsplash.com/photo-1609521263047-f8f205293f24?q=80&w=800&fit=crop"
    },
    {
        "title": "Hyundai Elantra 2019",
        "title_bn": "হুন্ডাই এলান্ট্রা ২০১৯",
        "description": "Perfect condition.",
        "description_bn": "খুবই ভালো কন্ডিশনের হুন্ডাই এলান্ট্রা, এক হাতে চালানো।",
        "price": 3200,
        "type": "CAR",
        "make": "Hyundai",
        "model": "Elantra",
        "year": 2019,
        "mileage": 65000,
        "condition": "USED_GOOD",
        "city": "Muscat",
        "image_url": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?q=80&w=800&fit=crop"
    },
    {
        "title": "Honda Civic 2021",
        "title_bn": "হোন্ডা সিভিক ২০২১",
        "description": "Sporty look.",
        "description_bn": "স্পোর্টি লুকের সুন্দর একটি গাড়ি, খুব যত্ন করে চালানো।",
        "price": 5500,
        "type": "CAR",
        "make": "Honda",
        "model": "Civic",
        "year": 2021,
        "mileage": 30000,
        "condition": "USED_LIKE_NEW",
        "city": "Sohar",
        "image_url": "https://images.unsplash.com/photo-1580273916550-e323be2ae537?q=80&w=800&fit=crop"
    }
]

for v in new_vehicles:
    veh = Vehicle(
        user=admin_user,
        title=v['title'],
        title_bn=v['title_bn'],
        description=v['description'],
        description_bn=v['description_bn'],
        price=v['price'],
        currency='OMR',
        type=v['type'],
        make=v['make'],
        model=v['model'],
        year=v['year'],
        mileage=v['mileage'],
        condition=v['condition'],
        city=v['city'],
        images=[v['image_url']]
    )
    veh.status = 'PUBLISHED'
    veh.save()

# --- 4. SERVICES ---
print("Updating Services...")
Service.objects.all().delete()

new_services = [
    {
        "title": "Professional AC Repair",
        "title_bn": "এসি মেরামত ও সার্ভিসিং",
        "description": "Best AC repair services in Muscat.",
        "description_bn": "মাস্কাটের সেরা এসি রিপেয়ার সার্ভিস।",
        "price": 10,
        "category": "Repair",
        "service_type": "AC Repair",
        "city": "Muscat",
        "image_url": "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?q=80&w=800&fit=crop"
    },
    {
        "title": "Home Cleaning Service",
        "title_bn": "বাসা পরিষ্কার সার্ভিস",
        "description": "Deep cleaning for your home.",
        "description_bn": "আপনার বাসার ডিপ ক্লিনিং সার্ভিস।",
        "price": 15,
        "category": "Cleaning",
        "service_type": "Deep Cleaning",
        "city": "Salalah",
        "image_url": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?q=80&w=800&fit=crop"
    },
    {
        "title": "Expert Plumber",
        "title_bn": "দক্ষ প্লাম্বার বা স্যানিটারি কাজ",
        "description": "All kinds of plumbing work.",
        "description_bn": "যেকোনো ধরণের স্যানিটারি কাজ সুদক্ষ কারিগর দ্বারা করানো হয়।",
        "price": 8,
        "category": "Plumbing",
        "service_type": "Installation",
        "city": "Muscat",
        "image_url": "https://images.unsplash.com/photo-1621905252507-b35492cc74b4?q=80&w=800&fit=crop"
    },
    {
        "title": "Movers and Packers",
        "title_bn": "প্যাকিং ও বাসা বদল",
        "description": "Safe moving of your house items.",
        "description_bn": "আপনার বাসার আসবাবপত্র নিরাপদে স্থানান্তরের নির্ভরযোগ্য মাধ্যম।",
        "price": 35,
        "category": "Moving",
        "service_type": "Relocation",
        "city": "Sohar",
        "image_url": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=800&fit=crop"
    }
]

for s in new_services:
    srv = Service(
        user=admin_user,
        title=s['title'],
        title_bn=s['title_bn'],
        description=s['description'],
        description_bn=s['description_bn'],
        price=s['price'],
        currency='OMR',
        category=s['category'],
        service_type=s['service_type'],
        city=s['city'],
        images=[s['image_url']]
    )
    srv.status = 'PUBLISHED'
    srv.save()

print("Done! Realistic data added.")
