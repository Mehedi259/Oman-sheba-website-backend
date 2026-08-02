import os
import django
import sys
import requests
from django.core.files.base import ContentFile
import random

sys.path.append('/var/www/sheba')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheba_backend.settings')
django.setup()

from community.models import Classified, ClassifiedCategory
from django.contrib.auth import get_user_model

User = get_user_model()
admin_user = User.objects.filter(is_superuser=True).first()

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        file_name = url.split('/')[-1].split('?')[0] + '.jpg'
        return ContentFile(response.content, name=file_name)
    return None

print("Updating Classifieds...")
Classified.objects.all().delete()
cat_electronics, _ = ClassifiedCategory.objects.get_or_create(name='Electronics', defaults={'name_bn': 'ইলেকট্রনিক্স', 'slug': 'electronics'})

new_items = [
    {
        "title": "iPhone 13 Pro Max",
        "title_bn": "আইফোন ১৩ প্রো ম্যাক্স",
        "description": "Used iPhone 13 Pro Max 256GB in pristine condition.",
        "description_bn": "আইফোন ১৩ প্রো ম্যাক্স 256GB খুব ভালো কন্ডিশনে আছে।",
        "price": 350,
        "category": cat_electronics,
        "image_url": "https://images.unsplash.com/photo-1632661674596-df8be070a5c5?q=80&w=800&fit=crop"
    },
    {
        "title": "MacBook Pro M1",
        "title_bn": "ম্যাকবুক প্রো এম১",
        "description": "Apple MacBook Pro M1 16GB RAM.",
        "description_bn": "অ্যাপল ম্যাকবুক প্রো এম১ 16GB র‍্যাম। ফ্রেশ কন্ডিশন।",
        "price": 500,
        "category": cat_electronics,
        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?q=80&w=800&fit=crop"
    },
    {
        "title": "Sony PlayStation 5",
        "title_bn": "সনি প্লেস্টেশন ৫",
        "description": "Sony PS5 with 2 controllers.",
        "description_bn": "সনি পিএস৫ সাথে দুইটি কন্ট্রোলার।",
        "price": 200,
        "category": cat_electronics,
        "image_url": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?q=80&w=800&fit=crop"
    },
    {
        "title": "Samsung Galaxy S22 Ultra",
        "title_bn": "স্যামসাং গ্যালাক্সি এস২২ আল্ট্রা",
        "description": "Like new condition.",
        "description_bn": "একদম নতুনের মতো।",
        "price": 300,
        "category": cat_electronics,
        "image_url": "https://images.unsplash.com/photo-1644365851410-61b8f05e4685?q=80&w=800&fit=crop"
    }
]

for item in new_items:
    c = Classified(
        owner=admin_user,
        title=item['title'],
        title_bn=item['title_bn'],
        description=item['description'],
        description_bn=item['description_bn'],
        price=item['price'],
        currency='OMR',
        category=item['category']
    )
    c.status = 'PUBLISHED'
    c.images = [item['image_url']]
    c.save()

print("Done! Realistic classifieds data added.")
