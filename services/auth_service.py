import bcrypt
from database.repository import UserRepository # Importamos la CLASE
from security.detector import AnalizadorPayload
from datetime import datetime

class AuthService:
    def __init__(self):
        self.detector = AnalizadorPayload()
        # Instanciamos el repositorio. Aquí se fija la ruta DB_PATH una sola vez.
        self.repository = UserRepository() 

    def registrar_usuario(self, name, pwd, email, ip, fingerprint):
        # 1. Seguridad: Analizar si los inputs son ataques
        for campo in [name, email]:
            resultado = self.detector.analizar(campo)
            if resultado['es_ataque']:
                fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Usamos el método del objeto repository
                self.repository.save_attack_attempt(ip, fingerprint, 1, fecha_hora, resultado['tipo'])
                return False, "Ataque detectado y bloqueado"

        # 2. Lógica: Hashear contraseña
        salt = bcrypt.gensalt()
        hashed_pwd = bcrypt.hashpw(pwd.encode('utf-8'), salt)

        # 3. Persistencia: Usamos el método del objeto
        success, message = self.repository.save_user(name, hashed_pwd, email)
        
        return success, message

    def login_usuario(self, email, pwd, ip, fingerprint):
        # 1. Protección proactiva: Analizar si el email es un ataque (SQLi)
        analisis = self.detector.analizar(email)
        if analisis['es_ataque']:
            fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.repository.save_attack_attempt(ip, fingerprint, 1, fecha_hora, analisis['tipo'])
            return False, "Actividad sospechosa bloqueada", None

        # 2. Búsqueda en DB
        user_data = self.repository.get_user_by_email(email)
        
        if not user_data:
            return False, "Credenciales inválidas", None # No revelamos si el email existe o no

        hashed_pwd, nombre = user_data

        # 3. Verificación de Hash
        # bcrypt requiere bytes, por eso usamos .encode()
        if bcrypt.checkpw(pwd.encode('utf-8'), hashed_pwd):
            return True, f"Bienvenido {nombre}", nombre
        else:
            return False, "Credenciales inválidas", None