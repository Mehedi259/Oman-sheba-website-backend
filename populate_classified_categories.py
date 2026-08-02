import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheba_backend.settings')
django.setup()

from community.models import ClassifiedCategory

categories = [
    {'name': 'Electronics', 'name_bn': 'ইলেকট্রনিক্স', 'slug': 'electronics', 'icon': 'Smartphone', 'order': 1},
    {'name': 'Computer', 'name_bn': 'কম্পিউটার', 'slug': 'computer', 'icon': 'Laptop', 'order': 2},
    {'name': 'Furniture', 'name_bn': 'ফার্নিচার', 'slug': 'furniture', 'icon': 'HomeIcon', 'order': 3},
    {'name': 'Clothing', 'name_bn': 'পোশাক', 'slug': 'clothing', 'icon': 'Shirt', 'order': 4},
    {'name': 'Baby Products', 'name_bn': 'শিশু সামগ্রী', 'slug': 'baby-products', 'icon': 'Baby', 'order': 5},
    {'name': 'Tools & Machinery', 'name_bn': 'যন্ত্রপাতি', 'slug': 'tools-machinery', 'icon': 'Wrench', 'order': 6},
    {'name': 'Books', 'name_bn': 'বই', 'slug': 'books', 'icon': 'BookOpen', 'order': 7},
    {'name': 'Others', 'name_bn': 'অন্যান্য', 'slug': 'others', 'icon': 'Heart', 'order': 8},
]

print("Populating classified categories...")
for cat_data in categories:
    cat, created = ClassifiedCategory.objects.get_or_create(
        slug=cat_data['slug'],
        defaults=cat_data
    )
    if not created:
        for k, v in cat_data.items():
            setattr(cat, k, v)
        cat.save()
        print(f"Updated category: {cat.name}")
    else:
        print(f"Created category: {cat.name}")
print("Done.")
