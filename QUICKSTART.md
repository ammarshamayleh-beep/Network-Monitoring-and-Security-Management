# 🚀 Smart Network Guardian - دليل التشغيل السريع

## ⚡ البدء السريع (Quick Start)

### **الخطوة 1: تشغيل Backend**

```bash
# انتقل لمجلد Backend
cd backend

# ثبّت المكتبات
pip install -r requirements.txt

# أنشئ قاعدة البيانات
python manage.py makemigrations
python manage.py migrate

# أنشئ حساب Admin
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123

# شغّل السيرفر
python manage.py runserver

# ✅ Backend يشتغل على: http://localhost:8000
```

### **الخطوة 2: تشغيل Desktop App**

```bash
# انتقل لمجلد Desktop App
cd desktop_app

# ثبّت المكتبات
pip install -r requirements.txt

# شغّل التطبيق
# Windows:
python main.py  # أو Run as Administrator

# Linux:
sudo python main.py

# macOS:
sudo python main.py

# ✅ التطبيق يفتح بواجهة رسومية
```

---

## 🔧 **الإعدادات الأولية**

### **في Desktop App:**

1. **افتح تبويب Settings**
2. **أدخل Backend URL:**
   ```
   http://localhost:8000/api
   ```
3. **الحصول على API Token:**
   - افتح Django Admin: http://localhost:8000/admin
   - اذهب لـ Auth > Tokens
   - أنشئ Token جديد للمستخدم
   - انسخ الـ Token

4. **أدخل Token في Settings**
5. **اضغط "Test Connection"**
6. **إذا ظهر "🟢 Connected" يعني تمام!**

---

## 📋 **الاستخدام الأساسي**

### **فحص الشبكة:**
1. اضغط "🔍 Network Scan" في Sidebar
2. انتظر 30-60 ثانية
3. شاهد الأجهزة في تبويب "Devices"

### **الفحص الأمني:**
1. اضغط "🛡️ Security Check"
2. اطّلع على النتائج والتوصيات
3. تابع التنبيهات في Dashboard

### **المراقبة المستمرة:**
1. اضغط "▶️ Start Monitoring"
2. سيتم فحص الشبكة تلقائياً كل X دقيقة
3. ستحصل على تنبيهات للأجهزة الجديدة

### **المزامنة مع Backend:**
1. اضغط "🔄 Sync with Backend"
2. البيانات تُرسل للسيرفر
3. يمكنك رؤيتها في Django Admin

---

## 🌐 **الوصول للخدمات**

- **Django Admin:** http://localhost:8000/admin
  - Username: admin
  - Password: [اللي حطيته]

- **API Root:** http://localhost:8000/api/
- **Devices API:** http://localhost:8000/api/devices/
- **Health Check:** http://localhost:8000/api/health/

---

## 🐛 **حل المشاكل الشائعة**

### **1. "No devices found"**
```bash
# الحل:
# Windows: Run as Administrator
# Linux/Mac: sudo python main.py
```

### **2. "Backend connection failed"**
```bash
# تأكد من:
1. Django Server يشتغل (python manage.py runserver)
2. URL صحيح: http://localhost:8000/api
3. Token صحيح
4. لا يوجد Firewall blocking
```

### **3. "Module not found"**
```bash
pip install -r requirements.txt
```

### **4. "Permission denied" أثناء الفحص**
```bash
# Windows:
# ثبّت Npcap من: https://npcap.com/

# Linux:
sudo apt-get install libpcap-dev
pip install scapy --upgrade

# macOS:
# منح صلاحيات في System Preferences > Security
```

---

## 📊 **التحقق من النجاح**

### **Desktop App:**
- ✅ الواجهة تفتح بدون أخطاء
- ✅ Public IP و Local IP يظهران
- ✅ الفحص يجد أجهزة
- ✅ Backend Status: 🟢 Connected

### **Backend:**
- ✅ السيرفر يشتغل بدون أخطاء
- ✅ Django Admin يفتح
- ✅ API تستجيب: http://localhost:8000/api/health/
- ✅ الأجهزة تظهر في Admin بعد المزامنة

---

## 🎓 **للتطوير والتعديل**

### **إضافة ميزة جديدة في Desktop App:**
1. افتح `main.py`
2. أضف Button في Sidebar
3. أنشئ Function جديدة
4. اربط Button بالـ Function

### **إضافة API Endpoint جديد:**
1. افتح `backend/apps/devices/views.py`
2. أضف `@action` decorator
3. اكتب الـ Function
4. اختبر على: http://localhost:8000/api/devices/{endpoint}/

---

## 📚 **الخطوات التالية**

بعد ما تشتغل كل شي:

1. **اقرأ README.md الشامل** لفهم المشروع كامل
2. **جرّب جميع المزايا** في Desktop App
3. **اطّلع على Django Admin** وشوف البيانات
4. **اقرأ الكود** وفهم كيف يعمل
5. **ابدأ التطوير والإضافة** للمشروع

---

## 📧 **محتاج مساعدة؟**

إذا واجهتك أي مشكلة:
1. راجع قسم "حل المشاكل" أعلاه
2. اقرأ الأخطاء بتمعن
3. ابحث عن الخطأ في Google
4. افتح Issue في GitHub

---

**بالتوفيق! 🎉**

المشروع جاهز وكامل للاستخدام كمشروع تخرج!
