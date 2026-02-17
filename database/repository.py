# \database\repository.py

import sqlite3
import os
from sqlite3 import IntegrityError
from pathlib import Path

class UserRepository:
    def __init__(self):
        # Esto calcula la ruta exacta hacia: proyecto/database/admin_user.db
        # Sin importar si estás en Windows (Dell) o Android (Samsung)
        BASE_DIR = Path(__file__).resolve().parent
        self.db_path = BASE_DIR / "admin_user.db"
        # Esto garantiza que si borraste el archivo, se cree con el UNIQUE nuevo
        if not os.path.exists('admin_user.db'):
            print(f"Base de datos no encontrada en: {self.db_path}. Creando...")
            # Importación local para evitar ciclos si es necesario
            from .db import create_db
            create_db()

    def _conectar(self):
        """Método privado para gestionar la conexión"""
        return sqlite3.connect(str(self.db_path))

    def save_user(self, name, hashed_pwd, email):
        conn = self._conectar()
        try:
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO usuario (nombre, password, email) VALUES (?, ?, ?)', 
                (name, hashed_pwd, email)
            )
            conn.commit()
            return True, "Usuario registrado"
        except IntegrityError:
            return False, "El correo electrónico ya está registrado."
        except Exception as e:
            return False, f"Error de DB: {str(e)}"
        finally:
            conn.close()

    def save_attack_attempt(self, ip, fingerprint, count, last, detail):
        conn = self._conectar()
        try:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO intento_ataque (ip_origen, huella_digital, intento_count, ultima_aparicion, detalle)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(huella_digital) DO UPDATE SET
                intento_count = intento_count + 1,
                ultima_aparicion = excluded.ultima_aparicion;
            ''', (ip, fingerprint, count, last, detail))
            conn.commit()
        finally:
            conn.close()
            
    def get_user_by_email(self, email):
        """Busca un usuario y retorna sus datos para validación"""
        conn = self._conectar()
        try:
            cur = conn.cursor()
            # Solo traemos lo estrictamente necesario: password hasheada y nombre
            cur.execute('SELECT password, nombre FROM usuario WHERE email = ?', (email,))
            return cur.fetchone() # Retorna (hash, nombre) o None
        except Exception as e:
            print(f"[!] Usuario no registrado: {e}")
            return None
        finally:
            conn.close()
if __name__ == "__main__":
    user = UserRepository()