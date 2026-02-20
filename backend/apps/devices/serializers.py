"""
Devices Serializers
تحويل Models إلى JSON
"""
from rest_framework import serializers
from .models import Device


class DeviceSerializer(serializers.ModelSerializer):
    """Serializer للأجهزة"""
    
    class Meta:
        model = Device
        fields = [
            'id',
            'ip_address',
            'mac_address',
            'hostname',
            'vendor',
            'status',
            'is_trusted',
            'first_seen',
            'last_seen',
            'device_type',
            'notes'
        ]
        read_only_fields = ['id', 'first_seen']


class DeviceSyncSerializer(serializers.Serializer):
    """Serializer للمزامنة من Desktop App"""
    
    devices = serializers.ListField(
        child=serializers.DictField()
    )
