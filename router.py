import socket
import threading
import pickle
import random
messages = []

conn = None
KEY = None

def send_message(data):
    global KEY
    global conn

    try:
        encoded = pickle.dumps(data)

        for i in range(1, KEY):
            encoded = encoded + str(i)
        conn.send(encoded)

        messages.append(data)

    except Exception as e:
        print("Send Error:", e)


def receive_messages():
    global KEY
    global conn

    while True:
        try:
            data = conn.recv(4096)

            if data:
                decoded = pickle.loads(data)

                messages.append(decoded)

        except Exception as e:
            print("Receive Error:", e)
            break


def start_as_server(name, ip, port):
    global KEY
    global conn

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((ip, int(port)))

    server.listen(1)

    KEY = random.randint(10000, 99999)
    conn, addr = server.accept()

    threading.Thread(
        target=receive_messages,
        daemon=True
    ).start()


def start_as_client(name, ip, port):
    global KEY
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