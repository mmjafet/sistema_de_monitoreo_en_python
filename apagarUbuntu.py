import paramiko
import tkinter as tk
from tkinter import simpledialog, messagebox

def apagar_computadora():
    # Solicitar detalles de conexión
    ip = simpledialog.askstring("IP del servidor", "Introduce la IP del servidor:")
    username = simpledialog.askstring("Usuario", "Introduce el nombre de usuario:")
    password = simpledialog.askstring("Contraseña", "Introduce la contraseña:", show="*")

    if not ip or not username or not password:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    try:
        # Conexión SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ip, username=username, password=password)

        # Solicitar la contraseña para ejecutar el comando de apagado
        sudo_password = simpledialog.askstring("Contraseña Sudo", "Introduce la contraseña de sudo:", show="*")
        if not sudo_password:
            messagebox.showerror("Error", "La contraseña de sudo es obligatoria.")
            return

        # Ejecutar el comando de apagado
        comando = f"echo {sudo_password} | sudo -S shutdown -h now"
        stdin, stdout, stderr = client.exec_command(comando)

        # Leer posibles errores
        error = stderr.read().decode()
        if error:
            messagebox.showerror("Éxito", f"El comando de apagado se ejecutó correctamente:\n{error}")
        else:
            messagebox.showinfo("Éxito", "El comando de apagado se ejecutó correctamente.")
    except Exception as e:
        messagebox.showerror("Error de conexión", str(e))
    finally:
        client.close()

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Apagar computadora remota por SSH")
root.geometry("300x150")

tk.Label(root, text="Presiona el botón para apagar").pack(pady=20)
tk.Button(root, text="Apagar Computadora", command=apagar_computadora).pack(pady=10)

root.mainloop()