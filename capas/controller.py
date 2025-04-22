from storage import put, get

def process_command(command):
    print(f"[+] Comando recibido en el controller: {command}")
    parts = command.split()
    if len(parts) == 0:
        return "ERROR"

    cmd = parts[0].upper()

    if cmd == "PUT" and len(parts) >= 3:
        key = parts[1]
        value = " ".join(parts[2:])
        return put(key, value)
    elif cmd == "GET" and len(parts) == 2:
        key = parts[1]
        return get(key)
    else:
        return "ERROR"
