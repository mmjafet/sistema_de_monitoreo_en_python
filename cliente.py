import socket
import tkinter as tk
from PIL import Image, ImageTk
import io

def start_screen_monitoring_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    def update_image():
        try:
            # Recibir el tamaño de la imagen
            size_data = client_socket.recv(4)
            if not size_data:
                return
            size = int.from_bytes(size_data, byteorder='big')

            # Recibir la imagen
            image_data = b''
            while len(image_data) < size:
                packet = client_socket.recv(size - len(image_data))
                if not packet:
                    return
                image_data += packet

            # Verificar si la imagen se recibió completamente
            if len(image_data) == size:
                # Mostrar la imagen
                image = Image.open(io.BytesIO(image_data))
                photo = ImageTk.PhotoImage(image)
                label.config(image=photo)
                label.image = photo

            # Actualizar la imagen en la interfaz cada 100 ms
            root.after(100, update_image)
        except Exception as e:
            print(f"Error: {e}")

    # Crear la interfaz gráfica
    root = tk.Tk()
    root.title("Monitoreo de Pantalla Remota")

    label = tk.Label(root)
    label.pack()

    # Iniciar la actualización de la imagen
    root.after(100, update_image)
    root.mainloop()

    client_socket.close()

def connect_to_server():
    host = ip_entry.get()
    port = int(port_entry.get())
    connect_window.destroy()  # Cerrar la ventana de conexión antes de iniciar la recepción
    start_screen_monitoring_client(host, port)

# Crear la interfaz para ingresar la IP y el puerto
connect_window = tk.Tk()
connect_window.title("Conectar al Servidor")

tk.Label(connect_window, text="IP del Servidor:").pack()
ip_entry = tk.Entry(connect_window)
ip_entry.pack()

tk.Label(connect_window, text="Puerto:").pack()
port_entry = tk.Entry(connect_window)
port_entry.pack()

connect_button = tk.Button(connect_window, text="Conectar", command=connect_to_server)
connect_button.pack()

connect_window.mainloop()