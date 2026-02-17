# client/interface_login.py
import os
import sys
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import threading
from client.network_service import NetworkService

class AppLogin(ctk.CTk):
    def __init__(self, on_success):
        super().__init__()
        self.on_sucess = on_success
        self.protocol("WM_DELETE_WINDOW", self.cerrar_seguro)
        self._esta_viva = True
        self.net = NetworkService()
        self.ultimo_resultado = None
        
        self.title("Acceso Seguro - Login")
        self.geometry("400x400")
        
        # UI Elements (Mantengo tus elementos)
        ctk.CTkLabel(self, text="Inicio de Sesión", font=("Arial", 22)).pack(pady=20)
        self.ent_email = ctk.CTkEntry(self, placeholder_text="Email", width=250)
        self.ent_email.pack(pady=10)
        self.ent_pass = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", width=250)
        self.ent_pass.pack(pady=10)

        self.boton = ctk.CTkButton(self, text="Entrar", command=self.iniciar_login)
        self.boton.pack(pady=20)
        
        self.btn_ir_reg = ctk.CTkButton(self, text="Crear cuenta nueva", fg_color="transparent")
        self.btn_ir_reg.pack(pady=10)
        
        self.callback_navegar = None

    def iniciar_login(self):
        e, p = self.ent_email.get(), self.ent_pass.get()
        
        if not e or not p:
            return CTkMessagebox(title="Error", message="Campos vacíos", icon="cancel")
        
        self.boton.configure(state="disabled")
        threading.Thread(target=self._hilo_login, args=(e, p), daemon=True).start()
        
    def _hilo_login(self, e, p):
        status, data = self.net.login(e, p)
        self.ultimo_resultado = (status, data)
        if self._esta_viva:
            # Mandamos la interacción al hilo principal con un ligero delay de seguridad
            self.after(10, self._procesar_login)

    def _procesar_login(self):
        status, data = self.ultimo_resultado
        if status == 200:
            nombre = data.get("user", "Usuario")
            from client.interface_dash import AppDashboard
            
            # 1. Limpieza total de los widgets de Login
            for widget in self.winfo_children():
                widget.destroy()
            
            # 2. Reconfiguración de la ventana actual (Self es la ventana)
            self.title("SOC Terminal - Panel de Control")
            self.geometry("700x500")
            
            # 3. Inyectamos la lógica del Dashboard en la ventana existente
            # Nota: Debes modificar AppDashboard para que pueda recibir un frame o 'self'
            AppDashboard.setup_ui(self, nombre) 
            
        else:
            self.boton.configure(state="normal")
            CTkMessagebox(title="Acceso Denegado", message=data.get("message"), icon="cancel")
    
    def cambiar_frame(self, frame_class, *args):
        if self.frame_actual:
            self.frame_actual.destroy()
        self.frame_actual = frame_class(self, *args)
        self.frame_actual.pack(fill="both", expand=True)
        
    def cerrar_seguro(self):
        try:
            # 1. CANCELAR tareas pendientes (esto elimina el "check_dpi_scaling")
            for after_id in self.tk.call('after', 'info'):
                self.after_cancel(after_id)
            
            # 2. Detener el ciclo y ocultar
            self.withdraw()
            self.quit()
            
            # 3. Destrucción
            self.destroy()
            
        except Exception:
            pass
        
        sys.stdout.flush()

        