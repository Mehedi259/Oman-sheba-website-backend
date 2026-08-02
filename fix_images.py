import os
import django
import sys
import requests
from django.core.files.base import ContentFile
import random

sys.path.append('/var/www/sheba')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheba_backend.settings')
django.setup()

from classifieds.models import Property, Vehicle, Service, ClassifiedImage

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        file_name = url.split('/')[-1].split('?')[0] + '.jpg'
        return ContentFile(response.content, name=file_name)
    return None

prop_img = 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?q=80&w=800&fit=crop'
veh_img = 'https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?q=80&w=800&fit=crop'
srv_img = 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?q=80&w=800&fit=crop'

print("Fixing property images...")
for p in Property.objects.all():
    if not ClassifiedImage.objects.filter(content_type='property', content_id=p.id).exists():
        img_content = download_image(prop_img)
        if img_content:
            ClassifiedImage.objects.create(content_type='property', content_id=p.id, image=img_content, is_primary=True)

print("Fixing vehicle images...")
for v in Vehicle.objects.all():
    if not ClassifiedImage.objects.filter(content_type='vehicle', content_id=v.id).exists():
        img_content = download_image(veh_img)
        if img_content:
            ClassifiedImage.objects.create(content_type='vehicle', content_id=v.id, image=img_content, is_primary=True)

print("Fixing service images...")
for s in Service.objects.all():
    if not ClassifiedImage.objects.filter(content_type='service', content_id=s.id).exists():
        img_content = download_image(srv_img)
        if img_content:
            ClassifiedImage.objects.create(content_type='service', content_id=s.id, image=img_content, is_primary=True)

print("Done fixing images!")
