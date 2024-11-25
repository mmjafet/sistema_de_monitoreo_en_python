import socket
import threading
import tkinter as tk
from tkinter import scrolledtext


clients = []  # Lista para almacenar los sockets de los clientes conectados

def create_button(frame, texto, comando):
    button = tk.Button(
        frame,
        text=texto,
        command=comando,
        font=("Sans-Serif", 12, "bold"),
        fg="#ffffff",  # Color del texto
        bg="#282e61",  # Color de fondo del botón
        activebackground="#636cb4",  # Color de fondo cuando el botón está activo
        highlightthickness=0,  # Grosor del contorno
        highlightbackground="#282e61",  # Color del contorno (mismo que el fondo del botón)
        highlightcolor="#282e61"  # Color del contorno al enfocar el botón
    )
    return button

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Obtener la dirección IP local
    host = socket.gethostbyname(socket.gethostname())
    server_socket.bind((host, port))
    server_socket.listen(5)

    # Mostrar IP y puerto en el área de texto
    text_area.insert(tk.END, f"Conéctate a la IP: {host} y el puerto: {port}...\n")

    while True:
        client_socket, addr = server_socket.accept()
        clients.append((client_socket, addr))  # Agregar el nuevo cliente a la lista con su dirección
        text_area.insert(tk.END, f"Conexión establecida con {addr}\n")
        # Manejar la conexión del cliente en un hilo separado
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

def handle_client(client_socket, addr):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            # Mostrar el mensaje recibido en la interfaz
            message = f"Mensaje de {addr}: {data.decode()}\n"
            text_area.insert(tk.END, message)
            text_area.see(tk.END)  # Hacer scroll automático al final

            # Reenviar el mensaje a todos los clientes conectados
            broadcast_message(data, addr)
    except Exception as e:
        text_area.insert(tk.END, f"Error con {addr}: {e}\n")
    finally:
        client_socket.close()
        clients.remove((client_socket, addr))  # Remover el cliente de la lista
        text_area.insert(tk.END, f"Cerrando conexión con {addr}\n")

def broadcast_message(message, sender_addr):
    # Enviar el mensaje a todos los clientes conectados excepto al que lo envió
    for client, addr in clients:
        if addr != sender_addr:
            try:
                # Si el remitente es None (mensaje del servidor), no incluir la dirección del remitente
                if sender_addr is None:
                    formatted_message = message.decode()
                else:
                    formatted_message = f"Cliente {sender_addr}: {message.decode()}"
                
                client.sendall(formatted_message.encode())
            except Exception as e:
                text_area.insert(tk.END, f"Error enviando mensaje: {e}\n")


def start_server_thread():
    # Iniciar el servidor en un hilo separado
    threading.Thread(target=start_server, args=(port,), daemon=True).start()
    text_area.insert(tk.END, "Servidor iniciado...\n")

def send_message():
    message = message_entry.get()
    if message:
        # Enviar el mensaje a todos los clientes conectados
        broadcast_message(message.encode(), None)
        # Mostrar el mensaje enviado en la interfaz del servidor
        text_area.insert(tk.END, f"Tú: {message}\n")
        text_area.see(tk.END)  # Hacer scroll automático al final
        message_entry.delete(0, tk.END)

# Crear la ventana principal
root = tk.Tk()
root.title("Servidor de Chat")
root.configure(bg="#0f1440")

# Crear área de texto para mostrar mensajes
text_area = scrolledtext.ScrolledText(root, width=50, height=20)
text_area.pack(padx=20, pady=20)

# Entrada de texto para enviar mensajes
message_entry = tk.Entry(root, width=40)
message_entry.pack(padx=10, pady=5)

# Botón para enviar mensajes
send_button = create_button(root, "Enviar Mensaje", send_message)
send_button.pack(pady=5)

# Configurar el puerto
port = 12345  # Cambia esto si deseas usar otro puerto

# Botón para iniciar el servidor
start_button = create_button(root, "Iniciar Servidor", start_server_thread)
start_button.pack(pady=10)

# Iniciar el bucle principal de la interfaz
root.mainloop()
