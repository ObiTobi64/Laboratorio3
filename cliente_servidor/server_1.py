import socket
import threading

HOST = '0.0.0.0'  # Acepta conexiones externas
PORT = 12345

data_store = {}  # Diccionario global para almacenar pares clave-valor
lock = threading.Lock()  # Para evitar condiciones de carrera

def handle_client(conn, addr):
    print(f"[+] Conexión establecida desde {addr}")
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                command = data.decode().strip()
                print(f"[{addr}] Comando recibido: {command}")
                response = process_command(command)
                conn.sendall(response.encode())
            except Exception as e:
                print(f"[!] Error con {addr}: {e}")
                break
    print(f"[-] Conexión cerrada con {addr}")

def process_command(command):
    parts = command.split()
    if len(parts) == 0:
        return "ERROR"
    cmd = parts[0].upper()

    if cmd == "PUT" and len(parts) >= 3:
        key = parts[1]
        value = " ".join(parts[2:])
        with lock:
            data_store[key] = value
        return "OK"
    elif cmd == "GET" and len(parts) == 2:
        key = parts[1]
        with lock:
            return data_store.get(key, "ERROR")
    else:
        return "ERROR"

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
