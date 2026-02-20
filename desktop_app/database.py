"""
Database Manager Module
وحدة إدارة قاعدة البيانات

الوظائف:
- حفظ معلومات الأجهزة
- تسجيل النشاطات (Logs)
- حفظ التنبيهات الأمنية
- تخزين إحصائيات الشبكة
"""

import sqlite3
import json
from datetime import datetime
import os


class DatabaseManager:
    def __init__(self, db_path='network_guardian.db'):
        """تهيئة قاعدة البيانات"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """الاتصال بقاعدة البيانات"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
            print(f"Database connected: {self.db_path}")
        except Exception as e:
            print(f"Database connection error: {e}")
    
    def create_tables(self):
        """إنشاء الجداول"""
        try:
            # Devices table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip TEXT NOT NULL,
                    mac TEXT,
                    hostname TEXT,
                    vendor TEXT,
                    status TEXT DEFAULT 'Active',
                    first_seen TIMESTAMP,
                    last_seen TIMESTAMP,
                    device_type TEXT,
                    notes TEXT,
                    is_trusted BOOLEAN DEFAULT 0,
                    UNIQUE(ip, mac)
                )
            ''')
            
            # Activity Logs table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS activity_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    source TEXT,
                    details TEXT
                )
            ''')
            
            # Security Alerts table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS security_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    alert_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    description TEXT,
                    source_ip TEXT,
                    target_ip TEXT,
                    status TEXT DEFAULT 'New',
                    resolved BOOLEAN DEFAULT 0,
                    resolved_at TIMESTAMP,
                    notes TEXT
                )
            ''')
            
            # Network Stats table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS network_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_devices INTEGER,
                    active_devices INTEGER,
                    download_speed REAL,
                    upload_speed REAL,
                    bandwidth_usage REAL,
                    packet_loss REAL,
                    latency REAL
                )
            ''')
            
            # Scan History table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS scan_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    scan_type TEXT NOT NULL,
                    duration REAL,
                    devices_found INTEGER,
                    alerts_generated INTEGER,
                    status TEXT,
                    results TEXT
                )
            ''')
            
            # Settings table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.conn.commit()
            print("Database tables created successfully")
        
        except Exception as e:
            print(f"Error creating tables: {e}")
    
    def save_device(self, device):
        """حفظ معلومات جهاز"""
        try:
            # Check if device exists
            self.cursor.execute('''
                SELECT id FROM devices WHERE ip = ? OR mac = ?
            ''', (device.get('ip'), device.get('mac')))
            
            existing = self.cursor.fetchone()
            
            if existing:
                # Update existing device
                self.cursor.execute('''
                    UPDATE devices 
                    SET hostname = ?, 
                        vendor = ?, 
                        status = ?, 
                        last_seen = ?
                    WHERE id = ?
                ''', (
                    device.get('hostname', 'Unknown'),
                    device.get('vendor', 'Unknown'),
                    device.get('status', 'Active'),
                    datetime.now().isoformat(),
                    existing[0]
                ))
            else:
                # Insert new device
                self.cursor.execute('''
                    INSERT INTO devices (ip, mac, hostname, vendor, status, first_seen, last_seen)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    device.get('ip'),
                    device.get('mac'),
                    device.get('hostname', 'Unknown'),
                    device.get('vendor', 'Unknown'),
                    device.get('status', 'Active'),
                    datetime.now().isoformat(),
                    datetime.now().isoformat()
                ))
            
            self.conn.commit()
            return True
        
        except Exception as e:
            print(f"Error saving device: {e}")
            return False
    
    def get_all_devices(self):
        """الحصول على جميع الأجهزة"""
        try:
            self.cursor.execute('''
                SELECT ip, mac, hostname, vendor, status, first_seen, last_seen, is_trusted
                FROM devices
                ORDER BY last_seen DESC
            ''')
            
            rows = self.cursor.fetchall()
            
            devices = []
            for row in rows:
                devices.append({
                    'ip': row[0],
                    'mac': row[1],
                    'hostname': row[2],
                    'vendor': row[3],
                    'status': row[4],
                    'first_seen': row[5],
                    'last_seen': row[6],
                    'is_trusted': row[7]
                })
            
            return devices
        
        except Exception as e:
            print(f"Error getting devices: {e}")
            return []
    
    def get_device(self, ip):
        """الحصول على معلومات جهاز معين"""
        try:
            self.cursor.execute('''
                SELECT * FROM devices WHERE ip = ?
            ''', (ip,))
            
            row = self.cursor.fetchone()
            
            if row:
                return {
                    'id': row[0],
                    'ip': row[1],
                    'mac': row[2],
                    'hostname': row[3],
                    'vendor': row[4],
                    'status': row[5],
                    'first_seen': row[6],
                    'last_seen': row[7],
                    'device_type': row[8],
                    'notes': row[9],
                    'is_trusted': row[10]
                }
            
            return None
        
        except Exception as e:
            print(f"Error getting device: {e}")
            return None
    
    def is_new_device(self, device):
        """التحقق من كون الجهاز جديد"""
        try:
            self.cursor.execute('''
                SELECT id FROM devices WHERE ip = ? OR mac = ?
            ''', (device.get('ip'), device.get('mac')))
            
            return self.cursor.fetchone() is None
        
        except Exception as e:
            print(f"Error checking new device: {e}")
            return False
    
    def mark_device_trusted(self, ip, trusted=True):
        """تمييز جهاز كموثوق"""
        try:
            self.cursor.execute('''
                UPDATE devices SET is_trusted = ? WHERE ip = ?
            ''', (1 if trusted else 0, ip))
            
            self.conn.commit()
            return True
        
        except Exception as e:
            print(f"Error marking device: {e}")
            return False
    
    def log_activity(self, level, message, source=None, details=None):
        """تسجيل نشاط في السجل"""
        try:
            self.cursor.execute('''
                INSERT INTO activity_logs (level, message, source, details)
                VALUES (?, ?, ?, ?)
            ''', (level, message, source, details))
            
            self.conn.commit()
            return True
        
        except Exception as e:
            print(f"Error logging activity: {e}")
            return False
    
    def get_logs(self, level=None, limit=100):
        """الحصول على السجلات"""
        try:
            if level:
                self.cursor.execute('''
                    SELECT timestamp, level, message, source, details
                    FROM activity_logs
                    WHERE level = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (level, limit))
            else:
                self.cursor.execute('''
                    SELECT timestamp, level, message, source, details
                    FROM activity_logs
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))
            
            rows = self.cursor.fetchall()
            
            logs = []
            for row in rows:
                logs.append({
                    'timestamp': row[0],
                    'level': row[1],
                    'message': row[2],
                    'source': row[3],
                    'details': row[4]
                })
            
            return logs
        
        except Exception as e:
            print(f"Error getting logs: {e}")
            return []
    
    def clear_logs(self):
        """مسح جميع السجلات"""
        try:
            self.cursor.execute('DELETE FROM activity_logs')
            self.conn.commit()
            return True
        
        except Exception as e:
            print(f"Error clearing logs: {e}")
            return False

    def clear_devices(self):
        """مسح جميع الأجهزة من قاعدة البيانات"""
        try:
            self.cursor.execute('DELETE FROM devices')
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error clearing devices: {e}")
            return False
    
    def save_security_alert(self, alert):
        """حفظ تنبيه أمني"""
        try:
            self.cursor.execute('''
                INSERT INTO security_alerts 
                (alert_type, severity, description, source_ip, target_ip)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                alert.get('type'),
                alert.get('severity'),
                alert.get('description'),
                alert.get('source_ip'),
                alert.get('target_ip')
            ))
            
            self.conn.commit()
            return True
        
        except Exception as e:
            print(f"Error saving alert: {e}")
            return False
    
    def get_security_alerts(self, status='New', limit=50):
        """الحصول على التنبيهات الأمنية"""
        try:
            if status:
                self.cursor.execute('''
                    SELECT * FROM security_alerts
                    WHERE status = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (status, limit))
            else:
                self.cursor.execute('''
                    SELECT * FROM security_alerts
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))
            
            rows = self.cursor.fetchall()
            
            alerts = []
            for row in rows:
                alerts.append({
                    'id': row[0],
                    'timestamp': row[1],
                    'alert_type': row[2],
                    'severity': row[3],
                    'description': row[4],
                    'source_ip': row[5],
                    'target_ip': row[6],
                    'status': row[7],
                    'resolved': row[8],
                    'resolved_at': row[9],
                    'notes': row[10]
                })
            
            return alerts
        
        except Exception as e:
            print(f"Error getting alerts: {e}")
            return []
    
    def resolve_alert(self, alert_id, notes=None):
        """حل تنبيه أمني"""
        try:
            self.cursor.execute('''
                UPDATE security_alerts
                SET status = 'Resolved',
                    resolved = 1,
                    resolved_at = ?,
                    notes = ?
                WHERE id = ?
            ''', (datetime.now().isoformat(), notes, alert_id))
            
            self.conn.commit()
            return True
        
        except Exception as e:
            print(f"Error resolving alert: {e}")
            return False

    def mark_alert_synced(self, alert_id):
        """تحديث حالة التنبيه إلى Synced"""
        try:
            self.cursor.execute('''
                UPDATE security_alerts
                SET status = 'Synced'
                WHERE id = ?
            ''', (alert_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error marking alert as synced: {e}")
            return False
    
    def save_network_stats(self, stats):
        """حفظ إحصائيات الشبكة"""
        try:
            self.cursor.execute('''
                INSERT INTO network_stats
                (total_devices, active_devices, download_speed, upload_speed, 
                 bandwidth_usage, packet_loss, latency)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                stats.get('total_devices', 0),
                stats.get('active_devices', 0),
                stats.get('download_speed', 0),
                stats.get('upload_speed', 0),
                stats.get('bandwidth_usage', 0),
                stats.get('packet_loss', 0),
                stats.get('latency', 0)
            ))
            
            self.conn.commit()
            return True
        
        except Exception as e:
            print(f"Error saving stats: {e}")
            return False
    
    def get_network_stats(self, hours=24):
        """الحصول على إحصائيات الشبكة"""
        try:
            self.cursor.execute('''
                SELECT * FROM network_stats
                WHERE timestamp > datetime('now', '-{} hours')
                ORDER BY timestamp DESC
            '''.format(hours))
            
            rows = self.cursor.fetchall()
            
            stats = []
            for row in rows:
                stats.append({
                    'id': row[0],
                    'timestamp': row[1],
                    'total_devices': row[2],
                    'active_devices': row[3],
                    'download_speed': row[4],
                    'upload_speed': row[5],
                    'bandwidth_usage': row[6],
                    'packet_loss': row[7],
                    'latency': row[8]
                })
            
            return stats
        
        except Exception as e:
            print(f"Error getting stats: {e}")
            return []
    
    def save_scan_history(self, scan):
        """حفظ سجل الفحص"""
        try:
            self.cursor.execute('''
                INSERT INTO scan_history
                (scan_type, duration, devices_found, alerts_generated, status, results)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                scan.get('type'),
                scan.get('duration'),
                scan.get('devices_found'),
                scan.get('alerts_generated'),
                scan.get('status'),
                json.dumps(scan.get('results', {}))
            ))
            
            self.conn.commit()
            return True
        
        except Exception as e:
            print(f"Error saving scan history: {e}")
            return False
    
    def get_scan_history(self, limit=20):
        """الحصول على سجل الفحوصات"""
        try:
            self.cursor.execute('''
                SELECT * FROM scan_history
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            rows = self.cursor.fetchall()
            
            history = []
            for row in rows:
                history.append({
                    'id': row[0],
                    'timestamp': row[1],
                    'scan_type': row[2],
                    'duration': row[3],
                    'devices_found': row[4],
                    'alerts_generated': row[5],
                    'status': row[6],
                    'results': json.loads(row[7]) if row[7] else {}
                })
            
            return history
        
        except Exception as e:
            print(f"Error getting scan history: {e}")
            return []
    
    def save_setting(self, key, value):
        """حفظ إعداد"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO settings (key, value, updated_at)
                VALUES (?, ?, ?)
            ''', (key, value, datetime.now().isoformat()))
            
            self.conn.commit()
            return True
        
        except Exception as e:
            print(f"Error saving setting: {e}")
            return False
    
    def get_setting(self, key, default=None):
        """الحصول على إعداد"""
        try:
            self.cursor.execute('''
                SELECT value FROM settings WHERE key = ?
            ''', (key,))
            
            row = self.cursor.fetchone()
            
            if row:
                return row[0]
            
            return default
        
        except Exception as e:
            print(f"Error getting setting: {e}")
            return default
    
    def get_statistics(self):
        """الحصول على إحصائيات عامة"""
        try:
            stats = {}
            
            # Total devices
            self.cursor.execute('SELECT COUNT(*) FROM devices')
            stats['total_devices'] = self.cursor.fetchone()[0]
            
            # Active devices (seen in last hour)
            self.cursor.execute('''
                SELECT COUNT(*) FROM devices 
                WHERE last_seen > datetime('now', '-1 hour')
            ''')
            stats['active_devices'] = self.cursor.fetchone()[0]
            
            # Total alerts
            self.cursor.execute('SELECT COUNT(*) FROM security_alerts')
            stats['total_alerts'] = self.cursor.fetchone()[0]
            
            # Unresolved alerts
            self.cursor.execute('''
                SELECT COUNT(*) FROM security_alerts WHERE resolved = 0
            ''')
            stats['unresolved_alerts'] = self.cursor.fetchone()[0]
            
            # Total scans
            self.cursor.execute('SELECT COUNT(*) FROM scan_history')
            stats['total_scans'] = self.cursor.fetchone()[0]
            
            return stats
        
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}
    
    def export_data(self, table_name, format='json'):
        """تصدير البيانات"""
        try:
            self.cursor.execute(f'SELECT * FROM {table_name}')
            rows = self.cursor.fetchall()
            
            # Get column names
            self.cursor.execute(f'PRAGMA table_info({table_name})')
            columns = [col[1] for col in self.cursor.fetchall()]
            
            data = []
            for row in rows:
                data.append(dict(zip(columns, row)))
            
            if format == 'json':
                return json.dumps(data, indent=2)
            else:
                return data
        
        except Exception as e:
            print(f"Error exporting data: {e}")
            return None
    
    def close(self):
        """إغلاق الاتصال بقاعدة البيانات"""
        try:
            if self.conn:
                self.conn.close()
                print("Database connection closed")
        except Exception as e:
            print(f"Error closing database: {e}")


# Test the module
if __name__ == "__main__":
    db = DatabaseManager('test_db.db')
    
    # Test device saving
    test_device = {
        'ip': '192.168.1.100',
        'mac': 'AA:BB:CC:DD:EE:FF',
        'hostname': 'Test-Device',
        'vendor': 'Apple',
        'status': 'Active'
    }
    
    db.save_device(test_device)
    
    # Get all devices
    devices = db.get_all_devices()
    print(f"Total devices: {len(devices)}")
    
    # Log activity
    db.log_activity('INFO', 'Test log message')
    
    # Get statistics
    stats = db.get_statistics()
    print(f"Statistics: {stats}")
    
    db.close()
