# 📦 دليل التثبيت الشامل - Smart Network Guardian

## خطوة بخطوة للتثبيت والتشغيل

---

## 📋 المتطلبات الأساسية

### 1. البرامج المطلوبة:

#### Windows:
```
✓ Python 3.8 أو أحدث
✓ Git (اختياري)
✓ Visual Studio Code أو أي Code Editor
✓ Npcap (لفحص الشبكة)
```

#### Linux/Mac:
```
✓ Python 3.8+
✓ pip
✓ libpcap-dev (Linux)
```

---

## 🚀 الجزء الأول: Desktop Application

### الخطوة 1: تحميل المشروع

**الطريقة 1: Git**
```bash
git clone https://github.com/your-repo/SmartNetworkGuardian.git
cd SmartNetworkGuardian
```

**الطريقة 2: تحميل مباشر**
- حمّل ملف ZIP
- فك الضغط
- افتح المجلد

### الخطوة 2: تثبيت Python

**Windows:**
1. حمّل Python من [python.org](https://www.python.org/downloads/)
2. شغّل الملف وفعّل "Add Python to PATH"
3. تحقق من التثبيت:
```cmd
python --version
pip --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**Mac:**
```bash
brew install python3
```

### الخطوة 3: تثبيت Npcap (Windows فقط)

1. حمّل Npcap من [npcap.com](https://npcap.com/)
2. شغّل الملف كـ Administrator
3. فعّل "Install Npcap in WinPcap API-compatible Mode"

### الخطوة 4: تثبيت المكتبات

```bash
cd desktop_app
pip install -r requirements.txt
```

**ملاحظة:** إذا واجهت مشاكل:
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### الخطوة 5: تشغيل التطبيق

**Windows:**
```cmd
python main.py
```

**Linux/Mac (يحتاج sudo للفحص):**
```bash
sudo python3 main.py
```

---

## ⚙️ الجزء الثاني: Django Backend

### الخطوة 1: انتقل لمجلد Backend

```bash
cd backend
```

### الخطوة 2: إنشاء Virtual Environment (مستحسن)

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### الخطوة 3: تثبيت المكتبات

```bash
pip install -r requirements.txt
```

### الخطوة 4: إعداد قاعدة البيانات

**استخدام SQLite (للتطوير):**
```bash
python manage.py makemigrations
python manage.py migrate
```

**استخدام PostgreSQL (للإنتاج):**

1. ثبّت PostgreSQL
2. أنشئ قاعدة بيانات:
```sql
CREATE DATABASE network_guardian_db;
CREATE USER guardian_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE network_guardian_db TO guardian_user;
```

3. عدّل `config/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'network_guardian_db',
        'USER': 'guardian_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

4. شغّل migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### الخطوة 5: إنشاء مستخدم Admin

```bash
python manage.py createsuperuser
```

اتبع التعليمات وأدخل:
- Username
- Email
- Password

### الخطوة 6: تشغيل Backend

```bash
python manage.py runserver
```

الـ Backend شغال على: `http://localhost:8000`

### الخطوة 7: اختبار API

افتح المتصفح:
```
http://localhost:8000/admin/        # لوحة الإدارة
http://localhost:8000/api/health/   # Health check
```

---

## 🎨 الجزء الثالث: React Frontend (قريباً)

### الخطوة 1: تثبيت Node.js

حمّل من [nodejs.org](https://nodejs.org/)

تحقق:
```bash
node --version
npm --version
```

### الخطوة 2: تثبيت المكتبات

```bash
cd frontend
npm install
```

### الخطوة 3: تشغيل Frontend

```bash
npm start
```

يفتح على: `http://localhost:3000`

---

## 🔗 ربط المكونات

### 1. Desktop App ↔ Backend

في Desktop App → Settings:
```
API URL: http://localhost:8000/api
```

### 2. Frontend ↔ Backend

في `frontend/src/config.js`:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

---

## ✅ التحقق من التثبيت

### Desktop App:
```
✓ النافذة تفتح بدون أخطاء
✓ Quick Stats تظهر IP Address
✓ Network Scan يعمل ويجد أجهزة
✓ Database يحفظ البيانات
```

### Backend:
```
✓ http://localhost:8000/admin/ يفتح
✓ http://localhost:8000/api/health/ يرجع {"status": "ok"}
✓ يمكن تسجيل الدخول بالـ superuser
```

### Frontend:
```
✓ http://localhost:3000 يفتح
✓ Dashboard يعرض البيانات
✓ API calls تعمل
```

---

## 🛠️ استكشاف الأخطاء

### مشكلة: "ModuleNotFoundError"
**الحل:**
```bash
pip install [اسم المكتبة الناقصة]
```

### مشكلة: "Permission Denied" في Network Scan
**الحل:**
- Windows: شغّل كـ Administrator
- Linux/Mac: استخدم sudo

### مشكلة: "Port already in use"
**الحل:**
```bash
# غيّر Port في settings.py
python manage.py runserver 8001
```

### مشكلة: Scapy لا يعمل
**الحل:**
- Windows: ثبّت Npcap
- Linux: `sudo apt install libpcap-dev`

### مشكلة: CORS Error في Frontend
**الحل:**
تأكد من `settings.py`:
```python
CORS_ALLOW_ALL_ORIGINS = True
```

---

## 📝 بعد التثبيت

### 1. اختبر Desktop App:
- شغّل Network Scan
- شغّل Security Check
- جرّب Monitoring

### 2. اختبر Backend:
- ادخل Admin Panel
- أضف device يدوياً
- جرّب API endpoints

### 3. ارب��هم مع بعض:
- شغّل Desktop App
- شغّل Backend
- اضغط "Sync with Backend"

---

## 🎓 للاستخدام كمشروع تخرج

### 1. غيّر المعلومات:
- اسمك في README.md
- معلومات الجامعة
- سنة التخرج

### 2. أضف screenshots:
- التقط صور للواجهات
- أضفها في `docs/screenshots/`

### 3. اكتب التقرير:
- استخدم `docs/PROJECT_REPORT.md` كقالب
- أضف نتائج الاختبارات
- وثّق المشاكل والحلول

---

## 📊 الخطوات التالية

### للتطوير:
1. أضف ميزات جديدة
2. حسّن Security Analysis
3. أضف Machine Learning
4. طوّر Mobile App

### للنشر:
1. استخدم PostgreSQL
2. ضع Backend على خادم
3. استخدم Nginx/Apache
4. فعّل HTTPS

---

## 🆘 المساعدة

### الموارد:
- Documentation: `docs/`
- Examples: `examples/`
- Issues: GitHub Issues

### الأسئلة الشائعة:
راجع `docs/FAQ.md`

---

## ✨ نصائح نهائية

1. **اقرأ الكود** - كل شي موثق ومشروح
2. **جرّب** - اختبر كل ميزة
3. **طوّر** - أضف لمساتك الخاصة
4. **وثّق** - اكتب كل شي عملته

---

**مبروك! المشروع جاهز للعمل 🎉**

أي استفسارات؟ افتح Issue في GitHub أو راجع Documentation!

---

**آخر تحديث:** ديسمبر 2024
