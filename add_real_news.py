import os
import django
import sys
import requests
from django.core.files.base import ContentFile
import random
from django.utils import timezone

sys.path.append('/var/www/sheba')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheba_backend.settings')
django.setup()

from news.models import Article

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        file_name = url.split('/')[-1].split('?')[0] + '.jpg'
        return ContentFile(response.content, name=file_name)
    return None

news_images = [
    'https://images.unsplash.com/photo-1585829365295-ab7cd400c167?q=80&w=800&fit=crop',
    'https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=800&fit=crop',
    'https://images.unsplash.com/photo-1523995462485-3d171b5c8fa9?q=80&w=800&fit=crop'
]

print("Updating News/Articles...")
# Create a few real news articles if they don't exist
new_articles = [
    {
        "title": "ওমানে নতুন ভিসা নিয়ম চালু",
        "title_bn": "ওমানে নতুন ভিসা নিয়ম চালু",
        "excerpt": "New visa rules implemented in Oman.",
        "excerpt_bn": "ওমানে প্রবাসীদের জন্য নতুন ভিসা নিয়ম চালু করা হয়েছে।",
        "content": "Full content...",
        "content_bn": "Full content...",
        "image_url": news_images[0]
    },
    {
        "title": "মাস্কাটে নতুন মেট্রো রেল প্রজেক্ট",
        "title_bn": "মাস্কাটে নতুন মেট্রো রেল প্রজেক্ট",
        "excerpt": "New metro rail project announced in Muscat.",
        "excerpt_bn": "মাস্কাট শহরে যাতায়াত ব্যবস্থা উন্নত করতে নতুন মেট্রো প্রজেক্টের ঘোষণা।",
        "content": "Full content...",
        "content_bn": "Full content...",
        "image_url": news_images[1]
    },
    {
        "title": "সালালাহ ট্যুরিজম ফেস্টিভ্যাল ২০২৬",
        "title_bn": "সালালাহ ট্যুরিজম ফেস্টিভ্যাল ২০২৬",
        "excerpt": "Salalah tourism festival is starting soon.",
        "excerpt_bn": "খুব শীঘ্রই শুরু হতে যাচ্ছে সালালাহ ট্যুরিজম ফেস্টিভ্যাল।",
        "content": "Full content...",
        "content_bn": "Full content...",
        "image_url": news_images[2]
    }
]

Article.objects.all().delete()
from django.contrib.auth import get_user_model
User = get_user_model()
admin_user = User.objects.filter(is_superuser=True).first()

for item in new_articles:
    a = Article(
        title=item['title'],
        title_bn=item['title_bn'],
        excerpt=item['excerpt'],
        excerpt_bn=item['excerpt_bn'],
        content=item['content'],
        content_bn=item['content_bn'],
        type='NEWS',
        status='PUBLISHED',
        author=admin_user,
        published_at=timezone.now()
    )
    img_content = download_image(item['image_url'])
    if img_content:
        a.featured_image = img_content
    a.save()

print("Done updating articles!")
