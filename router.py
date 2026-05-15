import socket
import threading
import pickle
import random

messages = []

conn = None
KEY = None
FirstM = False


def send_message(data):
    global conn
    global KEY
    try:
        encoded = pickle.dumps(data)

        size = len(encoded).to_bytes(4, "big")

        conn.sendall(size + encoded)

        messages.append(data)

    except Exception as e:
        print("Send Error:", e)


def receive_messages():
    global conn
    global KEY
    while True:

        try:

            raw_size = conn.recv(4)

            if not raw_size:
                break

            size = int.from_bytes(raw_size, "big")

            data = b""

            while len(data) < size:

                packet = conn.recv(4096)

                if not packet:
                    break

                data += packet

            decoded = pickle.loads(data)

            messages.append(decoded)

        except Exception as e:
            print("Receive Error:", e)
            break


def start_as_server(name, ip, port):
    global conn
    global KEY
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((ip, int(port)))

    server.listen(1)

    print("Server started")

    conn, addr = server.accept()

    threading.Thread(
        target=receive_messages,
        daemon=True
    ).start()


def start_as_client(name, ip, port):
    global conn

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((ip, int(port)))

    conn = client

    threading.Thread(
        target=receive_messages,
        daemon=True
    ).start()


def start(ip, port, name, mode):

    if mode == "Client":
        start_as_client(name, ip, port)

    elif mode == "Server":
        start_as_server(name, ip, port)
