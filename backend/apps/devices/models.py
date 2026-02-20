"""
Devices App Models
نماذج قاعدة البيانات للأجهزة
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Device(models.Model):
    """جهاز متصل بالشبكة"""
    
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Blocked', 'Blocked'),
    ]
    
    # Basic info - Mapped to 'devices' table in network_guardian.db
    # Table columns: id, ip, mac, hostname, vendor, status, first_seen, last_seen, device_type, notes, is_trusted
    
    ip_address = models.CharField(max_length=50, unique=True, db_column='ip') # Mapped to 'ip'
    mac_address = models.CharField(max_length=17, unique=True, db_column='mac') # Mapped to 'mac'
    hostname = models.CharField(max_length=255, blank=True, null=True)
    vendor = models.CharField(max_length=255, blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    is_trusted = models.BooleanField(default=0) # SQLite boolean is 0/1
    
    # Timestamps
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    
    # Extra
    device_type = models.CharField(max_length=50, blank=True, null=True) # Exists in DB
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = False # Let desktop app manage the table
        db_table = 'devices'
        ordering = ['-last_seen']
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'
    
    def __str__(self):
        return f"{self.ip_address} ({self.hostname or 'Unknown'})"
    
    @property
    def ip(self):
        return self.ip_address
        
    @property
    def mac(self):
        return self.mac_address

    def mark_seen(self):
        self.last_seen = timezone.now()
        self.status = 'Active'
        self.save(update_fields=['last_seen', 'status'])
