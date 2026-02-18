import sys
import os
# Esto añade la carpeta raíz al camino de búsqueda de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# server.py
from flask import Flask, request, jsonify
from services.auth_service import AuthService
import hashlib

FLASK_PID = os.getpid()

app = Flask(__name__)
auth_service = AuthService()

def generar_huella_cliente():
    user_agent = request.headers.get('User-Agent', 'unknown')
    ip_cliente = request.remote_addr
    return hashlib.sha256(f"{ip_cliente}-{user_agent}".encode()).hexdigest()

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    huella = generar_huella_cliente()
    
    # El servidor delega la lógica y seguridad al AuthService
    success, message = auth_service.registrar_usuario(
        data.get('name'), 
        data.get('password'), 
        data.get('email'),
        request.remote_addr,
        huella
    )
    
    status_code = 201 if success else 400
    return jsonify({"status": "success" if success else "error", "message": message}), status_code

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    huella = generar_huella_cliente()
    
    success, message, user_name = auth_service.login_usuario(
        data.get('email'),
        data.get('password'),
        request.remote_addr,
        huella
    )
    
    status_code = 200 if success else 401
    return jsonify({
        "status": "success" if success else "error",
        "message": message,
        "user": user_name
    }), status_code

if __name__ == "__main__":
    # debug=True es bueno, pero use_reloader=False evita que se bloquee 
    # al detectar archivos de la interfaz.
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)