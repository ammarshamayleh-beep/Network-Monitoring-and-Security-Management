import sqlite3
import os

dbs = ['network_guardian.db', 'desktop_app/network_guardian.db']
for db in dbs:
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        try:
            c.execute("SELECT COUNT(*) FROM devices")
            print(f"{db}: {c.fetchone()[0]} devices")
        except:
            print(f"{db}: no devices table")
        conn.close()
    else:
        print(f"{db}: missing")
