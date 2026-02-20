from django.db import models
from apps.devices.models import Device

class SecurityAlert(models.Model):
    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    # Mapped to 'security_alerts' table
    # Columns: id, timestamp, alert_type, severity, description, source_ip, target_ip, status, resolved, resolved_at, notes
    
    timestamp = models.DateTimeField(auto_now_add=True)
    alert_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    description = models.TextField()
    
    source_ip = models.CharField(max_length=50, blank=True, null=True)
    target_ip = models.CharField(max_length=50, blank=True, null=True)
    
    status = models.CharField(max_length=50, default='New') # New, Resolved, Ignored
    resolved = models.BooleanField(default=False) # 0 or 1
    
    resolved_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'security_alerts'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.alert_type} - {self.severity}"
