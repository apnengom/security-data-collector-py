import re # Librería de Expresiones Regulares
import sys
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import threading
import queue # <--- LIBRERÍA ESTÁNDAR PARA HILOS SEGUROS
from client.network_client import NetworkClient

class AppRegistro(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.cerrar_seguro)
        self._esta_viva = True
        self.net_service = NetworkClient()
        
        # COLA DE COMUNICACIÓN
        self.cola_mensajes = queue.Queue()
        
        self.title("Acceso Seguro - Registro")
        self.geometry("400x450")
        
        # ... (Tus elementos de UI se mantienen igual)
        self.etiqueta = ctk.CTkLabel(self, text="Registro de Usuario", font=("Arial", 22))
        self.etiqueta.pack(pady=20)
        self.ent_name = ctk.CTkEntry(self, placeholder_text="Nombre", width=250)
        self.ent_name.pack(pady=10)
        self.ent_email = ctk.CTkEntry(self, placeholder_text="Email", width=250)
        self.ent_email.pack(pady=10)
        self.ent_pass = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=250)
        self.ent_pass.pack(pady=10)
        self.boton = ctk.CTkButton(self, text="Confirmar Registro", command=self.iniciar_registro)
        self.boton.pack(pady=20)
        self.btn_ir_login = ctk.CTkButton(self, text="Ir a Login", fg_color="transparent", command=self.abrir_login)
        self.btn_ir_login.pack()
        
        self.callback_navegar = None

        # INICIAMOS EL MONITOR DE LA COLA
        self.revisar_cola()

    def revisar_cola(self):
        """Este método corre SIEMPRE en el hilo principal y revisa si hay mensajes"""
        if not self._esta_viva:
            return
            
        try:
            # Intentamos sacar un mensaje de la cola sin bloquear
            while True:
                exito, mensaje = self.cola_mensajes.get_nowait()
                if exito:
                    self.notificar_exito()
                else:
                    self.notificar_error(mensaje)
                self.cola_mensajes.task_done()
        except queue.Empty:
            pass
        
        # Revisamos de nuevo en 100ms
        self.after(100, self.revisar_cola)

    def iniciar_registro(self):
        u, e, p = self.ent_name.get().strip(), self.ent_email.get().strip(), self.ent_pass.get()
        
        # 1. Filtro de longitud (Evita ataques de denegación de servicio por strings gigantes)
        if len(u) < 3 or len(p) < 6:
            self.notificar_error("Usuario min. 3 y Password min. 6 caracteres")
            return

        # 2. Filtro de Email (Regex estándar de Blue Team)
        patron_email = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
        if not re.match(patron_email, e.lower()):
            self.notificar_error("Formato de correo electrónico inválido")
            return

        # 3. Filtro de caracteres prohibidos (Evita inyecciones básicas)
        if any(char in u for char in ["'", '"', ";", "--"]):
            self.notificar_error("El nombre contiene caracteres no permitidos")
            return

        self.boton.configure(state="disabled")
        threading.Thread(target=self._proceso_registro, args=(u, e, p), daemon=True).start()
    def _proceso_registro(self, n, e, p):
        try:
            # 1. Obtener respuesta del servicio de red
            status, data = self.net_service.registrar_usuario(n, e, p)
            
            # 2. Análisis de Status Code
            if status == 201:
                self.cola_mensajes.put((True, "Registro exitoso"))
            
            elif status in [400, 409]:
                # Extraemos el mensaje real enviado por Flask
                # Usamos la misma variable para evitar NameError
                msg_servidor = data.get("message", "Error de validación o duplicado")
                self.cola_mensajes.put((False, msg_servidor))
            
            else:
                self.cola_mensajes.put((False, f"Respuesta inesperada: {status}"))

        except Exception as e:
            # Esto SOLO debería activarse si falla la red o el JSON está corrupto
            self.cola_mensajes.put((False, f"Error en la comunicación: {str(e)}"))

    def notificar_exito(self):
        self.boton.configure(state="normal")
        msg = CTkMessagebox(title="Éxito", message="Registrado correctamente", icon="check")
        if msg.get():
            self.after(100, self.abrir_login)

    def notificar_error(self, mensaje):
        self.boton.configure(state="normal")
        CTkMessagebox(title="Error", message=mensaje, icon="cancel")

    def abrir_login(self):
        self.destroy()
        if self.callback_navegar: self.callback_navegar()

    def cerrar_seguro(self):
        try:
            # 1. CANCELAR tareas pendientes (esto elimina el "check_dpi_scaling")
            for after_id in self.tk.call('after', 'info'):
                self.after_cancel(after_id)
            
            # 2. Detener el ciclo y ocultar
            self.quit()
            self.withdraw()
            
            # 3. Destrucción
            self.destroy()
            
        except Exception:
            pass
        
        sys.stdout.flush()