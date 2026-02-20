# Smart Network Guardian - Setup Walkthrough

## ✅ Completed Setup
I have successfully set up and launched both components of your project:

1.  **Backend Server (Django)**
    *   Running at: `http://127.0.0.1:8000`
    *   Admin Panel: `http://127.0.0.1:8000/admin`
    *   Database: Initialized with all migrations applied.

2.  **Desktop Application**
    *   Status: **Running** 🟢
    *   Dependencies: All installed.
    *   **Features Implemented**: 
        *   ✅ Real-time Traffic Monitoring
        *   ✅ Port Scanning
        *   ✅ Device Export (CSV) & Report Generation (TXT)
        *   ✅ Threat Viewing & Log Management
        *   ✅ Backend Sync & Integration

## 🚀 How to Run (if restarted)

### 1. Start Backend
Open a terminal in `backend` folder:
```powershell
cd backend
python manage.py runserver
```

### 2. Start Desktop App
Open a new terminal in `desktop_app` folder:
```powershell
cd desktop_app
python main.py
```

## ⚠️ Important Note: Network Scanning
The app uses **Scapy** for advanced network scanning. On Windows, this requires **Npcap** to work fully.
*   **Current Status**: The app is running, but you saw a warning: `WARNING: No libpcap provider available`.
*   **Impact**: Features like ARP Scan might be limited. The app will fallback to "Ping Sweep" which works fine without Npcap.
*   **Fix**: If you want full scanning capabilities, download and install [Npcap](https://npcap.com/#download) (select "Install Npcap in WinPcap API-compatible Mode").

## 🔗 Connection
The Desktop App is configured to connect to `http://localhost:8000/api`.

### How to Connect (First Time)
1.  Launch the Desktop App.
2.  Click the **Connect** button in the top right corner.
3.  Enter the credentials:
    *   **Username**: `admin`
    *   **Password**: `admin`
4.  Once connected, the status will turn **Green** 🟢 and your scan data will automatically sync to the backend database.

## 🛠️ Troubleshooting
*   **Failed to Connect?**: Make sure the backend terminal is running `python manage.py runserver`.
*   **No Devices Found?**: Try running "Quick Scan" again after connecting.
*   **Warning: No libpcap**: This is normal on Windows without Npcap. The app is using fallback mode (Ping Sweep + Psutil) which is sufficient for the demo.
