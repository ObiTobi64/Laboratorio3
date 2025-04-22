import socket
import threading

# Diccionario para guardar estado por cliente
client_state = {}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    client_key = f"{addr[0]}:{addr[1]}"
    client_state[client_key] = client_state.get(client_key, 0)

    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode().strip()
            print(f"[{addr}] {message}")

            if message.startswith("PUT"):
                client_state[client_key] += 1
                response = f"PUT received. Total PUTs from you: {client_state[client_key]}"
            elif message == "GET_COUNT":
                response = f"Total PUTs from you: {client_state[client_key]}"
            else:
                response = "Unknown command"

            conn.sendall(response.encode())

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 12345))
    server.listen()

    print("[STARTING] Stateful Server on port 12345")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()

