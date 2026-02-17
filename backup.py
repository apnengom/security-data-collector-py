import sqlite3
from database.db import DB_PATH # Aprovechamos tu ruta blindada

def hacer_backup():
    try:
        conn = sqlite3.connect(str(DB_PATH))
        with open('backup_seguridad.sql', 'w') as f:
            for linea in conn.iterdump():
                f.write('%s\n' % linea)
        print(f"[+] Backup realizado con éxito en backup_seguridad.sql")
        conn.close()
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    hacer_backup()