# client/network_service.py
import requests

class NetworkService:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url

    def registrar(self, nombre, email, password):
        try:
            payload = {"name": nombre, "email": email, "password": password}
            response = requests.post(f"{self.base_url}/register", json=payload, timeout=7)
            return response.status_code, response.json()
        except Exception as e:
            return 500, {"message": f"Fallo de conexión: {str(e)}"}

    def login(self, email, password):
        try:
            payload = {"email": email, "password": password}
            response = requests.post(f"{self.base_url}/login", json=payload, timeout=7)
            return response.status_code, response.json()
        except Exception as e:
            return 500, {"message": f"Fallo de conexión: {str(e)}"}