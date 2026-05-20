import socket
import threading
import pickle
import time
import json
import os

messages = []
conn = None
server = None
conns = []

CHAT_FILE = "chat_history.json"

DISCOVERY_PORT = 54545
DISCOVER_MESSAGE = "LAN_MESSENGER_DISCOVER"
RESPONSE_MESSAGE = "LAN_MESSENGER_RESPONSE"


def clean_for_json(data):
    return {
        "name": data.get("name"),
        "message": data.get("message"),
        "pfp": None
    }


def load_chat():
    global messages

    if os.path.exists(CHAT_FILE):
        try:
            with open(CHAT_FILE, "r", encoding="utf-8") as file:
                messages = json.load(file)
        except:
            messages = []


def save_chat():
    try:
        safe_messages = []

        for msg in messages:
            safe_messages.append(clean_for_json(msg))

        with open(CHAT_FILE, "w", encoding="utf-8") as file:
            json.dump(safe_messages, file, indent=4)

    except Exception as e:
        print("Save Error:", e)


load_chat()


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return socket.gethostbyname(socket.gethostname())


def send_packet(sock, data):
    encoded = pickle.dumps(data)
    size = len(encoded).to_bytes(4, "big")
    sock.sendall(size + encoded)


def receive_exact(sock, size):
    data = b""

    while len(data) < size:
        packet = sock.recv(size - len(data))

        if not packet:
            return None

        data += packet

    return data


def broadcast(data, exclude=None):
    global conns

    dead = []

    for client in conns:
        if client == exclude:
            continue

        try:
            send_packet(client, data)
        except:
            dead.append(client)

    for client in dead:
        if client in conns:
            conns.remove(client)


def send_message(data):
    global conn, conns

    try:
        if conns:
            broadcast(data)

        elif conn:
            send_packet(conn, data)

        messages.append(data)
        save_chat()

    except Exception as e:
        print("Send Error:", e)


def receive_messages(sock, from_client=False):
    while True:
        try:
            raw_size = receive_exact(sock, 4)

            if not raw_size:
                break

            size = int.from_bytes(raw_size, "big")
            data = receive_exact(sock, size)

            if not data:
                break

            decoded = pickle.loads(data)
            messages.append(decoded)
            save_chat()

            if from_client:
                broadcast(decoded, exclude=sock)

        except Exception as e:
            print("Receive Error:", e)
            break

    if sock in conns:
        conns.remove(sock)


def discovery_responder(name, port):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        udp.bind(("", DISCOVERY_PORT))
    except Exception as e:
        print("Discovery Error:", e)
        return

    while True:
        try:
            data, address = udp.recvfrom(1024)

            if data.decode() == DISCOVER_MESSAGE:
                ip = get_local_ip()
                response = f"{RESPONSE_MESSAGE}|{name}|{ip}|{port}"
                udp.sendto(response.encode(), address)

        except Exception as e:
            print("Discovery Receive Error:", e)
            break


def discover_servers(timeout=2):
    found = []
    seen = set()

    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp.settimeout(0.3)

    try:
        udp.sendto(DISCOVER_MESSAGE.encode(), ("255.255.255.255", DISCOVERY_PORT))
    except Exception as e:
        print("Discovery Send Error:", e)

    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            data, address = udp.recvfrom(1024)
            decoded = data.decode()
            if decoded.startswith(RESPONSE_MESSAGE):
                parts = decoded.split("|")

                if len(parts) == 4:
                    name = parts[1]
                    ip = parts[2]
                    port = parts[3]
                    key = f"{ip}:{port}"

                    if key not in seen:
                        seen.add(key)
                        found.append(
                            {
                                "name": name,
                                "ip": ip,
                                "port": port
                            }
                        )

        except socket.timeout:
            pass

        except Exception as e:
            print("Discovery Error:", e)
            break


    udp.close()
    return found


def accept_clients():
    global server, conns

    while True:
        try:
            client, address = server.accept()
            conns.append(client)

            for old_message in messages:
                send_packet(client, old_message)

            threading.Thread(
                target=receive_messages,
                args=(client, True),
                daemon=True
            ).start()

            print("Client connected:", address)

        except Exception as e:
            print("Accept Error:", e)
            break


def start_as_server(name, ip, port):
    global server

    threading.Thread(
        target=discovery_responder,
        args=(name, port),
        daemon=True
    ).start()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, int(port)))
    server.listen()

    print("Server started on", ip, port)

    threading.Thread(
        target=accept_clients,
        daemon=True
    ).start()


def start_as_client(name, ip, port):
    global conn

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, int(port)))

    conn = client

    threading.Thread(
        target=receive_messages,
        args=(client, False),
        daemon=True
    ).start()


def start(ip, port, name, mode):
    if mode == "Client":
        start_as_client(name, ip, port)

    elif mode == "Server":
        start_as_server(name, ip, port)