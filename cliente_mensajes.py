import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

def connect_to_server():
    try:
        global client_socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host_entry.get(), int(port_entry.get())))
        text_area.insert(tk.END, "Conectado al servidor\n")
        # Iniciar un hilo para recibir mensajes del servidor
        threading.Thread(target=receive_messages, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar al servidor: {e}")

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            text_area.insert(tk.END, f"Servidor: {message}\n")
            text_area.see(tk.END)
        except Exception as e:
            text_area.insert(tk.END, f"Error al recibir mensaje: {e}\n")
            break

def send_message():
    message = message_entry.get()
    if message:
        client_socket.sendall(message.encode())
        text_area.insert(tk.END, f"Tú: {message}\n")
        text_area.see(tk.END)
        message_entry.delete(0, tk.END)

# Crear la ventana principal
root = tk.Tk()
root.title("Cliente de Chat")

# Entradas para la IP y el puerto del servidor
tk.Label(root, text="IP del Servidor:").pack(padx=10, pady=5)
host_entry = tk.Entry(root)
host_entry.pack(padx=10, pady=5)
host_entry.insert(0, "127.0.0.1")  # Valor por defecto

tk.Label(root, text="Puerto:").pack(padx=10, pady=5)
port_entry = tk.Entry(root)
port_entry.pack(padx=10, pady=5)
port_entry.insert(0, "12345")  # Valor por defecto

# Área de texto para mostrar mensajes
text_area = scrolledtext.ScrolledText(root, width=40, height=10)
text_area.pack(padx=10, pady=10)

# Entrada para enviar mensajes
message_entry = tk.Entry(root, width=30)
message_entry.pack(padx=10, pady=5)

send_button = tk.Button(root, text="Enviar", command=send_message)
send_button.pack(pady=5)

# Botón para conectarse al servidor
connect_button = tk.Button(root, text="Conectar", command=connect_to_server)
connect_button.pack(pady=10)

root.mainloop()
