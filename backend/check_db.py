import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.devices.models import Device

print(f"Database Path: {settings.DATABASES['default']['NAME']}")
print(f"Device Count: {Device.objects.count()}")

try:
    for d in Device.objects.all():
        print(f"- {d.ip_address} ({d.mac_address})")
except Exception as e:
    print(f"Error reading devices: {e}")
