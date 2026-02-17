class ControladorNavegacion:
    def __init__(self):
        self.login_window = None
        self.dash_window = None
        self.reg_window = None

    def lanzar_login(ventana_reg=None):
        if ventana_reg:
            ventana_reg.withdraw()
        
        login_app = AppLogin()
        # Configuramos el botón de ir a registro
        if hasattr(login_app, 'btn_ir_reg'):
            self._limpiar()
            login_app.btn_ir_reg.configure(command=lambda: lanzar_registro(login_app))

    def lanzar_registro(ventana_login):
        # Importación local para evitar errores circulares
        from client.interface_reg import AppRegistro
        ventana_login.withdraw() # Ocultamos login
        
        reg_app = AppRegistro()
        # Configuramos el botón de volver en la nueva ventana
        if hasattr(reg_app, 'btn_ir_login'):
            self._limpiar()
            reg_app.btn_ir_login.configure(command=lambda: lanzar_login(reg_app))
        
    def _limpiar(self):
        if self.ventana_actual:
            self.ventana_actual.withdraw()
            self.ventana_actual.destroy()
            self.ventana_actual = None