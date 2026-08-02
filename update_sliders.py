import os
import django
import sys

sys.path.append('/Users/mehedihasanmridul/Backend/ShebaWebsiteBackend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheba_backend.settings')
django.setup()

from system.models import HeroSlider

# Keep Musafir slider
musafir_sliders = HeroSlider.objects.filter(title_bn__icontains='মুসাফির')
ids_to_keep = list(musafir_sliders.values_list('id', flat=True))

if not ids_to_keep:
    # Maybe the title is in english or subtitle
    musafir_sliders = HeroSlider.objects.filter(title__icontains='musafir')
    ids_to_keep = list(musafir_sliders.values_list('id', flat=True))

if not ids_to_keep:
    print("Could not find Musafir slider, keeping all for safety.")
    ids_to_keep = list(HeroSlider.objects.all().values_list('id', flat=True))

# Delete other sliders
HeroSlider.objects.exclude(id__in=ids_to_keep).delete()

# Add relevant sliders
new_sliders = [
    {
        "title": "Trusted Service Platform",
        "title_bn": "ওমানে বাংলাদেশীদের বিশ্বস্ত সেবা প্ল্যাটফর্ম",
        "subtitle": "Jobs • Housing • Vehicles • Healthcare",
        "subtitle_bn": "চাকরি • বাসা • গাড়ি • স্বাস্থ্যসেবা — সব এক ঠিকানায়",
        "cta_text": "এক্সপ্লোর করুন",
        "link": "/",
        "is_external": False,
        "is_active": True,
        "order": 1,
        "overlay_gradient": "from-blue-950/85 via-blue-900/55 to-transparent",
    },
    {
        "title": "Find the Best Jobs in Oman",
        "title_bn": "ওমানে আপনার স্বপ্নের চাকরি খুঁজুন",
        "subtitle": "Thousands of job opportunities waiting for you",
        "subtitle_bn": "আপনার যোগ্যতা অনুযায়ী সেরা চাকরিটি বেছে নিন",
        "cta_text": "চাকরি দেখুন",
        "link": "/jobs",
        "is_external": False,
        "is_active": True,
        "order": 2,
        "overlay_gradient": "from-emerald-950/85 via-emerald-900/55 to-transparent",
    }
]

for sd in new_sliders:
    # Using default image path for now (hero fallback image on frontend)
    # The frontend falls back to /hero/slide-platform.jpg if no image
    # but the image field is required? Let's check
    pass

# Wait, image is an ImageField, might be required in model. Let's create it with an empty file or dummy if needed.
# Since image is ImageField(upload_to=...) without blank=True, null=True, it might be required.
