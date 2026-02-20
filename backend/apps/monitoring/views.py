from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import NetworkStat
from django.utils import timezone
import random
from datetime import timedelta

class MonitoringViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]  # Commented for testing

    @action(detail=False, methods=['get'])
    def network_activity(self, request):
        """
        Returns network activity from NetworkStat model.
        """
        # Get stats for last 24 hours
        last_24h = timezone.now() - timedelta(hours=24)
        stats = NetworkStat.objects.filter(timestamp__gte=last_24h).order_by('timestamp')
        
        # If no real data, fallback to a single point or empty
        if not stats.exists():
            # Return empty or minimal data to prevent UI crash
            return Response([])

        # Downsample if too many points (e.g. take one per hour)
        # For now, just return all or map nicely
        data = []
        for stat in stats:
            # Format time as HH:MM
            time_str = stat.timestamp.strftime('%H:%M')
            data.append({
                'time': time_str,
                'devices': stat.active_devices
            })
            
        return Response(data)

    @action(detail=False, methods=['get'])
    def security_score(self, request):
        """
        Calculates security score based on unresolved alerts.
        """
        # logic: Start with 100. Deduct points for unresolved alerts.
        # Critical: -15, High: -10, Medium: -5, Low: -1
        
        from apps.alerts.models import SecurityAlert
        
        alerts = SecurityAlert.objects.filter(resolved=False)
        deduction = 0
        
        for alert in alerts:
            severity = alert.severity.lower()
            if severity == 'critical': deduction += 15
            elif severity == 'high': deduction += 10
            elif severity == 'medium': deduction += 5
            elif severity == 'low': deduction += 1
            
        score = max(0, 100 - deduction)
        
        # For the trend graph, we might not have historical scores stored.
        # We can return the current score as the latest point, 
        # and maybe simulate previous points if strictly needed, 
        # or just return the single current point.
        # UI expects specific format? Let's check frontend. 
        # Frontend: data={securityScoreChartData} -> [{ name: 'Score', value: currentScore, ... }]
        # Wait, getSecurityScore in frontend returns an array for trend?
        # In Security.jsx: scoreData[scoreData.length - 1].score
        
        # Let's return a simple trend simulating stability if no history
        data = [
            {'date': 'Now', 'score': score}
        ]
        
        return Response(data)

    @action(detail=False, methods=['get'])
    def device_distribution(self, request):
        """
        Returns real device type distribution.
        """
        from apps.devices.models import Device
        from django.db.models import Count
        
        # Group by device_type
        # If device_type is null/empty, categorize as 'Unknown'
        
        # Since 'device_type' is a char field
        distribution = Device.objects.values('device_type').annotate(count=Count('id'))
        
        data = []
        colors = ['#00d4ff', '#7c4dff', '#00e676', '#ffa726', '#ff4081', '#536dfe']
        
        for idx, item in enumerate(distribution):
            dtype = item['device_type'] or 'Unknown'
            count = item['count']
            
            data.append({
                'name': dtype,
                'value': count,
                'color': colors[idx % len(colors)]
            })
            
        if not data:
            data = [{'name': 'No Devices', 'value': 0, 'color': '#cccccc'}]
            
        return Response(data)
