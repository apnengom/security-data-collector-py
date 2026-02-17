# main.py
import sys
from client.interface_login import AppLogin
from client.interface_reg import AppRegistro
from client.app_controller import ControladorNavegacion

if __name__ == "__main__":
    try:
        login_window = AppLogin(None)
        reg_window = AppRegistro()
        
        reg_window.withdraw() # Ocultamos registro al inicio
        
        # Vinculamos funciones de salto
        login_window.btn_ir_reg.configure(command=lambda: [login_window.withdraw(), reg_window.deiconify()])
        reg_window.btn_ir_login.configure(command=lambda: [reg_window.withdraw(), login_window.deiconify()])
        
        # El programa vive aquí:
        login_window.mainloop()
        
    except Exception as e:
        print(f"Error en ejecución: {e}")