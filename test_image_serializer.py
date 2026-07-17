import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheba_backend.settings')
django.setup()

from classifieds.models import Job, ClassifiedImage
from classifieds.serializers import JobSerializer

job = Job.objects.first()
if job:
    print(f"Job: {job.title}")
    images = ClassifiedImage.objects.filter(content_type='job', content_id=job.id)
    print(f"Found images: {images}")
    serializer = JobSerializer(job)
    print(f"Serialized images field: {serializer.data.get('images')}")
else:
    print("No jobs found")
