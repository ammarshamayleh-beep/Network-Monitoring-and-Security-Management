from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'mac_address', 'hostname', 'vendor', 'status', 'is_trusted', 'last_seen']
    list_filter = ['status', 'is_trusted']
    search_fields = ['ip_address', 'mac_address', 'hostname']
