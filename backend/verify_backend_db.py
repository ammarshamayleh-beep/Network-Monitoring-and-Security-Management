import os
import sys
import django
from pathlib import Path

# Add backend dir to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from apps.devices.models import Device

print(f"DEBUG: settings.DATABASES['default']['NAME'] = {settings.DATABASES['default']['NAME']}")

try:
    count = Device.objects.count()
    print(f"DEBUG: Total Devices in DB: {count}")
    for d in Device.objects.all():
        print(f" - {d.ip_address} | {d.mac_address}")
except Exception as e:
    print(f"ERROR: {e}")
