"""
Network Scanner Module
وحدة الفحص الحقيقي للشبكة

الوظائف:
- فحص الأجهزة المتصلة بالشبكة
- الحصول على معلومات IP
- الحصول على MAC Address
- تحديد نوع الجهاز والـ Vendor
"""

import socket
import subprocess
import platform
import re
import uuid
import requests
from datetime import datetime
import psutil
import logging
# Suppress Scapy warnings on Windows
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import scapy.all as scapy
from mac_vendor_lookup import MacLookup


class NetworkScanner:
    def __init__(self):
        self.mac_lookup = MacLookup()
        self.os_type = platform.system()
    
    def get_network_info(self):
        """الحصول على معلومات الشبكة الأساسية"""
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # Get MAC address
            mac = self.get_mac_address()
            
            # Get default gateway
            gateway = self.get_default_gateway()
            
            # Get network interfaces
            interfaces = self.get_network_interfaces()
            
            # Get connection type
            connection_type = self.detect_connection_type()
            
            return {
                'hostname': hostname,
                'local_ip': local_ip,
                'mac_address': mac,
                'gateway': gateway,
                'connection_type': connection_type,
                'interfaces': interfaces,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error getting network info: {e}")
            return {}
    
    def get_mac_address(self):
        """الحصول على MAC Address للجهاز الحالي"""
        try:
            mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
            return mac
        except:
            return "Unknown"
    
    def get_default_gateway(self):
        """الحصول على Default Gateway"""
        try:
            # Use scapy to find default gateway
            return scapy.conf.route.route("0.0.0.0")[2]
        except:
            return "Unknown"
    
    def get_network_interfaces(self):
        """الحصول على Network Interfaces"""
        try:
            interfaces = {}
            for iface_name, iface_addrs in psutil.net_if_addrs().items():
                interfaces[iface_name] = {}
                for addr in iface_addrs:
                    if addr.family == socket.AF_INET:
                        interfaces[iface_name]['ipv4'] = addr.address
                        interfaces[iface_name]['netmask'] = addr.netmask
                    elif addr.family == psutil.AF_LINK:
                        interfaces[iface_name]['mac'] = addr.address
            return interfaces
        except Exception as e:
            print(f"Error getting interfaces: {e}")
            return {}
    
    def detect_connection_type(self):
        """كشف نوع الاتصال (WiFi/Ethernet)"""
        try:
            interfaces = psutil.net_if_addrs().keys()
            
            # Check for WiFi
            wifi_keywords = ['wlan', 'wifi', 'wi-fi', 'wireless']
            for iface in interfaces:
                if any(keyword in iface.lower() for keyword in wifi_keywords):
                    return "WiFi"
            
            # Check for Ethernet
            eth_keywords = ['eth', 'ethernet', 'lan']
            for iface in interfaces:
                if any(keyword in iface.lower() for keyword in eth_keywords):
                    return "Ethernet"
            
            return "Unknown"
        except:
            return "Unknown"
    
    def get_public_ip(self):
        """الحصول على Public IP"""
        try:
            # Try multiple services for redundancy
            services = [
                "https://api.ipify.org",
                "https://ifconfig.me/ip",
                "https://icanhazip.com"
            ]
            
            for service in services:
                try:
                    response = requests.get(service, timeout=5)
                    if response.status_code == 200:
                        return response.text.strip()
                except:
                    continue
            
            return "Unable to fetch"
        except Exception as e:
            print(f"Error getting public IP: {e}")
            return "Error"
    
    def scan_network(self, network_range=None):
        """
        فحص الأجهزة المتصلة بالشبكة
        استخدام ARP scan للحصول على قائمة بالأجهزة
        """
        try:
            # If no network range specified, use current network
            if not network_range:
                local_ip = socket.gethostbyname(socket.gethostname())
                network_range = '.'.join(local_ip.split('.')[:3]) + '.0/24'
            
            print(f"Scanning network: {network_range}")
            
            # Create ARP request
            arp_request = scapy.ARP(pdst=network_range)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast/arp_request
            
            # Send and receive packets
            answered_list = scapy.srp(arp_request_broadcast, timeout=3, verbose=False)[0]
            
            devices = []
            for element in answered_list:
                device = {
                    'ip': element[1].psrc,
                    'mac': element[1].hwsrc,
                    'hostname': self.get_hostname(element[1].psrc),
                    'vendor': self.get_vendor(element[1].hwsrc),
                    'status': 'Active',
                    'first_seen': datetime.now().isoformat(),
                    'last_seen': datetime.now().isoformat()
                }
                devices.append(device)
            
            print(f"Found {len(devices)} devices")
            return devices
        
        except Exception as e:
            print(f"Error scanning network: {e}")
            # Fallback to ping sweep if scapy fails
            return self.ping_sweep(network_range)
    
    def ping_sweep(self, network_range):
        """
        Fallback method: فحص الشبكة باستخدام Ping
        """
        try:
            devices = []
            network_prefix = '.'.join(network_range.split('.')[:3])
            
            print(f"Performing ping sweep on {network_prefix}.0/24")
            
            for i in range(1, 255):
                ip = f"{network_prefix}.{i}"
                
                # Ping command based on OS
                if self.os_type == "Windows":
                    command = ["ping", "-n", "1", "-w", "100", ip]
                else:
                    command = ["ping", "-c", "1", "-W", "1", ip]
                
                try:
                    output = subprocess.run(command, 
                                          stdout=subprocess.PIPE, 
                                          stderr=subprocess.PIPE,
                                          timeout=2)
                    
                    if output.returncode == 0:
                        device = {
                            'ip': ip,
                            'mac': self.get_mac_from_arp(ip),
                            'hostname': self.get_hostname(ip),
                            'vendor': 'Unknown',
                            'status': 'Active',
                            'first_seen': datetime.now().isoformat(),
                            'last_seen': datetime.now().isoformat()
                        }
                        
                        if device['mac'] != 'Unknown':
                            device['vendor'] = self.get_vendor(device['mac'])
                            devices.append(device)
                            print(f"Found real device: {ip} [{device['mac']}]")
                        else:
                            # Skip ghost IPs that don't have a MAC address
                            continue
                except:
                    continue
            
            return devices
        except Exception as e:
            print(f"Error in ping sweep: {e}")
            return []
    
    def get_hostname(self, ip):
        """الحصول على Hostname من IP"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return "Unknown"
    
    def get_vendor(self, mac):
        """الحصول على Vendor من MAC Address"""
        try:
            vendor = self.mac_lookup.lookup(mac)
            return vendor
        except:
            return "Unknown"
    
    def get_mac_from_arp(self, ip):
        """الحصول على MAC من ARP table"""
        try:
            if self.os_type == "Windows":
                command = ["arp", "-a", ip]
            else:
                command = ["arp", "-n", ip]
            
            output = subprocess.check_output(command, universal_newlines=True)
            
            # Extract MAC address from output
            mac_pattern = r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})'
            match = re.search(mac_pattern, output)
            
            if match:
                return match.group(0)
            
            return "Unknown"
        except:
            return "Unknown"
    
    def get_device_details(self, ip):
        """الحصول على تفاصيل جهاز معين"""
        try:
            device = {
                'ip': ip,
                'hostname': self.get_hostname(ip),
                'mac': self.get_mac_from_arp(ip),
                'is_reachable': self.ping_host(ip),
                'open_ports': []  # Can be extended with port scanning
            }
            
            if device['mac'] != 'Unknown':
                device['vendor'] = self.get_vendor(device['mac'])
            else:
                device['vendor'] = 'Unknown'
            
            return device
        except Exception as e:
            print(f"Error getting device details: {e}")
            return None
    
    def ping_host(self, ip, count=1, timeout=1):
        """فحص إذا كان الجهاز متاح عن طريق Ping"""
        try:
            if self.os_type == "Windows":
                command = ["ping", "-n", str(count), "-w", str(timeout * 1000), ip]
            else:
                command = ["ping", "-c", str(count), "-W", str(timeout), ip]
            
            output = subprocess.run(command, 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
            
            return output.returncode == 0
        except:
            return False
    
    def get_network_speed(self, interface=None):
        """الحصول على سرعة الشبكة"""
        try:
            # This is a placeholder - actual implementation would use psutil
            # or platform-specific commands
            return {
                'download_speed': '0 Mbps',
                'upload_speed': '0 Mbps',
                'link_speed': '1000 Mbps'
            }
        except:
            return {}
    
    def trace_route(self, target):
        """تتبع المسار إلى هدف معين"""
        try:
            if self.os_type == "Windows":
                command = ["tracert", target]
            else:
                command = ["traceroute", target]
            
            output = subprocess.check_output(command, 
                                            universal_newlines=True, 
                                            timeout=30)
            return output
        except Exception as e:
            return f"Traceroute failed: {str(e)}"


# Test the module
if __name__ == "__main__":
    scanner = NetworkScanner()
    
    print("Getting network info...")
    info = scanner.get_network_info()
    print(json.dumps(info, indent=2))
    
    print("\nScanning network...")
    devices = scanner.scan_network()
    print(f"Found {len(devices)} devices")
    for device in devices:
        print(f"  - {device['ip']} ({device['hostname']}) - {device['vendor']}")
