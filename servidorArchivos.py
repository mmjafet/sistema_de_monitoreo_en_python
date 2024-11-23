import paramiko
from scp import SCPClient
import tkinter as tk
from tkinter import filedialog, messagebox

# Función para seleccionar el archivo a enviar
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo")
    archivo_entry.delete(0, tk.END)
    archivo_entry.insert(0, archivo)

# Función para enviar el archivo (de local a remoto)
def enviar_archivo():
    try:
        # Obtener los valores de los campos de la interfaz
        hostname = ip_entry.get()
        username = usuario_entry.get()
        password = contrasena_entry.get()
        file_path = archivo_entry.get()
        destino = destino_entry.get()

        if not hostname or not username or not password or not file_path or not destino:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        # Establecer la conexión SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)

        # Transferir el archivo usando SCP
        with SCPClient(client.get_transport()) as scp:
            scp.put(file_path, destino)

        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", "El archivo se ha transferido correctamente.")

        # Cerrar la conexión SSH
        client.close()

    except Exception as e:
        messagebox.showerror("Error", f"Hubo un problema: {e}")

# Función para recibir el archivo (de remoto a local)
def recibir_archivo():
    try:
        # Obtener los valores de los campos de la interfaz
        hostname = ip_entry.get()
        username = usuario_entry.get()
        password = contrasena_entry.get()
        archivo_remoto = archivo_entry.get()
        destino_local = destino_entry.get()

        if not hostname or not username or not password or not archivo_remoto or not destino_local:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        # Establecer la conexión SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)

        # Transferir el archivo usando SCP desde remoto a local
        with SCPClient(client.get_transport()) as scp:
            scp.get(archivo_remoto, destino_local)

        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", "El archivo se ha recibido correctamente.")

        # Cerrar la conexión SSH
        client.close()

    except Exception as e:
        messagebox.showerror("Error", f"Hubo un problema: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Transferencia de Archivos por SSH")

# Crear los campos de la interfaz
tk.Label(root, text="Dirección IP de la PC de destino").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
ip_entry = tk.Entry(root, width=30)
ip_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Usuario").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
usuario_entry = tk.Entry(root, width=30)
usuario_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Contraseña").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
contrasena_entry = tk.Entry(root, width=30, show="*")
contrasena_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Seleccionar archivo a enviar/recibir").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
archivo_entry = tk.Entry(root, width=30)
archivo_entry.grid(row=3, column=1, padx=10, pady=5)
seleccionar_button = tk.Button(root, text="Seleccionar archivo", command=seleccionar_archivo)
seleccionar_button.grid(row=3, column=2, padx=10, pady=5)

tk.Label(root, text="Ruta de destino en la PC remota o local").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
destino_entry = tk.Entry(root, width=30)
destino_entry.grid(row=4, column=1, padx=10, pady=5)

# Botones para enviar o recibir archivos
enviar_button = tk.Button(root, text="Enviar archivo", command=enviar_archivo)
enviar_button.grid(row=5, column=0, padx=10, pady=20)

recibir_button = tk.Button(root, text="Recibir archivo", command=recibir_archivo)
recibir_button.grid(row=5, column=1, padx=10, pady=20)

# Iniciar la interfaz gráfica
root.mainloop()
