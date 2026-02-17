# client/network_client.py
import requests

class NetworkClient:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url

    def registrar_usuario(self, nombre, email, password):
        try:
            payload = {"name": nombre, "email": email, "password": password}
            response = requests.post(f"{self.base_url}/register", json=payload, timeout=10)
            return response.status_code, response.json()
        except Exception as e:
            return 500, {"message": f"Error de red: {str(e)}"}

    def login_usuario(self, email, password):
        try:
            payload = {"email": email, "password": password}
            response = requests.post(f"{self.base_url}/login", json=payload, timeout=10)
            return response.status_code, response.json()
        except Exception as e:
            return 500, {"message": f"Error de red: {str(e)}"}