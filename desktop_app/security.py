"""
Security Analyzer Module
وحدة التحليل الأمني للشبكة

الوظائف:
- كشف التهديدات الأمنية
- فحص المنافذ المفتوحة
- كشف ARP Spoofing
- تحليل حركة المرور المشبوهة
- تقييم الأمان الشامل
"""

import socket
import subprocess
import platform
import re
from datetime import datetime
import hashlib


class SecurityAnalyzer:
    def __init__(self):
        self.os_type = platform.system()
        self.security_rules = self.load_security_rules()
        self.threat_database = {}
    
    def load_security_rules(self):
        """تحميل قواعد الأمان"""
        return {
            'dangerous_ports': [23, 135, 139, 445, 1433, 3389, 5900],
            'safe_ports': [80, 443, 22, 21],
            'max_open_ports': 10,
            'suspicious_patterns': [
                'rapid_connection_attempts',
                'port_scanning',
                'arp_poisoning',
                'dns_spoofing'
            ]
        }
    
    def quick_security_check(self):
        """فحص أمني سريع"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'status': 'Safe',
            'score': 100,
            'alerts': [],
            'warnings': [],
            'recommendations': []
        }
        
        # Check 1: Open Ports
        open_ports = self.check_common_ports()
        if open_ports['dangerous']:
            results['alerts'].append(
                f"⚠️ Dangerous ports open: {', '.join(map(str, open_ports['dangerous']))}"
            )
            results['score'] -= 20
            results['status'] = 'At Risk'
        
        if len(open_ports['all']) > self.security_rules['max_open_ports']:
            results['warnings'].append(
                f"⚠️ Too many open ports: {len(open_ports['all'])}"
            )
            results['score'] -= 10
        
        # Check 2: Firewall Status
        firewall_status = self.check_firewall_status()
        if not firewall_status['enabled']:
            results['alerts'].append("🔥 Firewall is disabled!")
            results['score'] -= 30
            results['status'] = 'Critical'
        
        # Check 3: Network Configuration
        network_check = self.check_network_configuration()
        if network_check['issues']:
            for issue in network_check['issues']:
                results['warnings'].append(f"⚠️ {issue}")
            results['score'] -= 5 * len(network_check['issues'])
        
        # Check 4: Known Vulnerabilities
        vuln_check = self.check_known_vulnerabilities()
        if vuln_check['found']:
            results['alerts'].append(
                f"🚨 Potential vulnerabilities detected: {len(vuln_check['vulnerabilities'])}"
            )
            results['score'] -= 15
        
        # Generate recommendations
        if results['score'] < 100:
            results['recommendations'] = self.generate_recommendations(results)
        
        # Final status based on score
        if results['score'] >= 80:
            results['status'] = 'Safe'
        elif results['score'] >= 60:
            results['status'] = 'Warning'
        elif results['score'] >= 40:
            results['status'] = 'At Risk'
        else:
            results['status'] = 'Critical'
        
        return results
    
    def check_common_ports(self, target='localhost'):
        """فحص المنافذ الشائعة"""
        try:
            all_ports = []
            dangerous_ports = []
            
            # Common ports to check
            ports_to_check = [
                20, 21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 
                443, 445, 993, 995, 1433, 3306, 3389, 5432, 5900, 
                8080, 8443
            ]
            
            for port in ports_to_check:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((target, port))
                
                if result == 0:
                    all_ports.append(port)
                    if port in self.security_rules['dangerous_ports']:
                        dangerous_ports.append(port)
                
                sock.close()
            
            return {
                'all': all_ports,
                'dangerous': dangerous_ports,
                'count': len(all_ports)
            }
        except Exception as e:
            print(f"Error checking ports: {e}")
            return {'all': [], 'dangerous': [], 'count': 0}
    
    def scan_port_range(self, target, start_port, end_port):
        """فحص نطاق من المنافذ"""
        open_ports = []
        
        try:
            for port in range(start_port, end_port + 1):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.3)
                result = sock.connect_ex((target, port))
                
                if result == 0:
                    service = self.identify_service(port)
                    open_ports.append({
                        'port': port,
                        'service': service,
                        'state': 'open'
                    })
                
                sock.close()
            
            return open_ports
        except Exception as e:
            print(f"Error scanning port range: {e}")
            return []
    
    def identify_service(self, port):
        """تحديد الخدمة التي تعمل على منفذ معين"""
        common_services = {
            20: 'FTP-Data',
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            135: 'RPC',
            139: 'NetBIOS',
            143: 'IMAP',
            443: 'HTTPS',
            445: 'SMB',
            993: 'IMAPS',
            995: 'POP3S',
            1433: 'MSSQL',
            3306: 'MySQL',
            3389: 'RDP',
            5432: 'PostgreSQL',
            5900: 'VNC',
            8080: 'HTTP-Proxy',
            8443: 'HTTPS-Alt'
        }
        
        return common_services.get(port, 'Unknown')
    
    def check_firewall_status(self):
        """فحص حالة الجدار الناري"""
        try:
            if self.os_type == "Windows":
                command = ["netsh", "advfirewall", "show", "allprofiles", "state"]
                output = subprocess.check_output(command, universal_newlines=True)
                
                # Check if firewall is ON
                enabled = "ON" in output.upper()
                
                return {
                    'enabled': enabled,
                    'status': 'Active' if enabled else 'Disabled',
                    'details': output
                }
            
            elif self.os_type == "Linux":
                # Check ufw or iptables
                try:
                    command = ["ufw", "status"]
                    output = subprocess.check_output(command, universal_newlines=True)
                    enabled = "active" in output.lower()
                except:
                    # Try iptables
                    command = ["iptables", "-L"]
                    output = subprocess.check_output(command, universal_newlines=True)
                    enabled = len(output.split('\n')) > 10  # Heuristic
                
                return {
                    'enabled': enabled,
                    'status': 'Active' if enabled else 'Disabled',
                    'details': output
                }
            
            else:
                return {
                    'enabled': None,
                    'status': 'Unknown',
                    'details': 'OS not supported'
                }
        
        except Exception as e:
            print(f"Error checking firewall: {e}")
            return {
                'enabled': None,
                'status': 'Error',
                'details': str(e)
            }
    
    def check_network_configuration(self):
        """فحص تكوين الشبكة"""
        issues = []
        
        try:
            # Check for default passwords (simulated)
            # In real implementation, this would check router admin interfaces
            
            # Check DNS configuration
            dns_check = self.check_dns_security()
            if not dns_check['secure']:
                issues.extend(dns_check['issues'])
            
            # Check for IP forwarding (security risk if enabled unnecessarily)
            if self.os_type == "Linux":
                try:
                    with open('/proc/sys/net/ipv4/ip_forward', 'r') as f:
                        if f.read().strip() == '1':
                            issues.append("IP forwarding is enabled")
                except:
                    pass
            
            return {
                'issues': issues,
                'count': len(issues)
            }
        
        except Exception as e:
            print(f"Error checking network configuration: {e}")
            return {'issues': [], 'count': 0}
    
    def check_dns_security(self):
        """فحص أمان DNS"""
        try:
            # Check for DNS leak
            # In production, this would test against known DNS servers
            
            return {
                'secure': True,
                'issues': [],
                'dns_servers': []
            }
        except:
            return {
                'secure': False,
                'issues': ['Unable to verify DNS security'],
                'dns_servers': []
            }
    
    def check_known_vulnerabilities(self):
        """فحص الثغرات المعروفة"""
        vulnerabilities = []
        
        try:
            # Check OS version for known vulnerabilities
            os_info = platform.platform()
            
            # Check for outdated software (simulated)
            # In production, this would check against CVE database
            
            # Example checks
            if "Windows" in os_info:
                # Check Windows version
                if "Windows-7" in os_info or "Windows-XP" in os_info:
                    vulnerabilities.append({
                        'id': 'OS-001',
                        'severity': 'Critical',
                        'description': 'Outdated Windows version detected',
                        'recommendation': 'Upgrade to Windows 10 or later'
                    })
            
            return {
                'found': len(vulnerabilities) > 0,
                'vulnerabilities': vulnerabilities,
                'count': len(vulnerabilities)
            }
        
        except Exception as e:
            print(f"Error checking vulnerabilities: {e}")
            return {'found': False, 'vulnerabilities': [], 'count': 0}
    
    def detect_arp_spoofing(self, network_devices):
        """كشف ARP Spoofing"""
        try:
            # Check for duplicate MAC addresses with different IPs
            mac_ip_map = {}
            suspicious = []
            
            for device in network_devices:
                mac = device.get('mac')
                ip = device.get('ip')
                
                if mac and ip:
                    if mac in mac_ip_map:
                        if mac_ip_map[mac] != ip:
                            suspicious.append({
                                'type': 'ARP Spoofing',
                                'mac': mac,
                                'ips': [mac_ip_map[mac], ip],
                                'severity': 'High'
                            })
                    else:
                        mac_ip_map[mac] = ip
            
            return {
                'detected': len(suspicious) > 0,
                'incidents': suspicious,
                'count': len(suspicious)
            }
        
        except Exception as e:
            print(f"Error detecting ARP spoofing: {e}")
            return {'detected': False, 'incidents': [], 'count': 0}
    
    def analyze_traffic_pattern(self, traffic_data):
        """تحليل أنماط حركة المرور"""
        suspicious_patterns = []
        
        try:
            # Check for port scanning
            if 'connection_attempts' in traffic_data:
                if traffic_data['connection_attempts'] > 50:
                    suspicious_patterns.append({
                        'type': 'Possible Port Scan',
                        'severity': 'Medium',
                        'details': f"{traffic_data['connection_attempts']} rapid connections"
                    })
            
            # Check for DDoS patterns
            if 'request_rate' in traffic_data:
                if traffic_data['request_rate'] > 1000:
                    suspicious_patterns.append({
                        'type': 'Possible DDoS',
                        'severity': 'High',
                        'details': f"Abnormal request rate: {traffic_data['request_rate']}/sec"
                    })
            
            return {
                'suspicious': len(suspicious_patterns) > 0,
                'patterns': suspicious_patterns,
                'count': len(suspicious_patterns)
            }
        
        except Exception as e:
            print(f"Error analyzing traffic: {e}")
            return {'suspicious': False, 'patterns': [], 'count': 0}
    
    def generate_security_report(self, scan_results):
        """إنشاء تقرير أمني شامل"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {},
            'details': {},
            'recommendations': []
        }
        
        # Calculate overall security score
        total_score = 100
        
        # Deduct points based on findings
        if scan_results.get('open_ports'):
            total_score -= len(scan_results['open_ports']['dangerous']) * 5
        
        if scan_results.get('vulnerabilities'):
            total_score -= scan_results['vulnerabilities']['count'] * 10
        
        if not scan_results.get('firewall', {}).get('enabled'):
            total_score -= 30
        
        report['summary'] = {
            'security_score': max(0, total_score),
            'status': self.get_security_status(total_score),
            'critical_issues': 0,
            'warnings': 0,
            'passed_checks': 0
        }
        
        return report
    
    def get_security_status(self, score):
        """تحديد حالة الأمان بناءً على النتيجة"""
        if score >= 90:
            return 'Excellent'
        elif score >= 75:
            return 'Good'
        elif score >= 60:
            return 'Fair'
        elif score >= 40:
            return 'Poor'
        else:
            return 'Critical'
    
    def generate_recommendations(self, results):
        """إنشاء توصيات أمنية"""
        recommendations = []
        
        if results['score'] < 80:
            if any('Firewall' in alert for alert in results['alerts']):
                recommendations.append(
                    "🔥 Enable Windows Firewall or install a third-party firewall"
                )
            
            if any('ports' in alert.lower() for alert in results['alerts']):
                recommendations.append(
                    "🔒 Close unnecessary open ports and disable unused services"
                )
            
            if results['score'] < 60:
                recommendations.append(
                    "🛡️ Consider installing antivirus/anti-malware software"
                )
                recommendations.append(
                    "🔄 Keep your operating system and software up to date"
                )
            
            if results['score'] < 40:
                recommendations.append(
                    "⚠️ URGENT: Your network security is critically compromised"
                )
                recommendations.append(
                    "👨‍💻 Consider consulting with a security professional"
                )
        
        return recommendations
    
    def create_security_hash(self, data):
        """إنشاء hash للبيانات الأمنية"""
        return hashlib.sha256(str(data).encode()).hexdigest()


# Test the module
if __name__ == "__main__":
    analyzer = SecurityAnalyzer()
    
    print("Running quick security check...")
    results = analyzer.quick_security_check()
    
    print(f"\nSecurity Status: {results['status']}")
    print(f"Security Score: {results['score']}/100")
    
    if results['alerts']:
        print("\n🚨 ALERTS:")
        for alert in results['alerts']:
            print(f"  {alert}")
    
    if results['warnings']:
        print("\n⚠️ WARNINGS:")
        for warning in results['warnings']:
            print(f"  {warning}")
    
    if results['recommendations']:
        print("\n💡 RECOMMENDATIONS:")
        for rec in results['recommendations']:
            print(f"  {rec}")
