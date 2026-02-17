# security/detector.py

class AnalizadorPayload: # Nombre en CamelCase (estándar Python)
    def __init__(self):
        # Las firmas son estáticas, no necesitan cambiar por cada análisis
        self.signatures = {
            "XSS": ["<SCRIPT>", "ALERT(", "ONERROR"],
            "PATH TRANSVERSAL": ["../", "/ETC/PASSWD", "/ETC/SHADOW"],
            "SQL INJECTION": ["SELECT", "DROP", "UNION", "OR 1=1", "--"],
            "WEB SHELL": ["CMD=", "SHELL", "BASH"]
        }

    def analizar(self, data_input): # Recibe la data por argumento
        data_up = str(data_input).upper()
        
        for categoria, patrones in self.signatures.items():
            if any(p in data_up for p in patrones):
                return {
                    "tipo": categoria,
                    "es_ataque": True,
                    "severidad": 8 # Podrías escalar esto según la categoría
                }
        
        return {"es_ataque": False, "tipo": None, "severidad": 0}