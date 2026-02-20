from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import SecurityAlert
from .serializers import SecurityAlertSerializer

class SecurityAlertViewSet(viewsets.ModelViewSet):
    queryset = SecurityAlert.objects.all()
    serializer_class = SecurityAlertSerializer
    # permission_classes = [IsAuthenticated]  # Commented for testing
    filterset_fields = ['severity', 'resolved', 'alert_type']
