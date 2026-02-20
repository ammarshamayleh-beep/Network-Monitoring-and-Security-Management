from django.contrib import admin
from .models import SecurityAlert

@admin.register(SecurityAlert)
class SecurityAlertAdmin(admin.ModelAdmin):
    list_display = ['alert_type', 'severity', 'timestamp', 'resolved']
    list_filter = ['severity', 'resolved']
