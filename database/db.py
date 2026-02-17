# \database\db.py
import sqlite3
import os
from pathlib import Path

# Obtiene la ruta de la carpeta donde está el proyecto
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = os.path.join(BASE_DIR, 'admin_user.db')

def create_db():
    # Conexión al Motor de Datos
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Habilitar soporte de llaves foráneas
    cursor.execute("PRAGMA foreign_keys = ON;")
    # Definición secuencial de tablas (DDL) 
    tablas = [
      # Inserta esto como el primer elemento de tu lista 'tablas'
      '''CREATE TABLE IF NOT EXISTS usuario (
          id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
          nombre TEXT NOT NULL,
          password TEXT NOT NULL,
          email TEXT UNIQUE NOT NULL
      )''',
      '''CREATE TABLE IF NOT EXISTS intento_ataque (
          id_invitado INTEGER PRIMARY KEY AUTOINCREMENT,
          ip_origen TEXT NOT NULL,
          huella_digital TEXT UNIQUE,
          intento_count INTEGER DEFAULT 1,
          ultima_aparicion DATETIME DEFAULT CURRENT_TIMESTAMP,
          detalle TEXT NOT NULL
      )''',
      '''CREATE TABLE IF NOT EXISTS gerencia (
          id_gerente INTEGER PRIMARY KEY AUTOINCREMENT,
          nom_gerencia TEXT NOT NULL,
          area TEXT NOT NULL
      )''',
      
      '''CREATE TABLE IF NOT EXISTS personal (
          id_personal INTEGER PRIMARY KEY AUTOINCREMENT,
          id_gerente INTEGER,
          nombre_empleado TEXT NOT NULL,
          FOREIGN KEY (id_gerente) REFERENCES gerencia(id_gerente)
      )''',
      
      '''CREATE TABLE IF NOT EXISTS reg_evento (
          id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
          descripcion TEXT,
          fecha DATETIME DEFAULT CURRENT_TIMESTAMP
      )''',
      
      '''CREATE TABLE IF NOT EXISTS det_ataque (
          id_ataque INTEGER PRIMARY KEY AUTOINCREMENT,
          tipo_ataque TEXT,
          payload_detectado TEXT,
          severidad INTEGER DEFAULT 5, 
          id_invitado INTEGER,
          id_registro_evento INTEGER,
          FOREIGN KEY (id_invitado) REFERENCES intento_ataque(id_invitado),
          FOREIGN KEY (id_registro_evento) REFERENCES reg_evento(id_evento)
      )''',
      '''CREATE TABLE IF NOT EXISTS regulaciones (
          id_regulacion INTEGER PRIMARY KEY AUTOINCREMENT,
          nombre_normativa TEXT NOT NULL, -- Ej: GDPR, ISO 27001
          descripcion TEXT
      )''',
      '''CREATE TABLE IF NOT EXISTS reg_usuario (
          id_reg_user INTEGER PRIMARY KEY AUTOINCREMENT,
          id_usuario INTEGER NOT NULL,
          ip_reg_usr TEXT NOT NULL,
          fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
          estado_inicial TEXT,
          FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
      )''',
      
      '''CREATE TABLE IF NOT EXISTS act_usuario (
          id_act_user INTEGER PRIMARY KEY AUTOINCREMENT,
          id_usuario INTEGER NOT NULL,
          ip_orig_usr TEXT NOT NULL,
          tipo_actividad TEXT, -- Ej: Login, Update, Logout
          descripcion_detallada TEXT,
          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
      )''',
      # 2. Registro de Regulaciones: Relaciona usuarios con el cumplimiento de normativas
      '''CREATE TABLE IF NOT EXISTS reg_regulaciones (
          id_reg_reg INTEGER PRIMARY KEY AUTOINCREMENT,
          id_usuario INTEGER,
          id_regulacion INTEGER,
          fecha_aceptacion DATETIME DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
          FOREIGN KEY (id_regulacion) REFERENCES regulaciones(id_regulacion)
      )''',

      # 3. Administrativo: Personal de alto nivel que gestiona el sistema
      '''CREATE TABLE IF NOT EXISTS administrativo (
          id_admin INTEGER PRIMARY KEY AUTOINCREMENT,
          id_personal INTEGER,
          nivel_acceso TEXT,
          FOREIGN KEY (id_personal) REFERENCES personal(id_personal)
      )''',

      # 4. Registro Administrativo: Auditoría de acciones de los administradores
      '''CREATE TABLE IF NOT EXISTS reg_administrativo (
          id_reg_admin INTEGER PRIMARY KEY AUTOINCREMENT,
          id_admin INTEGER,
          id_usuario_afectado INTEGER,
          accion_realizada TEXT,
          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (id_admin) REFERENCES administrativo(id_admin),
          FOREIGN KEY (id_usuario_afectado) REFERENCES usuario(id_usuario)
      )'''
    ]

    # Ejecución profesional una por una
    for tabla in tablas:
      try:
          cursor.execute(tabla)
      except sqlite3.Error as e:
          print(f"Error en la creación: {e}")

    conn.commit()
    print("Estructura DDL completada exitosamente.")
    