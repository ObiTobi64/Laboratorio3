import socket

SERVER_IP = '127.0.0.1'  # Cambia esto por la IP real del servidor si se prueba remotamente
PORT = 12345

def main():
    print("[*] Cliente iniciado")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))
        s.settimeout(5.0)  # Timeout de 5 segundos para recibir datos

        while True:
            try:
                command = input("Ingrese comando (PUT/GET): ").strip()
                if command.upper() == "EXIT":
                    print("Saliendo...")
                    break
                s.sendall(command.encode())

                try:
                    response = s.recv(1024)
                    print("Respuesta del servidor:", response.decode())
                except socket.timeout:
                    print("El servidor no respondió en el tiempo esperado (5 segundos).")

            except KeyboardInterrupt:
                print("\nSaliendo...")
                break
            except Exception as e:
                print("Error:", e)
                break

if __name__ == '__main__':
    main()
