import tkinter as tk
from tkinter import ttk
import subprocess
import os

def run_script(script_name):
    # Asegúrate de que la ruta del script sea correcta
    script_path = os.path.join(os.getcwd(), script_name)
    try:
        # Ejecutar el script en un nuevo proceso
        subprocess.Popen(['python3', script_path])
    except Exception as e:
        print(f"Error al ejecutar {script_name}: {e}")

def crear_label(texto, frame):
    label = tk.Label(frame, text=texto, font=("Arial", 18, "bold"), fg="#cdd4ea", bg="#0f1440")
    return label

def separator(frame):
    separator_canvas = tk.Canvas(frame, height=5, bg="#bc6fc7", highlightthickness=0)
    separator_canvas.pack(fill="x", padx=10, pady=(0, 10))
    return separator_canvas

def create_frame_horzontal(frame1):
    frame = tk.Frame(frame1, bg="#0f1440")
    return frame

def create_button(frame, texto, script):
    button = tk.Button(
        frame,
        text=texto,
        command=lambda: run_script(script),
        font=("Sans-Serif", 12, "bold"),
        fg="#ffffff",  # Color del texto
        bg="#282e61",  # Color de fondo del botón
        activebackground="#636cb4",  # Color de fondo cuando el botón está activo
        highlightthickness=0,  # Grosor del contorno
        highlightbackground="#282e61",  # Color del contorno (mismo que el fondo del botón)
        highlightcolor="#282e61"  # Color del contorno al enfocar el botón
    )
    return button


# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Monitoreo")
root.configure(bg="#0f1440")  # Fondo con un tono más oscuro

# Frame para centrar los botones
frame_principal = tk.Frame(root, bg="#0f1440")
frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
frame_principal.columnconfigure(0, weight=1)
frame_principal.columnconfigure(1, weight=1)

# Etiqueta de título (centrada en el frame_principal)
title_label = tk.Label(frame_principal, text="SISTEMA DE MONITOREO", font=("Segoe UI", 25, "bold"), fg="#ecf0f1", bg="#0f1440")
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30), sticky="nsew")  # Ocupa ambas columnas

frame = create_frame_horzontal(frame_principal)
frame.grid(row=1, column = 0, padx=10, pady=10,  sticky="nsew")

frame2 = create_frame_horzontal(frame_principal)
frame2.grid(row=1, column = 1 , padx=10, pady=10,  sticky="nsew")

#--------------------- MONITOREO--------------------------
# Subtítulo y separador para la sección de monitoreo
subtitle_label = crear_label("Monitorear", frame)
subtitle_label.pack(pady=(10, 5))  # Espaciado superior e inferior

# Separador
separator(frame)

# Frame para botones de pantallas
frame_pantalla = create_frame_horzontal(frame)
frame_pantalla.pack(pady=(10,30))

# Botones mejorados para ejecutar diferentes scripts
button1 = create_button(frame_pantalla,"Compartir Pantalla(Servidor)","servidor.py")
button1.grid(row=0, column=0, padx=10, ipadx=20, ipady=10)

button2 = create_button(frame_pantalla,"Ver Pantalla Externa(cliente)","cliente.py")
button2.grid(row=0, column=1, padx=10, ipadx=20, ipady=10)

#---------------------CHAT--------------------------
# Subtítulo y separador para la sección de monitoreo
subtitle_label= crear_label("Chatear", frame)
subtitle_label.pack(pady=(10, 5))  # Espaciado superior e inferior

# Separador
separator(frame)

# Frame para botones de pantallas
frame_chat = create_frame_horzontal(frame)
frame_chat.pack(pady=(10,30))

button3 = create_button(frame_chat, "Iniciar Sala de Chat", "servidor_mensajes.py")
button3.grid(row=0, column=0, padx=10, ipadx=20, ipady=10)

button4 = create_button(frame_chat, "Conectar a Sala de Chat", "cliente_mensajes.py")
button4.grid(row=0, column=1, padx=10, ipadx=20, ipady=10)

#---------------------ENVIAR / RECIBIR ARCHIVOS--------------------------
# Subtítulo y separador para la sección de recibir archivos
subtitle_label= crear_label("Recibir / Enviar archivos", frame)
subtitle_label.pack(pady=(10, 5))  # Espaciado superior e inferior

# Separador
separator(frame)

button5 = create_button(frame,"Enviar y recibir archivos", "archivos.py")
button5.pack(pady=10, ipadx=20, ipady=10)


#---------------------APAGAR COMPUTADOR--------------------------
# Subtítulo y separador para la sección de apagar
subtitle_label= crear_label("Apagar computador remoto", frame2)
subtitle_label.pack(pady=(10, 5))  # Espaciado superior e inferior

# Separador
separator(frame2)

button6 = create_button(frame2, "Apagar pc remota", "apagarUbuntu.py")
button6.pack(pady=10, ipadx=20, ipady=10)

#--------------------DENEGAR/PERMITIR PING-------------------------
# Subtítulo y separador para la sección de ping
subtitle_label= crear_label("Denegar / Permitir Ping ", frame2)
subtitle_label.pack(pady=(10, 5))  # Espaciado superior e inferior

# Separador
separator(frame2)

button6 = create_button(frame2, "Ping remoto", "denegarping.py")
button6.pack(pady=10, ipadx=20, ipady=10)


#-----------------BLOQUEA/DESBLOQUEAR MOUSE/ TECLADO-----------------------
# Subtítulo y separador para la sección de acceso a páginas
subtitle_label= crear_label("Controlar mouse / teclado ", frame2)
subtitle_label.pack(pady=(10, 5))  # Espaciado superior e inferior

# Separador
separator(frame2)

#button8 = create_button(frame2, "Ping remoto", "denegarping.py")
#button8.pack(pady=10, ipadx=20, ipady=10)

#-------------------DENEGAR ACCESO A PÁGINAS--------------------------
# Subtítulo y separador para la sección de acceso a páginas
subtitle_label= crear_label("Control de acceso a páginas web ", frame2)
subtitle_label.pack(pady=(10, 5))  # Espaciado superior e inferior

# Separador
separator(frame2)

#button7 = create_button(frame2, "Ping remoto", "denegarping.py")
#button7.pack(pady=10, ipadx=20, ipady=10)


# Ajustar el tamaño de la ventana

# Hacer que la ventana ajuste su tamaño según el contenido
root.update_idletasks()  # Asegura que la ventana haya calculado su tamaño

# Obtener las dimensiones de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Obtener las dimensiones de la ventana (después de que se haya ajustado al contenido)
window_width = root.winfo_width()
window_height = root.winfo_height()

# Calcular las coordenadas para centrar la ventana
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Establecer la geometría de la ventana con las coordenadas calculadas
root.geometry(f"+{x}+{y}")

#root.geometry("500x500")
root.resizable(True, True)

# Iniciar el bucle principal de la interfaz
root.mainloop()
