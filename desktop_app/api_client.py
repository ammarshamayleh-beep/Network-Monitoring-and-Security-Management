import requests
import json
from datetime import datetime

class SmartGuardianAPI:
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url.rstrip('/')
        self.token = None
        self.headers = {
            'Content-Type': 'application/json'
        }
        
    def login(self, username, password):
        """Login to get authentication token"""
        try:
            url = f"{self.base_url}/auth/login/"
            response = requests.post(url, json={
                'username': username,
                'password': password
            })
            
            if response.status_code == 200:
                self.token = response.json().get('token')
                self.headers['Authorization'] = f'Token {self.token}'
                return True, "Login successful"
            else:
                return False, f"Login failed: {response.text}"
                
        except Exception as e:
            return False, f"Connection error: {str(e)}"
            
    def check_health(self):
        """Check if backend is reachable"""
        try:
            url = f"{self.base_url}/health/"
            response = requests.get(url, timeout=3)
            return response.status_code == 200
        except:
            return False

    def sync_devices(self, devices):
        """
        Sync discovered devices with backend
        devices: request list of dicts with ip, mac, hostname, vendor
        """
        if not self.token:
            return False, "Not authenticated"
            
        try:
            url = f"{self.base_url}/devices/sync/"
            
            # Prepare data structure expected by backend serializer
            # Backend expects: { "devices": [...] }
            payload = {
                "devices": devices
            }
            
            response = requests.post(url, json=payload, headers=self.headers)
            
            if response.status_code == 200:
                result = response.json()
                return True, f"Synced: {result.get('created', 0)} new, {result.get('updated', 0)} updated"
            else:
                return False, f"Sync failed: {response.text}"
                
        except Exception as e:
            return False, f"Sync error: {str(e)}"

    def send_alert(self, alert_data):
        """
        Send security alert to backend
        alert_data: { title, description, severity, alert_type, device_ip }
        """
        if not self.token:
            return False, "Not authenticated"
            
        try:
            url = f"{self.base_url}/alerts/"
            response = requests.post(url, json=alert_data, headers=self.headers)
            
            if response.status_code == 201:
                return True, "Alert sent"
            else:
                return False, f"Alert failed: {response.text}"
                
        except Exception as e:
            return False, f"Alert error: {str(e)}"
