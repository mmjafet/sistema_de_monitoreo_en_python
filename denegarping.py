import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess

def run_command(command, password):
    # Agregar la contraseña al comando de sudo
    full_command = f"echo {password} | sudo -S {command}"
    try:
        result = subprocess.run(full_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando el comando: {e.stderr.decode()}")

def check_rule_exists(command, password):
    full_command = f"echo {password} | sudo -S {command}"
    try:
        subprocess.run(full_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def allow_ping(ips, password):
    for ip in ips:
        check_command = f"iptables -C INPUT -p icmp --icmp-type echo-request -s {ip} -j DROP"
        if check_rule_exists(check_command, password):
            command = f"iptables -D INPUT -p icmp --icmp-type echo-request -s {ip} -j DROP"
            run_command(command, password)
        
        command = f"iptables -I INPUT -p icmp --icmp-type echo-request -s {ip} -j ACCEPT"
        run_command(command, password)
        print(f"Ping permitido desde la IP {ip}")

def deny_ping(ips, password):
    for ip in ips:
        check_command = f"iptables -C INPUT -p icmp --icmp-type echo-request -s {ip} -j ACCEPT"
        if check_rule_exists(check_command, password):
            command = f"iptables -D INPUT -p icmp --icmp-type echo-request -s {ip} -j ACCEPT"
            run_command(command, password)
        
        command = f"iptables -I INPUT -p icmp --icmp-type echo-request -s {ip} -j DROP"
        run_command(command, password)
        print(f"Ping denegado desde la IP {ip}")

def execute_action(action):
    ip = ip_entry.get()  
    if ip:
        password = simpledialog.askstring("Contraseña", "Ingrese la contraseña de administrador:", show="*")
        if not password:
            messagebox.showerror("Error", "Se requiere una contraseña.")
            return
        
        if action == 'permitir':
            allow_ping([ip], password)
            messagebox.showinfo("Acción completada", f"Ping permitido desde la IP {ip}.")
        elif action == 'denegar':
            deny_ping([ip], password)
            messagebox.showinfo("Acción completada", f"Ping denegado desde la IP {ip}.")
        else:
            messagebox.showerror("Error", "Acción no válida.")
    else:
        messagebox.showerror("Error", "Por favor, ingresa una dirección IP.")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("PINGS")
root.geometry("400x250")

action_label = tk.Label(root, text="¿Quieres permitir o denegar el ping?")
action_label.pack(pady=10)

action_variable = tk.StringVar(root)
action_variable.set("Seleccione la acción")

action_menu = tk.OptionMenu(root, action_variable, "permitir", "denegar")
action_menu.pack(pady=10)

ip_label = tk.Label(root, text="Ingresa la dirección IP:")
ip_label.pack(pady=10)

ip_entry = tk.Entry(root)  
ip_entry.pack(pady=10)

execute_button = tk.Button(root, text="Ejecutar", command=lambda: execute_action(action_variable.get()))
execute_button.pack(pady=10)

root.mainloop()
