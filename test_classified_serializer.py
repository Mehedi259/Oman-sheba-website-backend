import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sheba_backend.settings")
django.setup()

from community.serializers import ClassifiedSerializer
from community.models import ClassifiedCategory
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.first()

data = {
  "title_bn": "iphone",
  "description_bn": "gfdsgdfd",
  "category": "electronics",
  "price": 2552,
  "currency": "OMR",
  "city": "Sohar",
  "area": "mascut",
  "contact_name": "Mehedi Hasan",
  "contact_phone": "01627021553",
  "status": "PUBLISHED",
  "title": "iphone",
  "description": "gfdsgdfd"
}

serializer = ClassifiedSerializer(data=data)
if serializer.is_valid():
    print("Valid!")
    serializer.save(owner=user)
else:
    print("Invalid!")
    print(serializer.errors)
