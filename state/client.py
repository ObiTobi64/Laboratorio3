import socket

def start_client(host="localhost", port=12345):
    print(f"Conectando al servidor en {host}:{port}...\n")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        while True:
            cmd = input("Escribe un comando (PUT, GET_COUNT, exit): ").strip()
            if cmd.lower() == "exit":
                print("Cerrando conexión.")
                break

            s.sendall(cmd.encode())
            data = s.recv(1024)
            print(f"Respuesta: {data.decode()}\n")

if __name__ == "__main__":
    print("Cliente de prueba para app_server_p4")
    h = input("Host [localhost]: ").strip() or "localhost"
    p = input("Puerto [12345]: ").strip()
    port = int(p) if p else 12345

    start_client(host=h, port=port)

