"""
Devices Views
API Endpoints للأجهزة
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Count, Avg
from .models import Device
from .serializers import DeviceSerializer, DeviceSyncSerializer
from apps.alerts.models import SecurityAlert


class DeviceViewSet(viewsets.ModelViewSet):
    """API للأجهزة"""
    
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    # permission_classes = [IsAuthenticated]  # Commented for testing
    
    # Search & Filter
    search_fields = ['ip_address', 'mac_address', 'hostname', 'vendor']
    filterset_fields = ['status', 'is_trusted']
    ordering_fields = ['last_seen', 'first_seen']
    
    @action(detail=False, methods=['post'])
    def sync(self, request):
        """
        مزامنة الأجهزة من Desktop App
        POST /api/devices/sync/
        """
        serializer = DeviceSyncSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        devices_data = serializer.validated_data['devices']
        
        created_count = 0
        updated_count = 0
        
        for device_data in devices_data:
            ip = device_data.get('ip')
            mac = device_data.get('mac')
            
            if not ip or not mac:
                continue
            
            # Update or create
            device, created = Device.objects.update_or_create(
                mac_address=mac,
                defaults={
                    'ip_address': ip,
                    'hostname': device_data.get('hostname', ''),
                    'vendor': device_data.get('vendor', ''),
                    'status': device_data.get('status', 'active'),
                    'last_seen': timezone.now()
                }
            )
            
            if created:
                created_count += 1
            else:
                updated_count += 1
        
        return Response({
            'success': True,
            'message': f'Synced {len(devices_data)} devices',
            'created': created_count,
            'updated': updated_count
        })
    
    @action(detail=True, methods=['post'])
    def mark_trusted(self, request, pk=None):
        """تمييز جهاز كموثوق"""
        device = self.get_object()
        device.is_trusted = True
        device.save()
        
        return Response({
            'success': True,
            'message': f'Device {device.ip_address} marked as trusted'
        })
    
    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        """حظر جهاز"""
        device = self.get_object()
        device.status = 'blocked'
        device.save()
        
        return Response({
            'success': True,
            'message': f'Device {device.ip_address} blocked'
        })
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """الحصول على الأجهزة النشطة فقط (Case-insensitive)"""
        active_devices = Device.objects.filter(status__in=['active', 'Active'])
        serializer = self.get_serializer(active_devices, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """إحصائيات الأجهزة والشبكة"""
        # Calculate real security score
        alerts = SecurityAlert.objects.filter(resolved=False)
        deduction = 0
        for alert in alerts:
            severity = alert.severity.lower()
            if severity == 'critical': deduction += 15
            elif severity == 'high': deduction += 10
            elif severity == 'medium': deduction += 5
            elif severity == 'low': deduction += 1
            
        security_score = max(0, 100 - deduction)

        stats = {
            'total_devices': Device.objects.count(),
            'active_devices': Device.objects.filter(status__in=['active', 'Active']).count(),
            'total_alerts': alerts.count(),
            'average_security_score': security_score,
        }
        return Response(stats)

    @action(detail=False, methods=['post'])
    def clear_all(self, request):
        """حذف جميع الأجهزة من السيرفر"""
        Device.objects.all().delete()
        return Response({
            'success': True,
            'message': 'All devices cleared from server'
        })
