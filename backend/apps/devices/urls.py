"""
Devices URLs
روابط API للأجهزة
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet

router = DefaultRouter()
router.register(r'', DeviceViewSet, basename='device')

urlpatterns = [
    path('', include(router.urls)),
]

"""
Available Endpoints:
- GET    /api/devices/              # List all devices
- POST   /api/devices/              # Create device
- GET    /api/devices/{id}/         # Get device details
- PUT    /api/devices/{id}/         # Update device
- DELETE /api/devices/{id}/         # Delete device
- POST   /api/devices/sync/         # Sync from Desktop App
- POST   /api/devices/{id}/mark_trusted/  # Mark as trusted
- POST   /api/devices/{id}/block/   # Block device
- GET    /api/devices/active/       # Get active devices only
"""
