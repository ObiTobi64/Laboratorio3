import socket
import threading

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode().strip()
            print(f"[{addr}] {message}")

            if message.startswith("PUT"):
                response = "PUT received and processed."
            elif message == "GET_COUNT":
                response = "Stateless server: I don’t track your PUTs."
            else:
                response = "Unknown command"

            conn.sendall(response.encode())

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", port))
    server.listen()

    print(f"[STARTING] Stateless Server on port {port}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server(12347)

