import socket
import threading
import pickle
import time
import json
from datetime import date

def write_json(data,name):
    with open(name,".json", "w") as file:
        json.dump(data, file, indent=4)

def read_json(name):
    try:
        with open(name,".json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

class Data:
    def __init__(self,data):
        self.data = data
    def to_dict(self):
        return {
            "data": self.data,

        }


datajsonm = read_json()

messages = []
conn = None

DISCOVERY_PORT = 54545
DISCOVER_MESSAGE = "LAN_MESSENGER_DISCOVER"
RESPONSE_MESSAGE = "LAN_MESSENGER_RESPONSE"



def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return socket.gethostbyname(socket.gethostname())


def send_message(data):
    global conn

    try:
        encoded = pickle.dumps(data)
        size = len(encoded).to_bytes(4, "big")
        conn.sendall(size + encoded)
        messages.append(data)

    except Exception as e:
        print("Send Error:", e)


def receive_exact(size):
    global conn

    data = b""

    while len(data) < size:
        packet = conn.recv(size - len(data))

        if not packet:
            return None

        data += packet

    return data


def receive_messages():
    global conn

    while True:
        try:
            raw_size = receive_exact(4)

            if not raw_size:
                break

            size = int.from_bytes(raw_size, "big")
            data = receive_exact(size)

            if not data:
                break

            decoded = pickle.loads(data)
            messages.append(decoded)

        except Exception as e:
            print("Receive Error:", e)
            break


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
            message = data.decode()

            if message == DISCOVER_MESSAGE:
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


def start_as_server(name, ip, port):
    global conn

    threading.Thread(
        target=discovery_responder,
        args=(name, port),
        daemon=True
    ).start()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, int(port)))
    server.listen(1)

    print("Server started on", ip, port)

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