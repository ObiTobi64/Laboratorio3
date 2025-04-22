import socket
import threading
from controller import process_command

HOST = '0.0.0.0'
PORT = 12345

def handle_client(conn, addr):
    print(f"[+] Conexión establecida desde {addr}")
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                command = data.decode().strip()
                print(f"[{addr}] Comando recibido en el servidor: {command}")
                response = process_command(command)
                conn.sendall(response.encode())
            except Exception as e:
                print(f"[!] Error con {addr}: {e}")
                break
    print(f"[-] Conexión cerrada con {addr}")

def start_server():
    print(f"[*] Servidor escuchando en {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == '__main__':
    start_server()
