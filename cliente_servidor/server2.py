import socket
import threading
import time

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
                
                # Si process_command devuelve None (simulando timeout), no respondemos nada
                if response is not None:
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

    # Simular cuelgue del servidor (no se responde para forzar timeout en cliente)
    if cmd == "WAIT":
        print("[*] Simulando retraso de 10 segundos...")
        time.sleep(10)
        return None  # No se responde al cliente

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
