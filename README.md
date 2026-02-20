# 🛡️ Smart Network Guardian - دليل المشروع الشامل

## نظام متكامل لمراقبة الشبكات والأمن السيبراني

---

## 📋 **جدول المحتويات**

1. [نظرة عامة](#نظرة-عامة)
2. [هيكل المشروع](#هيكل-المشروع)
3. [المزايا والوظائف](#المزايا-والوظائف)
4. [التقنيات المستخدمة](#التقنيات-المستخدمة)
5. [التثبيت والإعداد](#التثبيت-والإعداد)
6. [شرح الملفات](#شرح-الملفات)
7. [استخدام النظام](#استخدام-النظام)
8. [API Documentation](#api-documentation)
9. [قاعدة البيانات](#قاعدة-البيانات)
10. [استكشاف الأخطاء](#استكشاف-الأخطاء)

---

## 🎯 **نظرة عامة**

**Smart Network Guardian** هو نظام احترافي متكامل لمراقبة الشبكات وحمايتها من التهديدات الأمنية.

### **مكونات المشروع:**

```
Smart Network Guardian
├── Desktop App (Python/Tkinter)      → تطبيق سطح مكتب للمراقبة
├── Backend API (Django/DRF)          → خادم API وقاعدة بيانات
└── Frontend Dashboard (React)         → لوحة تحكم ويب (قريباً)
```

### **الفكرة:**
- **Desktop App** يفحص الشبكة المحلية ويجمع البيانات
- **Backend** يخزن البيانات ويوفر API
- **Frontend** يعرض البيانات بشكل تفاعلي

---

## 📁 **هيكل المشروع**

```
SmartNetworkGuardian/
│
├── desktop_app/                    # تطبيق سطح المكتب
│   ├── main.py                     # الملف الرئيسي + واجهة المستخدم
│   ├── scanner.py                  # فحص الشبكة (Real Scanning)
│   ├── security.py                 # التحليل الأمني
│   ├── database.py                 # قاعدة بيانات محلية (SQLite)
│   ├── requirements.txt            # المكتبات المطلوبة
│   └── README.md                   # دليل الاستخدام
│
├── backend/                        # Django Backend
│   ├── config/                     # إعدادات Django
│   │   ├── settings.py             # الإعدادات الرئيسية
│   │   ├── urls.py                 # المسارات (Routes)
│   │   ├── wsgi.py                 # WSGI Server
│   │   └── asgi.py                 # ASGI + WebSocket
│   │
│   ├── apps/                       # تطبيقات Django
│   │   ├── devices/                # إدارة الأجهزة
│   │   │   ├── models.py           # نماذج قاعدة البيانات
│   │   │   ├── serializers.py     # محولات API
│   │   │   ├── views.py            # API Endpoints
│   │   │   ├── urls.py             # المسارات
│   │   │   └── admin.py            # لوحة الإدارة
│   │   │
│   │   ├── alerts/                 # التنبيهات الأمنية
│   │   ├── monitoring/             # المراقبة المستمرة
│   │   └── users/                  # إدارة المستخدمين
│   │
│   ├── manage.py                   # أداة إدارة Django
│   ├── requirements.txt            # المكتبات المطلوبة
│   └── README.md                   # دليل Backend
│
├── frontend/                       # React Frontend (قريباً)
│
├── docs/                           # التوثيق
│   ├── PROJECT_REPORT.md          # تقرير المشروع
│   ├── INSTALLATION.md            # دليل التثبيت
│   └── API_DOCS.md                # توثيق API
│
└── README.md                       # الدليل الرئيسي (هذا الملف)
```

---

## ✨ **المزايا والوظائف**

### **1. Desktop Application**

#### **فحص الشبكة (Network Scanning)**
- ✅ فحص حقيقي للأجهزة (مش simulation!)
- ✅ استخدام ARP Protocol للكشف عن الأجهزة
- ✅ Ping Sweep كـ Fallback
- ✅ الحصول على IP, MAC, Hostname, Vendor
- ✅ تحديد نوع الجهاز تلقائياً

#### **التحليل الأمني (Security Analysis)**
- ✅ فحص المنافذ المفتوحة (Port Scanning)
- ✅ فحص حالة الجدار الناري (Firewall Check)
- ✅ كشف ARP Spoofing
- ✅ تحليل أنماط حركة المرور
- ✅ تقييم أمني شامل مع Security Score

#### **المراقبة المستمرة**
- ✅ Real-time Monitoring
- ✅ كشف الأجهزة الجديدة تلقائياً
- ✅ تنبيهات فورية
- ✅ سجل كامل للنشاطات

#### **قاعدة البيانات المحلية**
- ✅ SQLite مدمجة
- ✅ حفظ معلومات الأجهزة
- ✅ سجل النشاطات (Activity Logs)
- ✅ التنبيهات الأمنية
- ✅ إحصائيات تفصيلية

#### **الواجهة الرسومية**
- ✅ Dark Theme احترافي
- ✅ تبويبات منظمة
- ✅ Real-time Updates
- ✅ سهلة الاستخدام

### **2. Django Backend**

#### **REST API**
- ✅ Endpoints كاملة للأجهزة
- ✅ Authentication (Token-based)
- ✅ Filtering & Searching
- ✅ Pagination
- ✅ Swagger Documentation (قريباً)

#### **قاعدة البيانات**
- ✅ Models احترافية
- ✅ Relationships صحيحة
- ✅ Indexes للأداء
- ✅ PostgreSQL/SQLite Support

#### **Admin Panel**
- ✅ Django Admin مخصص
- ✅ إدارة الأجهزة
- ✅ عرض الإحصائيات
- ✅ إدارة المستخدمين

#### **WebSocket Support**
- ✅ Django Channels
- ✅ Real-time Communication
- ✅ Live Updates للـ Frontend

### **3. Frontend Dashboard (React)** - قريباً
- 📊 لوحة تحكم تفاعلية
- 📈 Charts & Graphs
- 🔔 Real-time Notifications
- 📱 Responsive Design

---

## 🔧 **التقنيات المستخدمة**

### **Desktop App:**
```python
- Python 3.8+
- Tkinter (GUI)
- Scapy (Network Scanning)
- Netifaces (Network Interfaces)
- SQLite (Database)
- Requests (API Communication)
```

### **Backend:**
```python
- Django 4.2+
- Django REST Framework
- Django Channels (WebSocket)
- PostgreSQL / SQLite
- CORS Headers
```

### **Frontend:** (قريباً)
```javascript
- React 18+
- Material-UI / Tailwind CSS
- Axios (API Client)
- Chart.js / Recharts
- WebSocket Client
```

---

## 🚀 **التثبيت والإعداد**

### **المتطلبات الأساسية:**
- Python 3.8 أو أحدث
- pip (مدير حزم Python)
- Node.js & npm (للـ Frontend فقط)
- صلاحيات Administrator (لبعض المزايا)

### **1. Desktop App**

```bash
# 1. انتقل لمجلد التطبيق
cd desktop_app

# 2. ثبّت المكتبات
pip install -r requirements.txt

# 3. شغّل التطبيق
python main.py

# ملاحظة: على Windows، شغّل كـ Administrator
# على Linux: sudo python main.py
```

### **2. Django Backend**

```bash
# 1. انتقل لمجلد Backend
cd backend

# 2. ثبّت المكتبات
pip install -r requirements.txt

# 3. أنشئ قاعدة البيانات
python manage.py makemigrations
python manage.py migrate

# 4. أنشئ حساب Admin
python manage.py createsuperuser

# 5. شغّل السيرفر
python manage.py runserver

# Backend يشتغل على: http://localhost:8000
```

### **3. Frontend** (قريباً)

```bash
cd frontend
npm install
npm start
```

---

## 📖 **شرح الملفات بالتفصيل**

### **Desktop App Files:**

#### **1. main.py**
```python
الملف الرئيسي للتطبيق

المكونات:
- SmartNetworkGuardian: الـ Class الرئيسي
- setup_modern_theme(): إعداد الثيم
- create_ui(): إنشاء الواجهة
- init_*_tab(): تهيئة كل تبويب
- Action Methods: الوظائف الرئيسية

المزايا الجديدة:
✅ Real Scanner Integration
✅ Database Integration
✅ API Communication
✅ Real-time Monitoring
✅ Professional UI
```

#### **2. scanner.py**
```python
وحدة فحص الشبكة - Real Implementation

الوظائف الرئيسية:
- scan_network(): فحص الأجهزة بـ ARP
- ping_sweep(): Fallback بـ Ping
- get_network_info(): معلومات الشبكة الأساسية
- get_public_ip(): الحصول على IP العام
- get_vendor(): تحديد الشركة المصنعة

التقنيات:
- Scapy للـ ARP Scanning
- Subprocess للـ Ping
- MAC Vendor Lookup
- Netifaces للـ Interfaces
```

#### **3. security.py**
```python
وحدة التحليل الأمني

الوظائف:
- quick_security_check(): فحص سريع شامل
- check_common_ports(): فحص المنافذ
- check_firewall_status(): حالة الجدار الناري
- detect_arp_spoofing(): كشف ARP Attacks
- analyze_traffic_pattern(): تحليل حركة المرور
- generate_security_report(): تقرير شامل

النتائج:
- Security Score (0-100)
- Alerts & Warnings
- Recommendations
```

#### **4. database.py**
```python
إدارة قاعدة البيانات المحلية (SQLite)

الجداول:
1. devices - معلومات الأجهزة
2. activity_logs - سجل النشاطات
3. security_alerts - التنبيهات الأمنية
4. network_stats - الإحصائيات
5. scan_history - سجل الفحوصات
6. settings - الإعدادات

الوظائف:
- save_device()
- get_all_devices()
- log_activity()
- save_security_alert()
- get_statistics()
```

### **Backend Files:**

#### **1. config/settings.py**
```python
إعدادات Django الكاملة

التكوين:
- INSTALLED_APPS: التطبيقات المثبتة
- MIDDLEWARE: الوسطاء
- DATABASES: PostgreSQL/SQLite
- REST_FRAMEWORK: إعدادات API
- CORS: السماح للـ Frontend
- CHANNELS: WebSocket Support
- LOGGING: سجلات النظام
```

#### **2. apps/devices/models.py**
```python
نماذج قاعدة البيانات

Models:
1. Device - الجهاز
   - IP, MAC, Hostname
   - Vendor, Type, Status
   - Security Score
   - Open Ports, Services
   - Metadata

2. DeviceHistory - السجل التاريخي
   - Event Type
   - Old/New Values
   - Timestamp

3. NetworkScan - فحوصات الشبكة
   - Scan Type, Status
   - Devices Found
   - Duration, Results
```

#### **3. apps/devices/serializers.py**
```python
محولات البيانات للـ API

Serializers:
- DeviceSerializer: كامل
- DeviceListSerializer: مبسط للقوائم
- DeviceCreateSerializer: للإنشاء
- DeviceUpdateSerializer: للتحديث
- NetworkScanSerializer: للفحوصات
- DeviceStatisticsSerializer: للإحصائيات
```

#### **4. apps/devices/views.py**
```python
API Endpoints

ViewSets:
1. DeviceViewSet
   - CRUD Operations
   - /api/devices/ - List/Create
   - /api/devices/{id}/ - Retrieve/Update/Delete
   - /api/devices/online/ - الأجهزة النشطة
   - /api/devices/statistics/ - الإحصائيات
   - /api/devices/sync/ - المزامنة

2. NetworkScanViewSet
   - CRUD للفحوصات
   - /api/devices/scans/ - List/Create
   - /api/devices/scans/latest/ - آخر فحص
```

---

## 🔌 **API Documentation**

### **Authentication**

```bash
# الحصول على Token
POST /api/auth/login/
{
  "username": "admin",
  "password": "password"
}

Response:
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}

# استخدام Token
Headers:
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### **Devices Endpoints**

```bash
# 1. Get All Devices
GET /api/devices/
Headers: Authorization: Token {token}

Response:
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "ip_address": "192.168.1.100",
      "mac_address": "AA:BB:CC:DD:EE:FF",
      "hostname": "My-PC",
      "vendor": "Apple",
      "device_type": "computer",
      "status": "active",
      "is_online": true,
      ...
    }
  ]
}

# 2. Create Device
POST /api/devices/
{
  "ip_address": "192.168.1.101",
  "mac_address": "11:22:33:44:55:66",
  "hostname": "New-Device",
  "vendor": "Samsung"
}

# 3. Get Online Devices
GET /api/devices/online/

# 4. Get Statistics
GET /api/devices/statistics/

Response:
{
  "total_devices": 10,
  "active_devices": 7,
  "trusted_devices": 5,
  "devices_by_type": {...},
  "security_stats": {...}
}

# 5. Sync from Desktop App
POST /api/devices/sync/
{
  "devices": [
    {
      "ip": "192.168.1.100",
      "mac": "AA:BB:CC:DD:EE:FF",
      "hostname": "Device1"
    },
    ...
  ]
}

# 6. Block Device
POST /api/devices/{id}/block/

# 7. Mark as Trusted
POST /api/devices/{id}/mark_trusted/
```

---

## 💾 **قاعدة البيانات**

### **Desktop App (SQLite):**

```sql
-- Devices Table
CREATE TABLE devices (
    id INTEGER PRIMARY KEY,
    ip TEXT NOT NULL,
    mac TEXT,
    hostname TEXT,
    vendor TEXT,
    status TEXT,
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    device_type TEXT,
    is_trusted BOOLEAN
);

-- Activity Logs
CREATE TABLE activity_logs (
    id INTEGER PRIMARY KEY,
    timestamp TIMESTAMP,
    level TEXT,
    message TEXT,
    source TEXT,
    details TEXT
);

-- Security Alerts
CREATE TABLE security_alerts (
    id INTEGER PRIMARY KEY,
    timestamp TIMESTAMP,
    alert_type TEXT,
    severity TEXT,
    description TEXT,
    status TEXT
);
```

### **Backend (PostgreSQL/SQLite):**

```python
# Django Models تنشئ الجداول تلقائياً
python manage.py makemigrations
python manage.py migrate

# الجداول الرئيسية:
- devices_device
- devices_devicehistory
- devices_networkscan
- alerts_securityalert
- monitoring_networkstatistics
- auth_user
```

---

## 🎨 **استخدام النظام**

### **سيناريو كامل:**

```
1. شغّل Django Backend
   cd backend
   python manage.py runserver

2. شغّل Desktop App
   cd desktop_app
   python main.py

3. في Desktop App:
   - اضغط "Network Scan" لفحص الشبكة
   - شاهد الأجهزة في تبويب "Devices"
   - اضغط "Security Check" للفحص الأمني

4. في Settings:
   - أدخل Backend URL: http://localhost:8000/api
   - أدخل Token (من Django Admin)
   - اضغط "Sync with Backend"

5. تحقق من البيانات:
   - افتح Django Admin: http://localhost:8000/admin
   - شاهد الأجهزة المزامنة
   - اطّلع على الإحصائيات
```

---

## 🛠️ **استكشاف الأخطاء**

### **Desktop App:**

**المشكلة:** "No devices found"
```
الحل:
1. شغّل بصلاحيات Administrator/sudo
2. تأكد من اتصالك بالشبكة
3. ثبّت Npcap (Windows) أو libpcap (Linux)
4. جرّب Ping Sweep بدلاً من ARP
```

**المشكلة:** "Permission denied"
```
الحل:
Windows: Run as Administrator
Linux: sudo python main.py
macOS: منح صلاحيات في System Preferences
```

### **Backend:**

**المشكلة:** "ModuleNotFoundError"
```
الحل:
pip install -r requirements.txt
```

**المشكلة:** "Database error"
```
الحل:
python manage.py makemigrations
python manage.py migrate
```

**المشكلة:** "CORS error"
```
الحل:
تحقق من CORS_ALLOWED_ORIGINS في settings.py
```

---

## 📊 **الإحصائيات والتقارير**

### **المتاحة حالياً:**
- ✅ عدد الأجهزة (Total/Active)
- ✅ الأجهزة حسب النوع
- ✅ الأجهزة حسب الشركة المصنعة
- ✅ Security Score متوسط
- ✅ الأجهزة ذات الثغرات
- ✅ سجل الفحوصات

### **قريباً:**
- 📈 Bandwidth Usage
- 📊 Traffic Analysis
- 🕐 Historical Trends
- 📄 PDF Reports
- 📧 Email Reports

---

## 🚧 **الميزات القادمة**

### **Phase 1** (الأسبوع القادم):
- [ ] Alerts App كامل
- [ ] Monitoring App
- [ ] Users App
- [ ] Admin Panel تحسينات

### **Phase 2** (الأسابيع القادمة):
- [ ] React Frontend
- [ ] Real-time Dashboard
- [ ] Charts & Graphs
- [ ] Notifications System

### **Phase 3** (المستقبل):
- [ ] Mobile App (React Native)
- [ ] Deep Packet Inspection
- [ ] Machine Learning
- [ ] Intrusion Prevention System
- [ ] Cloud Integration

---

## 📚 **المراجع والمصادر**

### **Network Security:**
- OWASP Top 10
- NIST Cybersecurity Framework
- Cisco Security Best Practices

### **Technical Documentation:**
- Django Documentation
- Django REST Framework
- Scapy Documentation
- React Documentation

### **Tools & Libraries:**
- Wireshark (Packet Analysis)
- Nmap (Port Scanning)
- Metasploit (Security Testing)

---

## 👨‍💻 **معلومات المشروع**

**اسم المشروع:** Smart Network Guardian
**الإصدار:** 2.0 Professional Edition
**النوع:** مشروع تخرج - علوم الحاسوب
**الترخيص:** MIT License

**المطور:** [اسمك]
**الجامعة:** [اسم الجامعة]
**السنة:** 2024

---

## 🤝 **المساهمة والتطوير**

### **كيف تساهم:**
1. Fork المشروع
2. أنشئ Branch جديد (`git checkout -b feature/amazing-feature`)
3. Commit التعديلات (`git commit -m 'Add amazing feature'`)
4. Push للـ Branch (`git push origin feature/amazing-feature`)
5. افتح Pull Request

### **Guidelines:**
- اكتب كود نظيف ومنظم
- أضف تعليقات بالعربي/English
- اتبع PEP 8 لـ Python
- اختبر التعديلات قبل الـ Commit

---

## 📧 **التواصل والدعم**

للأسئلة والاستفسارات:
- افتح Issue في GitHub
- راسلني على [بريدك الإلكتروني]

---

## 🎓 **للأغراض الأكاديمية**

هذا المشروع مصمم خصيصاً لمشاريع التخرج في تخصصات:
- علوم الحاسوب (Computer Science)
- هندسة الشبكات (Network Engineering)
- الأمن السيبراني (Cybersecurity)
- هندسة البرمجيات (Software Engineering)

### **الجوانب الأكاديمية:**
✅ Problem Statement واضح
✅ Solution Architecture محترف
✅ Implementation عملي
✅ Testing & Validation
✅ Documentation شامل
✅ Scalability & Future Work

---

## ⚖️ **إخلاء المسؤولية**

هذا النظام مصمم للأغراض التعليمية والبحثية. استخدامه لأغراض غير قانونية أو غير أخلاقية هو مسؤولية المستخدم بالكامل.

**تنبيه:** فحص الشبكات بدون إذن قد يكون غير قانوني في بعض الدول.

---

## 📝 **Changelog**

### **v2.0 (2024-02-01)**
- ✅ Real Network Scanner
- ✅ Django Backend Integration
- ✅ REST API Complete
- ✅ WebSocket Support
- ✅ Professional UI
- ✅ Security Analysis
- ✅ Database Integration

### **v1.0 (الإصدار القديم)**
- Basic UI
- Simulated Scanning
- No Backend
- Limited Features

---

**آخر تحديث:** فبراير 2024

**جاهز للاستخدام والتطوير! 🚀**
