import threading
import socket

messages = []
conn = None


def send_message(msg, name):
    global conn
    try:
        conn.send(msg.encode())
        messages.append(f"{name}: {msg}")
    except Exception as e:
        print("Send error:", e)


def start_as_server(name, ip, port):
    global conn

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, int(port)))
    server.listen(1)

    conn, addr = server.accept()

    client_name = conn.recv(1024).decode()
    conn.send(name.encode())

    def receive():
        while True:
            try:
                msg = conn.recv(1024).decode()
                if not msg:
                    break
                messages.append(f"{client_name}: {msg}")
            except:
                break

    threading.Thread(target=receive, daemon=True).start()


def start_as_client(name, ip, port):
    global conn

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, int(port)))

    client.send(name.encode())
    server_name = client.recv(1024).decode()

    conn = client

    def receive():
        while True:
            try:
                msg = client.recv(1024).decode()
                if not msg:
                    break
                messages.append(f"{server_name}: {msg}")
            except:
                break

    threading.Thread(target=receive, daemon=True).start()


def start(ip, port, name, mode):
    if mode == "Client":
        start_as_client(name, ip, port)
    elif mode == "Server":
        start_as_server(name, ip, port)