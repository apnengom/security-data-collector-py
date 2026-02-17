import customtkinter as ctk

class AppDashboard:
    @staticmethod
    def setup_ui(master, nombre_usuario):
        # 1. Limpieza de protocolo: Re-vinculamos el cierre seguro al master
        master.protocol("WM_DELETE_WINDOW", lambda: AppDashboard.cerrar_seguro(master))

        # 2. Sidebar Lateral
        sidebar = ctk.CTkFrame(master, width=140, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(sidebar, text="ROL: ADMIN", text_color="green").pack(pady=20)

        # 3. Contenedor Principal
        main_frame = ctk.CTkFrame(master)
        main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame, 
            text=f"Operator: {nombre_usuario}", 
            font=("Consolas", 24)
        ).pack(pady=10)

        # 4. Monitor de Eventos
        txt_logs = ctk.CTkTextbox(main_frame, width=500, height=200)
        txt_logs.pack(pady=10)
        txt_logs.insert("0.0", ">>> Sistema Iniciado...\n>>> Monitoreo: ACTIVO\n")
        txt_logs.configure(state="disabled")

    @staticmethod
    def cerrar_seguro(master):
        """Finaliza el proceso de raíz sin dejar zombies"""
        try:
            # Cancelar callbacks de Tkinter para evitar errores de hilos
            for after_id in master.tk.call('after', 'info'):
                master.after_cancel(after_id)
            
            master.withdraw()
            master.quit()     # Detiene el mainloop
            master.destroy()  # Destruye la ventana de la RAM

        except Exception as e:
            import os
            # Convertimos e a string para una comparación real
            error_msg = str(e)
            
            # Filtramos el error específico de Tcl que ya conocemos
            if "can't delete Tcl command" not in error_msg:
                print(f"Cierre forzado por error inesperado: {error_msg}")
                # os._exit es más agresivo y efectivo para Blue Team que sys.exit
                os._exit(0)
