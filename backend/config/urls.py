from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'ok', 'message': 'Backend is running'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', obtain_auth_token),
    path('api/health/', health_check),
    path('api/devices/', include('apps.devices.urls')),
    path('api/alerts/', include('apps.alerts.urls')),
    path('api/monitoring/', include('apps.monitoring.urls')),
    path('api/users/', include('apps.users.urls')),
]

admin.site.site_header = "Smart Network Guardian"
admin.site.site_title = "Network Guardian"
