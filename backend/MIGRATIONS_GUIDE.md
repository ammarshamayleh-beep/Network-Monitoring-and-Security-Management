# 🗄️ دليل إعداد قاعدة البيانات (Migrations)

## خطوات تشغيل قاعدة البيانات

### 1. التأكد من الإعدادات
تأكد أن `config/settings.py` يحتوي على:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 2. إنشاء Migrations

```bash
cd backend
python manage.py makemigrations devices
python manage.py makemigrations alerts
python manage.py makemigrations monitoring
python manage.py makemigrations
```

**النتيجة المتوقعة:**
```
Migrations for 'devices':
  apps/devices/migrations/0001_initial.py
    - Create model Device
Migrations for 'alerts':
  apps/alerts/migrations/0001_initial.py
    - Create model SecurityAlert
```

### 3. تطبيق Migrations

```bash
python manage.py migrate
```

**النتيجة المتوقعة:**
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying devices.0001_initial... OK
  Applying alerts.0001_initial... OK
  ...
```

### 4. إنشاء Superuser

```bash
python manage.py createsuperuser
```

أدخل:
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123` (أو أي كلمة مرور)

### 5. تشغيل السيرفر

```bash
python manage.py runserver
```

### 6. اختبار

افتح المتصفح:
```
http://localhost:8000/admin/           # Login as admin
http://localhost:8000/api/health/      # Should return {"status": "ok"}
http://localhost:8000/api/devices/     # Should show empty list []
```

## ✅ Checklist

- [ ] makemigrations نفذت بنجاح
- [ ] migrate نفذت بنجاح
- [ ] superuser تم إنشاؤه
- [ ] السيرفر يشتغل على port 8000
- [ ] Admin panel يفتح ويمكن تسجيل الدخول
- [ ] API endpoints تعمل

## 🔧 استكشاف الأخطاء

### خطأ: "No changes detected"
**الحل:**
```bash
python manage.py makemigrations --empty devices
```

### خطأ: "Table already exists"
**الحل:**
```bash
rm db.sqlite3
rm */migrations/0*.py
python manage.py makemigrations
python manage.py migrate
```

### خطأ: "Apps aren't loaded yet"
**الحل:**
تأكد من وجود:
```python
# في config/settings.py
INSTALLED_APPS = [
    ...
    'apps.devices',
    'apps.alerts',
    'apps.monitoring',
    'apps.users',
]
```

## 📊 بنية قاعدة البيانات

### Device Table
```sql
CREATE TABLE devices_device (
    id INTEGER PRIMARY KEY,
    ip_address VARCHAR(39) UNIQUE,
    mac_address VARCHAR(17) UNIQUE,
    hostname VARCHAR(255),
    vendor VARCHAR(255),
    status VARCHAR(20),
    is_trusted BOOLEAN,
    first_seen DATETIME,
    last_seen DATETIME,
    notes TEXT
);
```

### SecurityAlert Table
```sql
CREATE TABLE alerts_securityalert (
    id INTEGER PRIMARY KEY,
    alert_type VARCHAR(100),
    severity VARCHAR(20),
    description TEXT,
    device_id INTEGER,
    timestamp DATETIME,
    resolved BOOLEAN
);
```

## 🚀 جاهز!

بعد تنفيذ كل الخطوات، Backend جاهز للعمل!
