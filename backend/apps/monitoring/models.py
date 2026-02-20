from django.db import models

class NetworkStat(models.Model):
    # Mapped to 'network_stats' table
    # Columns: id, timestamp, total_devices, active_devices, download_speed, upload_speed, bandwidth_usage, packet_loss, latency
    
    timestamp = models.DateTimeField(auto_now_add=True)
    total_devices = models.IntegerField(default=0)
    active_devices = models.IntegerField(default=0)
    
    download_speed = models.FloatField(default=0.0)
    upload_speed = models.FloatField(default=0.0)
    bandwidth_usage = models.FloatField(default=0.0)
    packet_loss = models.FloatField(default=0.0)
    latency = models.FloatField(default=0.0)
    
    class Meta:
        managed = False
        db_table = 'network_stats'
        ordering = ['-timestamp']
