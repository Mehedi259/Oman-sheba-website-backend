import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheba_backend.settings')
django.setup()

from classifieds.serializers import JobSerializer, PropertySerializer, VehicleSerializer

# Test Job
job_data = {
    'title': 'Test Job',
    'title_bn': 'Test Job BN',
    'description': 'Description',
    'type': 'FULL_TIME',
    'city': 'Muscat',
    'contact_phone': '123456',
    'company_name_bn': 'Company BN',
    'company_name_en': 'Company EN',
}
s_job = JobSerializer(data=job_data)
s_job.is_valid()
print("Job Errors:", s_job.errors)

# Test Property
prop_data = {
    'title': 'Test Prop',
    'description': 'Desc',
    'city': 'Muscat',
    'contact_phone': '123',
    'property_type': 'APARTMENT',
    'purpose': 'RENT',
    'price': 500,
}
s_prop = PropertySerializer(data=prop_data)
s_prop.is_valid()
print("Property Errors:", s_prop.errors)

# Test Vehicle
veh_data = {
    'title': 'Test Veh',
    'description': 'Desc',
    'city': 'Muscat',
    'contact_phone': '123',
    'vehicle_type': 'CAR',
    'brand': 'Toyota',
    'model': 'Camry',
    'year': 2020,
    'condition': 'NEW',
    'fuel_type': 'PETROL',
    'transmission': 'AUTOMATIC',
    'price': 5000,
}
s_veh = VehicleSerializer(data=veh_data)
s_veh.is_valid()
print("Vehicle Errors:", s_veh.errors)
