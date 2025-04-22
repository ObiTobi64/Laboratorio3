import threading

data_store = {}
lock = threading.Lock()

def put(key, value):
    with lock:
        data_store[key] = value
        print(f"[+] Guardando clave valor en storage")
        return "OK"

def get(key):
    with lock:
        print(f"[+] Recuperando valor en storage con clave: {key}")
        return data_store.get(key, "ERROR")
