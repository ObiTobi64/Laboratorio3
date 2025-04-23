import socket
import threading
import sys

# Mapeo estático de códigos UPB a IP:puerto (puedes modificar según pruebas)
PEER_MAP = {
    "69017": ("127.0.0.1", 5001),
    "70835": ("127.0.0.1", 5002),
    "70419": ("127.0.0.1", 5003),
    "64931": ("127.0.0.1", 5004),
}

local_store = {}
BUFFER_SIZE = 1024

def start_server(my_ip, my_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((my_ip, my_port))
    server.listen()

    print(f"[SERVIDOR] Escuchando en {my_ip}:{my_port}...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,))
        thread.daemon = True
        thread.start()

def handle_client(conn):
    try:
        data = conn.recv(BUFFER_SIZE).decode().strip()
        if data.startswith("GET_P2P"):
            _, key = data.split(maxsplit=1)
            value = local_store.get(key, None)
            if value is not None:
                conn.sendall(f"VALOR {value}".encode())
            else:
                conn.sendall("ERROR Clave no encontrada".encode())
    except Exception as e:
        print(f"[ERROR] Al procesar conexión entrante: {e}")
    finally:
        conn.close()

def get_remote(codigo_upb_peer, clave_remota):
    if codigo_upb_peer not in PEER_MAP:
        print(f"[ERROR] Peer {codigo_upb_peer} desconocido")
        return

    ip, port = PEER_MAP[codigo_upb_peer]
    print(f'found this map\n{PEER_MAP}')
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.sendall(f"GET_P2P {clave_remota}".encode())
            response = s.recv(BUFFER_SIZE).decode()
            print(f"[RESPUESTA REMOTA] {response}")
    except Exception as e:
        print(f"[ERROR] No se pudo contactar al peer {codigo_upb_peer}: {e}")

def main():
    if len(sys.argv) != 4:
        print("Uso: python peer_p5.py <codigo_upb> <mi_ip> <mi_puerto>")
        return

    my_code = sys.argv[1]
    my_ip = sys.argv[2]
    my_port = int(sys.argv[3])

    # Iniciar servidor en hilo separado
    server_thread = threading.Thread(target=start_server, args=(my_ip, my_port))
    server_thread.daemon = True
    server_thread.start()

    print(f"[INFO] Peer {my_code} iniciado. Escribe comandos:")

    while True:
        try:
            cmd = input(">>> ").strip()
            if cmd.startswith("PUT_LOCAL"):
                _, key, value = cmd.split(maxsplit=2)
                local_store[key] = value
                print(f"[OK] Guardado localmente: {key} -> {value}")

            elif cmd.startswith("GET_LOCAL"):
                _, key = cmd.split(maxsplit=1)
                value = local_store.get(key)
                if value:
                    print(f"[OK] {key} => {value}")
                else:
                    print("[ERROR] Clave no encontrada")

            elif cmd.startswith("GET_REMOTE"):
                _, codigo_upb_peer, clave_remota = cmd.split(maxsplit=2)
                get_remote(codigo_upb_peer, clave_remota)

            elif cmd in ("exit", "quit"):
                print("Saliendo...")
                break

            else:
                print("[COMANDO NO RECONOCIDO] Usa PUT_LOCAL, GET_LOCAL o GET_REMOTE")

        except KeyboardInterrupt:
            print("\nInterrumpido. Saliendo...")
            break
        except Exception as e:
            print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()

