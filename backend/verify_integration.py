import sys
import os
import time

# Add desktop_app to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'desktop_app'))

from api_client import SmartGuardianAPI

def test_integration():
    print("1. Initializing API Client...")
    api = SmartGuardianAPI("http://127.0.0.1:8000/api")
    
    print("2. Testing Health Check...")
    if not api.check_health():
        print("ERROR: Backend is not reachable!")
        return False
    print("   Backend is Online ✅")
    
    print("3. Logging in as admin...")
    success, msg = api.login("admin", "admin")
    if not success:
        print(f"ERROR: Login failed - {msg}")
        return False
    print(f"   Login Successful (Token: {api.token[:10]}...) ✅")
    
    print("4. Simulating Device Sync...")
    mock_devices = [
        {
            "ip": "192.168.1.105",
            "mac": "00:11:22:33:44:55",
            "hostname": "Test-PC-Integration",
            "vendor": "Virtual Corp",
            "status": "active"
        },
        {
            "ip": "192.168.1.200",
            "mac": "AA:BB:CC:DD:EE:FF",
            "hostname": "Smart-TV-Test",
            "vendor": "Screen Co",
            "status": "active"
        }
    ]
    
    success, msg = api.sync_devices(mock_devices)
    if success:
        print(f"   Sync Successful: {msg} ✅")
    else:
        print(f"ERROR: Sync failed - {msg}")
        return False
        
    print("\n🎉 INTEGRATION TEST PASSED! The Desktop App can talk to the Backend.")
    return True

if __name__ == "__main__":
    test_integration()
