import socket
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os

# Función para iniciar el servidor
def start_server():
    host = socket.gethostbyname(socket.gethostname())  # Obtener IP local
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    text_area.insert(tk.END, f"Servidor iniciado en IP: {host}, puerto: {port}\n")

    while True:
        client_socket, addr = server_socket.accept()
        text_area.insert(tk.END, f"Cliente conectado desde {addr}\n")
        threading.Thread(target=receive_file, args=(client_socket,)).start()

# Función para recibir archivos
def receive_file(sock):
    while True:
        try:
            header = sock.recv(1024).decode()  # Recibimos el encabezado
            if header == "FILE":
                filename = sock.recv(1024).decode()  # Recibimos el nombre del archivo
                filename = filename.replace("\n", "").replace("\r", "")  # Limpiar caracteres no válidos
                print(f"Recibiendo archivo: {filename}")
                with open(f"recibido_{filename}", "wb") as f:
                    while True:
                        data = sock.recv(1024)  # Recibimos los datos binarios
                        if data == b"EOF":
                            break
                        f.write(data)  # Escribimos los datos binarios en el archivo
                text_area.insert(tk.END, f"Archivo recibido: {filename}\n")
        except Exception as e:
            text_area.insert(tk.END, f"Error recibiendo archivo: {e}\n")
            break

# Función para enviar archivo
def send_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        filename = os.path.basename(filepath)
        target_socket = client_socket if role.get() == "Cliente" else server_socket
        if target_socket:
            try:
                target_socket.sendall("FILE".encode())
                target_socket.sendall(filename.encode())  # Enviar el nombre del archivo
                with open(filepath, "rb") as f:
                    while (chunk := f.read(1024)):  # Leer el archivo en bloques de 1024 bytes
                        target_socket.sendall(chunk)  # Enviar los bloques de datos
                target_socket.sendall("EOF".encode())  # Enviar un marcador de fin
                text_area.insert(tk.END, f"Archivo enviado: {filename}\n")
            except Exception as e:
                text_area.insert(tk.END, f"Error enviando archivo: {e}\n")
        else:
            messagebox.showwarning("Advertencia", "No hay conexión establecida para enviar el archivo.")

# Función para iniciar como servidor
def start_as_server():
    global server_socket
    threading.Thread(target=start_server, daemon=True).start()

# Función para conectar como cliente
def connect_to_server():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host_entry.get(), port))
        text_area.insert(tk.END, f"Conectado al servidor {host_entry.get()}:{port}\n")
        threading.Thread(target=receive_file, args=(client_socket,)).start()
        return client_socket
    except Exception as e:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar al servidor: {e}")

# Función para iniciar como cliente
def start_as_client():
    global client_socket
    client_socket = connect_to_server()

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Transferencia de Archivos Bidireccional")

# Área de texto para mostrar mensajes
text_area = scrolledtext.ScrolledText(root, width=50, height=20)
text_area.pack(padx=20, pady=20)

# Botón para enviar archivo
file_button = tk.Button(root, text="Enviar Archivo", command=send_file)
file_button.pack(pady=5)

# Opciones de rol (Servidor/Cliente)
role = tk.StringVar(value="Servidor")
tk.Radiobutton(root, text="Servidor", variable=role, value="Servidor", command=start_as_server).pack(anchor="w")
tk.Radiobutton(root, text="Cliente", variable=role, value="Cliente", command=start_as_client).pack(anchor="w")

# Campo para ingresar la dirección IP del servidor
tk.Label(root, text="Dirección IP del Servidor:").pack()
host_entry = tk.Entry(root, width=15)
host_entry.insert(0, "127.0.0.1")  # Cambiar según la IP del servidor si es necesario
host_entry.pack()

# Puerto para la conexión
port = 12345

# Ejecutar la interfaz gráfica
root.mainloop()