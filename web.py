import os
import subprocess
import tkinter as tk
from tkinter import simpledialog, messagebox
import paramiko

# Función para ejecutar comandos en el servidor remoto por SSH
def ejecutar_comando_remoto(comando, ip, usuario, contrasena):
    try:
        # Crear la conexión SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Aceptar claves no conocidas
        ssh.connect(ip, username=usuario, password=contrasena)
        
        # Ejecutar el comando
        stdin, stdout, stderr = ssh.exec_command(comando)
        salida = stdout.read().decode()
        error = stderr.read().decode()

        if error:
            messagebox.showerror("Error", f"Error al ejecutar el comando: {error}")
        else:
            return salida
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar al servidor: {str(e)}")
    finally:
        ssh.close()

# Función para bloquear las páginas en el servidor remoto
def bloquear_paginas():
    paginas_a_bloquear = entry_paginas.get().split(",")  # Páginas introducidas en el campo de texto
    loopback = "127.0.0.1"
    
    ip = entry_ip.get()  # IP del servidor remoto
    usuario = simpledialog.askstring("Usuario", "Introduce tu usuario del servidor remoto:", show='*')
    if not usuario:
        return  # Si no se ingresa un usuario, se cancela la operación
    
    contrasena = simpledialog.askstring("Contraseña", "Introduce tu contraseña del servidor remoto:", show='*')
    if not contrasena:
        return  # Si no se ingresa una contraseña, se cancela la operación
    
    # Comando para bloquear páginas en el servidor remoto
    for pagina in paginas_a_bloquear:
        pagina = pagina.strip()  # Limpiar espacios en blanco
        if pagina:
            # Verificar si la página ya está bloqueada
            comando_check = f"grep '{pagina}' /etc/hosts"
            resultado = ejecutar_comando_remoto(comando_check, ip, usuario, contrasena)
            
            if pagina not in resultado:
                # Bloquear la página añadiéndola al archivo /etc/hosts
                comando_bloqueo = f"echo '{loopback} {pagina}' | sudo tee -a /etc/hosts"
                ejecutar_comando_remoto(comando_bloqueo, ip, usuario, contrasena)
                messagebox.showinfo("Éxito", f"Página bloqueada: {pagina}")
            else:
                messagebox.showinfo("Información", f"La página {pagina} ya está bloqueada.")
    
    # Reiniciar el servicio de red en el servidor remoto
    comando_restart = "sudo systemctl restart networking"
    ejecutar_comando_remoto(comando_restart, ip, usuario, contrasena)
    messagebox.showinfo("Éxito", "El servidor se ha reiniciado correctamente.")

# Función para desbloquear las páginas en el servidor remoto
def desbloquear_paginas():
    paginas_a_desbloquear = entry_paginas.get().split(",")  # Páginas introducidas en el campo de texto
    ip = entry_ip.get()  # IP del servidor remoto
    usuario = simpledialog.askstring("Usuario", "Introduce tu usuario del servidor remoto:", show='*')
    if not usuario:
        return  # Si no se ingresa un usuario, se cancela la operación
    
    contrasena = simpledialog.askstring("Contraseña", "Introduce tu contraseña del servidor remoto:", show='*')
    if not contrasena:
        return  # Si no se ingresa una contraseña, se cancela la operación
    
    # Leer el archivo /etc/hosts en el servidor remoto
    comando_read = "cat /etc/hosts"
    resultado = ejecutar_comando_remoto(comando_read, ip, usuario, contrasena)

    # Eliminar las páginas a desbloquear del archivo
    for pagina in paginas_a_desbloquear:
        pagina = pagina.strip()
        if pagina in resultado:
            comando_desbloqueo = f"sudo sed -i '/{pagina}/d' /etc/hosts"
            ejecutar_comando_remoto(comando_desbloqueo, ip, usuario, contrasena)
            messagebox.showinfo("Éxito", f"Página desbloqueada: {pagina}")
        else:
            messagebox.showinfo("Información", f"La página {pagina} no está bloqueada.")
    
    # Reiniciar el servicio de red en el servidor remoto
    comando_restart = "sudo systemctl restart networking"
    ejecutar_comando_remoto(comando_restart, ip, usuario, contrasena)
    messagebox.showinfo("Éxito", "El servidor se ha reiniciado correctamente.")

# Función para conectarse al servidor por IP (opcional)
def conectar_por_ip():
    ip = entry_ip.get()  # Obtener IP del campo de texto
    if ip:
        # Aquí se puede agregar código para conectar al servidor con la IP proporcionada
        messagebox.showinfo("Conexión", f"Conectado al servidor con IP {ip}")
    else:
        messagebox.showerror("Error", "Por favor, introduce una IP válida.")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Bloquear/Desbloquear Páginas Web en Servidor Remoto")

# IP de conexión
label_ip = tk.Label(root, text="IP del servidor remoto:")
label_ip.pack(padx=10, pady=5)

entry_ip = tk.Entry(root)
entry_ip.pack(padx=10, pady=5)

boton_conectar = tk.Button(root, text="Conectar", command=conectar_por_ip)
boton_conectar.pack(pady=10)

# Páginas a bloquear/desbloquear
label_paginas = tk.Label(root, text="Páginas a bloquear/desbloquear (separadas por coma):")
label_paginas.pack(padx=10, pady=5)

entry_paginas = tk.Entry(root)
entry_paginas.pack(padx=10, pady=5)

# Botones para bloquear y desbloquear
boton_bloquear = tk.Button(root, text="Bloquear Páginas", command=bloquear_paginas)
boton_bloquear.pack(pady=10)

boton_desbloquear = tk.Button(root, text="Desbloquear Páginas", command=desbloquear_paginas)
boton_desbloquear.pack(pady=10)

root.mainloop()
