import socket
import pyautogui
import io
from PIL import Image

# Configuración del servidor
HOST = '0.0.0.0'  # Escucha en todas las interfaces
PORT = 12345

def capture_screen():
    """Captura la pantalla y devuelve una imagen comprimida en bytes."""
    screenshot = pyautogui.screenshot()
    buffer = io.BytesIO()
    screenshot.save(buffer, format="JPEG")
    return buffer.getvalue()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Servidor escuchando en {HOST}:{PORT}")
        conn, addr = server_socket.accept()
        print(f"Cliente conectado desde {addr}")
        with conn:
            while True:
                try:
                    screen_data = capture_screen()
                    # Enviar longitud de la imagen
                    conn.sendall(len(screen_data).to_bytes(4, byteorder='big'))
                    # Enviar los datos de la imagen
                    conn.sendall(screen_data)
                except Exception as e:
                    print(f"Error: {e}")
                    break

if __name__ == "__main__":
    main()