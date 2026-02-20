"""
Smart Network Guardian - Desktop Application
نظام متقدم لمراقبة الشبكات والأمن السيبراني

المزايا الجديدة:
- Real Network Scanning (مش simulation)
- Database Integration
- Enhanced Security Features
- API Communication مع Backend
- Real-time Monitoring
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import json
import requests
from datetime import datetime
import sqlite3
import os
import psutil
import csv
from tkinter import filedialog

# استيراد الوحدات المخصصة
from scanner import NetworkScanner
from security import SecurityAnalyzer
from database import DatabaseManager
from api_client import SmartGuardianAPI
from tkinter import simpledialog

class SmartNetworkGuardian:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Network Guardian - v2.0 Professional")
        self.root.geometry("1400x850")
        
        # Initialize components
        self.db = DatabaseManager()
        self.scanner = NetworkScanner()
        self.security = SecurityAnalyzer()
        
        # API Configuration (Django Backend)
        self.api = SmartGuardianAPI()
        self.api_connected = False
        
        # Results storage
        self.current_scan_results = {}
        self.monitoring_active = False
        
        # Setup UI
        self.center_window()
        self.setup_modern_theme()
        self.create_ui()
        
        # Start initial checks
        self.perform_startup_checks()
    
    def center_window(self):
        """توسيط النافذة على الشاشة"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_modern_theme(self):
        """إعداد الثيم الحديث"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Modern Color Palette
        self.colors = {
            'primary': '#1a1a2e',
            'secondary': '#16213e',
            'accent': '#0f3460',
            'success': '#00ff88',
            'warning': '#ffa500',
            'danger': '#ff3838',
            'info': '#00d4ff',
            'light': '#eaeaea',
            'dark': '#0a0a0a'
        }
        
        # Configure styles
        self.style.configure('.',
            background=self.colors['primary'],
            foreground=self.colors['light'],
            font=('Segoe UI', 10))
        
        self.style.configure('TFrame',
            background=self.colors['primary'])
        
        self.style.configure('Header.TLabel',
            font=('Segoe UI', 16, 'bold'),
            foreground=self.colors['success'],
            background=self.colors['primary'])
        
        self.style.configure('Title.TLabel',
            font=('Segoe UI', 12, 'bold'),
            foreground=self.colors['light'],
            background=self.colors['primary'])
        
        self.style.configure('Data.TLabel',
            font=('Consolas', 10),
            foreground=self.colors['info'],
            background=self.colors['secondary'])
        
        # Button styles
        self.style.configure('Accent.TButton',
            font=('Segoe UI', 11, 'bold'),
            background=self.colors['success'],
            foreground=self.colors['dark'],
            borderwidth=0,
            focuscolor='none',
            padding=10)
        
        self.style.map('Accent.TButton',
            background=[('active', '#00cc70'), ('pressed', '#00aa60')])
        
        # Treeview style
        self.style.configure('Treeview',
            background=self.colors['secondary'],
            foreground=self.colors['light'],
            fieldbackground=self.colors['secondary'],
            borderwidth=0,
            rowheight=28)
        
        self.style.configure('Treeview.Heading',
            background=self.colors['accent'],
            foreground=self.colors['light'],
            borderwidth=0,
            font=('Segoe UI', 10, 'bold'))
        
        self.style.map('Treeview',
            background=[('selected', self.colors['accent'])])
        
        self.root.configure(bg=self.colors['primary'])
        self.root.configure(bg=self.colors['primary'])
    
    def connect_to_backend(self):
        """الاتصال بالسيرفر"""
        # Try auto-login with default credentials first
        self.update_status("Connecting to backend...")
        success, msg = self.api.login("admin", "admin")
        
        if success:
            self._handle_login_success("admin")
            return

        # If auto-login fails, ask user
        username = simpledialog.askstring("Connect to Backend", "Username:", parent=self.root, initialvalue="admin")
        if not username: return
        
        password = simpledialog.askstring("Connect to Backend", "Password:", parent=self.root, show="*")
        if password is None: return # Cancelled
        
        success, msg = self.api.login(username, password)
        
        if success:
            self._handle_login_success(username)
        else:
            self.api_connected = False
            self.backend_status.config(text="🔴 Error", foreground=self.colors['danger'])
            self.update_status("Connection failed")
            messagebox.showerror("Connection Error", f"Failed to connect:\n{msg}")
            
    def _handle_login_success(self, username):
        self.api_connected = True
        self.backend_status.config(text="🟢 Connected", foreground=self.colors['success'])
        self.update_status(f"Connected to backend as {username}")
        # Auto sync after login
        self.sync_with_backend()

    def create_ui(self):
        """إنشاء واجهة المستخدم"""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Header
        self.create_header(main_container)
        
        # Content area (Sidebar + Main Content)
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Sidebar
        self.create_sidebar(content_frame)
        
        # Main content with tabs
        self.create_main_content(content_frame)
        
        # Status bar
        self.create_status_bar(main_container)
    
    def create_header(self, parent):
        """إنشاء الهيدر"""
        header = ttk.Frame(parent, style='TFrame')
        header.pack(fill=tk.X, pady=(0, 10))
        
        # Logo and title
        title_frame = ttk.Frame(header)
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(title_frame,
            text="🛡️ SMART NETWORK GUARDIAN",
            style='Header.TLabel').pack(side=tk.LEFT, padx=10)
        
        ttk.Label(title_frame,
            text="Professional Network Monitoring & Security System",
            style='Title.TLabel').pack(side=tk.LEFT, padx=10)
        
        # Connection status
        status_frame = ttk.Frame(header)
        status_frame.pack(side=tk.RIGHT, padx=10)
        
        ttk.Label(status_frame,
            text="Backend:",
            style='Title.TLabel').pack(side=tk.LEFT)
        
        self.backend_status = ttk.Label(status_frame,
            text="🔴 Disconnected",
            style='Data.TLabel')
        self.backend_status.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(status_frame, text="Connect", 
                   command=self.connect_to_backend,
                   style='Accent.TButton', width=10).pack(side=tk.LEFT, padx=5)
    
    
    def create_sidebar(self, parent):
        """إنشاء الشريط الجانبي"""
        sidebar = ttk.Frame(parent, width=280)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        sidebar.pack_propagate(False)
        
        # Quick Stats Panel
        stats_frame = ttk.LabelFrame(sidebar, text=" Quick Stats ", padding=10)
        stats_frame.pack(fill=tk.X, pady=5)
        
        # Public IP
        ip_frame = ttk.Frame(stats_frame)
        ip_frame.pack(fill=tk.X, pady=3)
        ttk.Label(ip_frame, text="Public IP:", style='Title.TLabel').pack(side=tk.LEFT)
        self.public_ip_label = ttk.Label(ip_frame, text="Loading...", style='Data.TLabel')
        self.public_ip_label.pack(side=tk.RIGHT)
        
        # Local IP
        local_frame = ttk.Frame(stats_frame)
        local_frame.pack(fill=tk.X, pady=3)
        ttk.Label(local_frame, text="Local IP:", style='Title.TLabel').pack(side=tk.LEFT)
        self.local_ip_label = ttk.Label(local_frame, text="Loading...", style='Data.TLabel')
        self.local_ip_label.pack(side=tk.RIGHT)
        
        # Devices Count
        devices_frame = ttk.Frame(stats_frame)
        devices_frame.pack(fill=tk.X, pady=3)
        ttk.Label(devices_frame, text="Devices:", style='Title.TLabel').pack(side=tk.LEFT)
        self.devices_count_label = ttk.Label(devices_frame, text="0", style='Data.TLabel')
        self.devices_count_label.pack(side=tk.RIGHT)
        
        # Alerts Count
        alerts_frame = ttk.Frame(stats_frame)
        alerts_frame.pack(fill=tk.X, pady=3)
        ttk.Label(alerts_frame, text="Alerts:", style='Title.TLabel').pack(side=tk.LEFT)
        self.alerts_count_label = ttk.Label(alerts_frame, text="0", style='Data.TLabel')
        self.alerts_count_label.pack(side=tk.RIGHT)
        
        # Separator
        ttk.Separator(sidebar, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Action Buttons
        actions_frame = ttk.LabelFrame(sidebar, text=" Quick Actions ", padding=10)
        actions_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(actions_frame,
            text="🔍 Network Scan",
            command=self.quick_network_scan,
            style='Accent.TButton').pack(fill=tk.X, pady=3)
        
        ttk.Button(actions_frame,
            text="🛡️ Security Check",
            command=self.quick_security_check,
            style='Accent.TButton').pack(fill=tk.X, pady=3)
        
        ttk.Button(actions_frame,
            text="📊 Generate Report",
            command=self.generate_report,
            style='Accent.TButton').pack(fill=tk.X, pady=3)
        
        ttk.Button(actions_frame,
            text="🔄 Sync with Backend",
            command=self.sync_with_backend,
            style='Accent.TButton').pack(fill=tk.X, pady=3)
        
        # Separator
        ttk.Separator(sidebar, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Monitoring Control
        monitor_frame = ttk.LabelFrame(sidebar, text=" Monitoring ", padding=10)
        monitor_frame.pack(fill=tk.X, pady=5)
        
        self.monitor_btn = ttk.Button(monitor_frame,
            text="▶️ Start Monitoring",
            command=self.toggle_monitoring,
            style='Accent.TButton')
        self.monitor_btn.pack(fill=tk.X, pady=3)
        
        # Exit button
        ttk.Button(sidebar,
            text="🚪 Exit Application",
            command=self.safe_exit).pack(side=tk.BOTTOM, fill=tk.X, pady=5)
    
    def create_main_content(self, parent):
        """إنشاء المحتوى الرئيسي مع التبويبات"""
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.tabs = {
            'dashboard': ttk.Frame(self.notebook),
            'devices': ttk.Frame(self.notebook),
            'security': ttk.Frame(self.notebook),
            'traffic': ttk.Frame(self.notebook),
            'logs': ttk.Frame(self.notebook),
            'settings': ttk.Frame(self.notebook)
        }
        
        self.notebook.add(self.tabs['dashboard'], text='📊 Dashboard')
        self.notebook.add(self.tabs['devices'], text='📱 Network Devices')
        self.notebook.add(self.tabs['security'], text='🛡️ Security')
        self.notebook.add(self.tabs['traffic'], text='📈 Traffic Monitor')
        self.notebook.add(self.tabs['logs'], text='📋 Activity Logs')
        self.notebook.add(self.tabs['settings'], text='⚙️ Settings')
        
        # Initialize tabs
        self.init_dashboard_tab()
        self.init_devices_tab()
        self.init_security_tab()
        self.init_traffic_tab()
        self.init_logs_tab()
        self.init_settings_tab()
    
    def init_dashboard_tab(self):
        """تهيئة تبويب Dashboard"""
        tab = self.tabs['dashboard']
        
        # Overview Cards
        cards_frame = ttk.Frame(tab)
        cards_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Network Status Card
        status_card = ttk.LabelFrame(cards_frame, text=" Network Status ", padding=15)
        status_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.network_status_text = scrolledtext.ScrolledText(status_card,
            height=8,
            bg=self.colors['secondary'],
            fg=self.colors['light'],
            font=('Consolas', 10))
        self.network_status_text.pack(fill=tk.BOTH, expand=True)
        
        # Recent Alerts Card
        alerts_card = ttk.LabelFrame(cards_frame, text=" Recent Alerts ", padding=15)
        alerts_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.alerts_text = scrolledtext.ScrolledText(alerts_card,
            height=8,
            bg=self.colors['secondary'],
            fg=self.colors['warning'],
            font=('Consolas', 10))
        self.alerts_text.pack(fill=tk.BOTH, expand=True)
        
        # Statistics
        stats_frame = ttk.LabelFrame(tab, text=" Network Statistics ", padding=15)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame,
            height=10,
            bg=self.colors['secondary'],
            fg=self.colors['info'],
            font=('Consolas', 10))
        self.stats_text.pack(fill=tk.BOTH, expand=True)
    
    def init_devices_tab(self):
        """تهيئة تبويب Devices"""
        tab = self.tabs['devices']
        
        # Control panel
        control_frame = ttk.Frame(tab)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(control_frame,
            text="🔍 Scan Network",
            command=self.scan_network_devices,
            style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame,
            text="🔄 Refresh",
            command=self.refresh_devices,
            style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame,
            text="📤 Export List",
            command=self.export_devices,
            style='Accent.TButton').pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame,
            text="🗑️ Clear History",
            command=self.clear_devices_history,
            style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        # Devices table
        table_frame = ttk.Frame(tab)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create treeview
        columns = ('IP', 'MAC', 'Hostname', 'Vendor', 'Status', 'First Seen', 'Last Seen')
        self.devices_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        for col in columns:
            self.devices_tree.heading(col, text=col)
            self.devices_tree.column(col, width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.devices_tree.yview)
        self.devices_tree.configure(yscroll=scrollbar.set)
        
        self.devices_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def init_security_tab(self):
        """تهيئة تبويب Security"""
        tab = self.tabs['security']
        
        # Control panel
        control_frame = ttk.Frame(tab)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(control_frame,
            text="🛡️ Run Security Scan",
            command=self.run_security_scan,
            style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame,
            text="🔍 Port Scan",
            command=self.run_port_scan,
            style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame,
            text="⚠️ View Threats",
            command=self.view_threats,
            style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        # Security Results
        results_frame = ttk.LabelFrame(tab, text=" Security Scan Results ", padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.security_results = scrolledtext.ScrolledText(results_frame,
            bg=self.colors['secondary'],
            fg=self.colors['light'],
            font=('Consolas', 10))
        self.security_results.pack(fill=tk.BOTH, expand=True)
    
    def init_traffic_tab(self):
        """تهيئة تبويب Traffic Monitor"""
        tab = self.tabs['traffic']
        
        # Control panel
        control_frame = ttk.Frame(tab)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(control_frame,
            text="Traffic Monitoring:",
            style='Title.TLabel').pack(side=tk.LEFT, padx=5)
        
        self.traffic_btn = ttk.Button(control_frame,
            text="▶️ Start Capture",
            command=self.toggle_traffic_monitor,
            style='Accent.TButton')
        self.traffic_btn.pack(side=tk.LEFT, padx=5)
        
        # Traffic display
        traffic_frame = ttk.LabelFrame(tab, text=" Network Traffic ", padding=15)
        traffic_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.traffic_text = scrolledtext.ScrolledText(traffic_frame,
            bg=self.colors['secondary'],
            fg=self.colors['info'],
            font=('Consolas', 9))
        self.traffic_text.pack(fill=tk.BOTH, expand=True)
    
    def init_logs_tab(self):
        """تهيئة تبويب Logs"""
        tab = self.tabs['logs']
        
        # Control panel
        control_frame = ttk.Frame(tab)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(control_frame,
            text="🔄 Refresh Logs",
            command=self.refresh_logs,
            style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame,
            text="🗑️ Clear Logs",
            command=self.clear_logs,
            style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame,
            text="📤 Export Logs",
            command=self.export_logs,
            style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        # Filter
        ttk.Label(control_frame,
            text="Filter:",
            style='Title.TLabel').pack(side=tk.LEFT, padx=(20, 5))
        
        self.log_filter = ttk.Combobox(control_frame,
            values=['All', 'Info', 'Warning', 'Error', 'Security'],
            state='readonly',
            width=15)
        self.log_filter.current(0)
        self.log_filter.pack(side=tk.LEFT, padx=5)
        self.log_filter.bind('<<ComboboxSelected>>', lambda e: self.refresh_logs())
        
        # Logs display
        logs_frame = ttk.Frame(tab)
        logs_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.logs_text = scrolledtext.ScrolledText(logs_frame,
            bg=self.colors['secondary'],
            fg=self.colors['light'],
            font=('Consolas', 9))
        self.logs_text.pack(fill=tk.BOTH, expand=True)
    
    def init_settings_tab(self):
        """تهيئة تبويب Settings"""
        tab = self.tabs['settings']
        
        # Backend Settings
        backend_frame = ttk.LabelFrame(tab, text=" Backend API Settings ", padding=15)
        backend_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # API URL
        url_frame = ttk.Frame(backend_frame)
        url_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(url_frame, text="API URL:", width=15).pack(side=tk.LEFT)
        self.api_url_entry = ttk.Entry(url_frame)
        self.api_url_entry.insert(0, self.api.base_url)
        self.api_url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # API Token
        token_frame = ttk.Frame(backend_frame)
        token_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(token_frame, text="API Token:", width=15).pack(side=tk.LEFT)
        self.api_token_entry = ttk.Entry(token_frame, show="*")
        self.api_token_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Test connection
        ttk.Button(backend_frame,
            text="🔌 Test Connection",
            command=self.test_backend_connection,
            style='Accent.TButton').pack(pady=10)
        
        # Scan Settings
        scan_frame = ttk.LabelFrame(tab, text=" Scan Settings ", padding=15)
        scan_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Auto scan interval
        interval_frame = ttk.Frame(scan_frame)
        interval_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(interval_frame, text="Auto Scan Interval (minutes):", width=25).pack(side=tk.LEFT)
        self.scan_interval = ttk.Spinbox(interval_frame, from_=1, to=60, width=10)
        self.scan_interval.set(1)
        self.scan_interval.pack(side=tk.LEFT, padx=5)
        
        # Alert Settings
        alert_frame = ttk.LabelFrame(tab, text=" Alert Settings ", padding=15)
        alert_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.alert_new_device = tk.BooleanVar(value=True)
        ttk.Checkbutton(alert_frame,
            text="Alert on new device detected",
            variable=self.alert_new_device).pack(anchor=tk.W, pady=3)
        
        self.alert_suspicious = tk.BooleanVar(value=True)
        ttk.Checkbutton(alert_frame,
            text="Alert on suspicious activity",
            variable=self.alert_suspicious).pack(anchor=tk.W, pady=3)
        
        # Save button
        ttk.Button(tab,
            text="💾 Save Settings",
            command=self.save_settings,
            style='Accent.TButton').pack(pady=20)
    
    def create_status_bar(self, parent):
        """إنشاء شريط الحالة"""
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(parent,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            background=self.colors['accent'],
            foreground='white',
            padding=8,
            font=('Segoe UI', 9))
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.update_status("Ready - Waiting for initialization...")
    
    def update_status(self, message):
        """تحديث شريط الحالة"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_var.set(f"[{timestamp}] {message}")
        self.log_activity("INFO", message)
    
    def log_activity(self, level, message):
        """تسجيل النشاط في قاعدة البيانات"""
        try:
            self.db.log_activity(level, message)
        except Exception as e:
            print(f"Logging error: {e}")
    
    def perform_startup_checks(self):
        """إجراء الفحوصات الأولية"""
        threading.Thread(target=self._startup_checks_thread, daemon=True).start()
    
    def _startup_checks_thread(self):
        """فحوصات بدء التشغيل في Thread منفصل"""
        self.update_status("Performing startup checks...")
        
        # Get network info
        network_info = self.scanner.get_network_info()
        
        if network_info:
            self.root.after(0, lambda: self.local_ip_label.config(
                text=network_info.get('local_ip', 'N/A')))
            
            # Get public IP
            public_ip = self.scanner.get_public_ip()
            if public_ip:
                self.root.after(0, lambda: self.public_ip_label.config(text=public_ip))
            
            # Update dashboard
            self.root.after(0, lambda: self.update_dashboard_info(network_info))
        
        # Test backend connection
        self.test_backend_connection()
        
        # Load initial devices
        self.refresh_devices()
        
        self.update_status("Startup checks completed")
    
    def update_dashboard_info(self, network_info):
        """تحديث معلومات Dashboard"""
        self.network_status_text.delete(1.0, tk.END)
        self.network_status_text.insert(tk.END, "=== Network Information ===\n\n")
        
        for key, value in network_info.items():
            if key != 'interfaces':
                self.network_status_text.insert(tk.END, f"{key}: {value}\n")
    
    # Action Methods
    def quick_network_scan(self):
        """فحص سريع للشبكة"""
        self.update_status("Starting quick network scan...")
        threading.Thread(target=self._quick_scan_thread, daemon=True).start()
    
    def _quick_scan_thread(self):
        """Thread للفحص السريع"""
        try:
            devices = self.scanner.scan_network()
            
            # Save to database
            for device in devices:
                self.db.save_device(device)
            
            # Update UI
            self.root.after(0, lambda: self.refresh_devices())
            self.root.after(0, lambda: self.devices_count_label.config(
                text=str(len(devices))))
            
            self.update_status(f"Quick scan completed - Found {len(devices)} devices")
            
            # Auto sync if connected
            if self.api_connected:
                self.root.after(0, self.sync_with_backend)
                
        except Exception as e:
            self.update_status(f"Scan error: {str(e)}")
            messagebox.showerror("Scan Error", f"An error occurred:\n{str(e)}")
    
    def quick_security_check(self):
        """فحص أمني سريع"""
        self.update_status("Running security check...")
        threading.Thread(target=self._security_check_thread, daemon=True).start()
    
    def _security_check_thread(self):
        """Thread للفحص الأمني"""
        try:
            results = self.security.quick_security_check()
            
            # Save alerts to database for sync
            for alert_msg in results.get('alerts', []):
                # Determine severity
                severity = 'Medium'
                if 'Dangerous' in alert_msg or 'Critical' in alert_msg:
                    severity = 'High'
                
                # Create alert object
                alert_data = {
                    'type': 'Security Scan',
                    'severity': severity,
                    'description': alert_msg.replace('⚠️ ', '').replace('🚨 ', '').replace('🔥 ', ''),
                    'source_ip': self.scanner.get_network_info().get('local_ip', 'unknown'),
                    'target_ip': 'localhost'
                }
                self.db.save_security_alert(alert_data)

            # Display results
            alert_count = len(results.get('alerts', []))
            self.root.after(0, lambda: self.alerts_count_label.config(
                text=str(alert_count)))
            
            # Update alerts display
            self.root.after(0, lambda: self.display_security_results(results))
            
            self.update_status(f"Security check completed - {alert_count} alerts")
            
            # Auto sync if connected and alerts found
            if self.api_connected and alert_count > 0:
                self.root.after(0, self.sync_with_backend)

        except Exception as e:
            self.update_status(f"Security check error: {str(e)}")
    
    def display_security_results(self, results):
        """عرض نتائج الفحص الأمني"""
        self.alerts_text.delete(1.0, tk.END)
        self.alerts_text.insert(tk.END, "=== Security Alerts ===\n\n")
        
        for alert in results.get('alerts', []):
            self.alerts_text.insert(tk.END, f"⚠️ {alert}\n\n")
        
        if not results.get('alerts'):
            self.alerts_text.insert(tk.END, "✅ No security issues detected\n")
    
    def generate_report(self):
        """إنشاء تقرير شامل"""
        try:
            self.update_status("Generating report...")
            
            report_content = []
            report_content.append("="*50)
            report_content.append(f"SMART NETWORK GUARDIAN - SECURITY REPORT")
            report_content.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_content.append("="*50)
            report_content.append("\n")
            
            # 1. Network Overview
            report_content.append("1. NETWORK OVERVIEW")
            report_content.append("-" * 20)
            network_info = self.scanner.get_network_info()
            for k, v in network_info.items():
                if k != 'interfaces':
                    report_content.append(f"{k}: {v}")
            report_content.append(f"Public IP: {self.scanner.get_public_ip()}")
            report_content.append("\n")
            
            # 2. Devices
            report_content.append("2. CONNECTED DEVICES")
            report_content.append("-" * 20)
            devices = self.db.get_all_devices()
            report_content.append(f"Total Devices: {len(devices)}")
            for device in devices:
                report_content.append(f"- {device['ip']} ({device['hostname']}) - {device['vendor']}")
            report_content.append("\n")
            
            # 3. Security Status
            report_content.append("3. SECURITY STATUS")
            report_content.append("-" * 20)
            security_res = self.security.quick_security_check()
            report_content.append(f"Security Score: {security_res['score']}/100")
            report_content.append(f"Status: {security_res['status']}")
            
            if security_res['alerts']:
                report_content.append("\nALERTS:")
                for alert in security_res['alerts']:
                    report_content.append(f"[!] {alert}")
            else:
                report_content.append("\nNo Critical Alerts")
                
            report_content.append("\n")
            report_content.append("="*50)
            report_content.append("End of Report")
            
            # Save file
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")],
                title="Save Security Report",
                initialfile=f"Security_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(report_content))
                
                messagebox.showinfo("Report", "Report generated successfully!")
                self.update_status("Report generated")
            else:
                self.update_status("Report generation cancelled")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
            self.update_status("Report generation failed")
    
    def clear_devices_history(self):
        """مسح سجل الأجهزة بالكامل"""
        if messagebox.askyesno("تأكيد", "هل أنت متأكد من مسح جميع سجلات الأجهزة؟\nسيتم حذف الأجهزة الوهمية والقديمة."):
            if self.db.clear_devices():
                self.refresh_devices()
                self.devices_count_label.config(text="0")
                self.update_status("تم مسح سجل الأجهزة بنجاح")
                
                # Update Dashboard statistics too
                self._startup_checks_thread() 
            else:
                messagebox.showerror("خطأ", "فشل في مسح سجل الأجهزة")

    def sync_with_backend(self):
        """مزامنة البيانات مع Backend باستخدام API Client"""
        if not self.api_connected:
            self.update_status("Sync skipped - Not connected")
            return

        self.update_status("Syncing with backend...")
        
        def _sync():
            try:
                devices = self.db.get_all_devices()
                if not devices:
                    self.update_status("Nothing to sync")
                    return

                success, msg = self.api.sync_devices(devices)
                
                # Sync Alerts
                alerts = self.db.get_security_alerts(status='New')
                alerts_synced = 0
                if alerts:
                    self.update_status(f"Syncing {len(alerts)} alerts...")
                    for alert in alerts:
                        # Prepare alert data for API
                        alert_data = {
                            'alert_type': alert['alert_type'],
                            'severity': alert['severity'],
                            'description': alert['description'],
                            'source_ip': alert['source_ip'],
                            'resolved': alert['resolved']
                        }
                        
                        # Send to backend
                        alert_success, alert_msg = self.api.send_alert(alert_data)
                        if alert_success:
                            self.db.mark_alert_synced(alert['id'])
                            alerts_synced += 1
                        else:
                            print(f"Failed to sync alert {alert['id']}: {alert_msg}")

                if success:
                    status_msg = f"Sync completed: Devices synced"
                    if alerts_synced > 0:
                        status_msg += f", {alerts_synced} alerts sent"
                    self.update_status(status_msg)
                    # Show notification only if triggered manually (check thread name or something) 
                    # For now just log it
                    print(f"Sync success: {msg}")
                else:
                    self.update_status(f"Sync failed: {msg}")
                    
            except Exception as e:
                self.update_status(f"Sync error: {str(e)}")

        threading.Thread(target=_sync, daemon=True).start()
    
    def toggle_monitoring(self):
        """تشغيل/إيقاف المراقبة"""
        self.monitoring_active = not self.monitoring_active
        
        if self.monitoring_active:
            self.monitor_btn.config(text="⏸️ Stop Monitoring")
            self.update_status("Continuous monitoring started")
            threading.Thread(target=self._monitoring_thread, daemon=True).start()
            
            # Also start traffic monitor if not active
            if not getattr(self, 'traffic_monitor_active', False):
                self.toggle_traffic_monitor()
        else:
            self.monitor_btn.config(text="▶️ Start Monitoring")
            self.update_status("Monitoring stopped")
            
            # Also stop traffic monitor
            if getattr(self, 'traffic_monitor_active', False):
                self.toggle_traffic_monitor()
    
    def _monitoring_thread(self):
        """Thread للمراقبة المستمرة"""
        while self.monitoring_active:
            try:
                # Perform periodic scans
                devices = self.scanner.scan_network()
                
                # Check for new devices
                for device in devices:
                    if self.db.is_new_device(device):
                        self.log_activity("WARNING", f"New device detected: {device['ip']}")
                        if self.alert_new_device.get():
                            self.root.after(0, lambda d=device: messagebox.showwarning(
                                "New Device", 
                                f"New device detected!\nIP: {d['ip']}\nMAC: {d['mac']}"
                            ))
                    
                    self.db.save_device(device)
                
                # Wait for next scan
                interval = int(self.scan_interval.get()) * 60
                time.sleep(interval)
            except Exception as e:
                self.log_activity("ERROR", f"Monitoring error: {str(e)}")
    
    def scan_network_devices(self):
        """فحص أجهزة الشبكة"""
        self.quick_network_scan()
    
    def refresh_devices(self):
        """تحديث قائمة الأجهزة"""
        # Clear current items
        for item in self.devices_tree.get_children():
            self.devices_tree.delete(item)
        
        # Load from database
        devices = self.db.get_all_devices()
        
        for device in devices:
            self.devices_tree.insert('', tk.END, values=(
                device.get('ip', 'N/A'),
                device.get('mac', 'N/A'),
                device.get('hostname', 'Unknown'),
                device.get('vendor', 'Unknown'),
                device.get('status', 'Active'),
                device.get('first_seen', 'N/A'),
                device.get('last_seen', 'N/A')
            ))
        
        self.devices_count_label.config(text=str(len(devices)))
    
    def export_devices(self):
        """تصدير قائمة الأجهزة"""
        try:
            devices = self.db.get_all_devices()
            if not devices:
                messagebox.showwarning("Export", "No devices to export")
                return
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Export Devices List"
            )
            
            if file_path:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=devices[0].keys())
                    writer.writeheader()
                    writer.writerows(devices)
                
                messagebox.showinfo("Export", f"Successfully exported {len(devices)} devices")
                self.update_status("Devices list exported")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
    
    def run_security_scan(self):
        """تشغيل فحص أمني شامل"""
        self.quick_security_check()
        
        # Display in security tab
        self.notebook.select(self.tabs['security'])
    
    def run_port_scan(self):
        """فحص المنافذ"""
        target = self.scanner.get_network_info().get('local_ip')
        if not target:
            messagebox.showerror("Error", "Could not determine local IP")
            return
            
        self.update_status(f"Scanning ports on {target}...")
        self.security_results.delete(1.0, tk.END)
        self.security_results.insert(tk.END, f"Starting port scan on {target}...\n")
        self.security_results.insert(tk.END, "Scanning common ports (This may take a moment)...\n\n")
        
        def _scan_thread():
            try:
                # Scan most common ports
                results = self.security.scan_port_range(target, 20, 1024)
                
                def _update_ui():
                    if results:
                        for port_info in results:
                            self.security_results.insert(tk.END, 
                                f"[OPEN] Port {port_info['port']} ({port_info['service']})\n", 'danger')
                    else:
                        self.security_results.insert(tk.END, "No common open ports found.\n", 'success')
                    
                    self.update_status("Port scan completed")
                
                self.root.after(0, _update_ui)
                
            except Exception as e:
                self.root.after(0, lambda: self.security_results.insert(tk.END, f"Error: {str(e)}\n"))
        
        threading.Thread(target=_scan_thread, daemon=True).start()
    
    def view_threats(self):
        """عرض التهديدات"""
        try:
            # Threats are basically high severity logs or specific alerts
            threats = self.db.get_logs('Security')
            
            if not threats:
                messagebox.showinfo("Threats", "No active threats detected.\nSystem is secure! 🛡️")
                return
            
            # Show in a custom window
            threat_window = tk.Toplevel(self.root)
            threat_window.title("Active Threats")
            threat_window.geometry("600x400")
            
            list_frame = ttk.Frame(threat_window, padding=10)
            list_frame.pack(fill=tk.BOTH, expand=True)
            
            columns = ('Time', 'Level', 'Message')
            tree = ttk.Treeview(list_frame, columns=columns, show='headings')
            
            tree.heading('Time', text='Time')
            tree.column('Time', width=150)
            tree.heading('Level', text='Level')
            tree.column('Level', width=100)
            tree.heading('Message', text='Threat Description')
            tree.column('Message', width=300)
            
            for threat in threats:
                tree.insert('', tk.END, values=(
                    threat['timestamp'],
                    threat['level'],
                    threat['message']
                ))
            
            tree.pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view threats: {str(e)}")
    
    def toggle_traffic_monitor(self):
        """تشغيل/إيقاف مراقبة Traffic"""
        if getattr(self, 'traffic_monitor_active', False):
            self.traffic_monitor_active = False
            self.traffic_btn.config(text="▶️ Start Capture")
            self.update_status("Traffic monitoring stopped")
        else:
            self.traffic_monitor_active = True
            self.traffic_btn.config(text="⏹️ Stop Capture")
            self.update_status("Traffic monitoring started")
            self.traffic_text.delete(1.0, tk.END)
            self.traffic_text.insert(tk.END, "Starting Traffic Monitor (Speed/Usage)...\n\n")
            threading.Thread(target=self._traffic_monitor_thread, daemon=True).start()

    def _format_bytes(self, size):
        power = 2**10
        n = 0
        power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /= power
            n += 1
        return f"{size:.2f} {power_labels[n]}B"

    def _traffic_monitor_thread(self):
        last_net_io = psutil.net_io_counters()
        tick = 0
        
        while getattr(self, 'traffic_monitor_active', False):
            time.sleep(1)
            tick += 1
            
            current_net_io = psutil.net_io_counters()
            
            bytes_sent = current_net_io.bytes_sent - last_net_io.bytes_sent
            bytes_recv = current_net_io.bytes_recv - last_net_io.bytes_recv
            
            last_net_io = current_net_io
            
            # Update UI
            timestamp = datetime.now().strftime("%H:%M:%S")
            msg = f"[{timestamp}] Upload: {self._format_bytes(bytes_sent)}/s | Download: {self._format_bytes(bytes_recv)}/s\n"
            
            def _update():
                self.traffic_text.insert(tk.END, msg)
                self.traffic_text.see(tk.END)
                
            self.root.after(0, _update)
            
            # Save to DB every 5 seconds
            if tick % 5 == 0:
                try:
                    # Get device counts
                    dev_stats = self.db.get_statistics()
                    
                    # Convert to Mbps for DB (approx)
                    down_speed = (bytes_recv * 8) / 1_000_000
                    up_speed = (bytes_sent * 8) / 1_000_000
                    
                    stats_data = {
                        'total_devices': dev_stats.get('total_devices', 0),
                        'active_devices': dev_stats.get('active_devices', 0),
                        'download_speed': round(down_speed, 2),
                        'upload_speed': round(up_speed, 2),
                        'bandwidth_usage': round(down_speed + up_speed, 2),
                        'packet_loss': 0.0, # Placeholder
                        'latency': 0.0 # Placeholder
                    }
                    self.db.save_network_stats(stats_data)
                except Exception as e:
                    print(f"Error saving stats: {e}")
    
    def refresh_logs(self):
        """تحديث السجلات"""
        self.logs_text.delete(1.0, tk.END)
        
        filter_type = self.log_filter.get()
        logs = self.db.get_logs(filter_type if filter_type != 'All' else None)
        
        for log in logs:
            timestamp = log.get('timestamp', '')
            level = log.get('level', 'INFO')
            message = log.get('message', '')
            
            self.logs_text.insert(tk.END, f"[{timestamp}] [{level}] {message}\n")
    
    def clear_logs(self):
        """مسح السجلات"""
        if messagebox.askyesno("Clear Logs", "Are you sure you want to clear all logs?"):
            self.db.clear_logs()
            self.refresh_logs()
            self.update_status("Logs cleared")
    
    def export_logs(self):
        """تصدير السجلات"""
        try:
            logs = self.db.get_logs(None)
            if not logs:
                messagebox.showwarning("Export", "No logs to export")
                return
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Export Activity Logs"
            )
            
            if file_path:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=['id', 'timestamp', 'level', 'message'])
                    writer.writeheader()
                    writer.writerows(logs)
                
                messagebox.showinfo("Export", f"Successfully exported {len(logs)} logs")
                self.update_status("Logs exported")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
    
    def test_backend_connection(self):
        """اختبار الاتصال بـ Backend"""
        self.update_status("Testing backend connection...")
        threading.Thread(target=self._test_connection_thread, daemon=True).start()
    
    def _test_connection_thread(self):
        """Thread لاختبار الاتصال"""
        try:
            api_url = self.api_url_entry.get()
            response = requests.get(f"{api_url}/health/", timeout=5)
            
            if response.status_code == 200:
                self.root.after(0, lambda: self.backend_status.config(
                    text="🟢 Connected",
                    foreground=self.colors['success']))
                self.update_status("Backend connection successful")
            else:
                self.root.after(0, lambda: self.backend_status.config(
                    text="🔴 Error",
                    foreground=self.colors['danger']))
                self.update_status(f"Backend returned status {response.status_code}")
        except Exception as e:
            self.root.after(0, lambda: self.backend_status.config(
                text="🔴 Disconnected",
                foreground=self.colors['danger']))
            self.update_status(f"Backend connection failed: {str(e)}")
    
    def save_settings(self):
        """حفظ الإعدادات"""
        self.api_base_url = self.api_url_entry.get()
        self.api_token = self.api_token_entry.get()
        
        # Save to config file
        config = {
            'api_url': self.api_base_url,
            'api_token': self.api_token,
            'scan_interval': self.scan_interval.get(),
            'alert_new_device': self.alert_new_device.get(),
            'alert_suspicious': self.alert_suspicious.get()
        }
        
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        
        messagebox.showinfo("Settings", "Settings saved successfully!")
        self.update_status("Settings saved")
    
    def safe_exit(self):
        """إغلاق آمن للتطبيق"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.monitoring_active = False
            self.db.close()
            self.root.quit()


def main():
    """نقطة البداية الرئيسية"""
    root = tk.Tk()
    
    # Set window icon (optional)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    app = SmartNetworkGuardian(root)
    root.mainloop()


if __name__ == "__main__":
    main()
