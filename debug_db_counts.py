import sqlite3
import os

paths = [
    'network_guardian.db',
    'desktop_app/network_guardian.db',
    'backend/db.sqlite3'
]

for path in paths:
    if os.path.exists(path):
        try:
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [t[0] for t in cursor.fetchall()]
            print(f"File: {path}")
            print(f"  Tables: {tables}")
            if 'devices' in tables:
                cursor.execute("SELECT COUNT(*) FROM devices")
                count = cursor.fetchone()[0]
                print(f"  Devices count: {count}")
                if count > 0:
                    cursor.execute("SELECT ip, mac, status FROM devices LIMIT 3")
                    print(f"  Samples: {cursor.fetchall()}")
            conn.close()
        except Exception as e:
            print(f"File: {path} - Error: {e}")
    else:
        print(f"File: {path} - Not found")
