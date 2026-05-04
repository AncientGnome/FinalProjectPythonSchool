import threading
import socket
def start_as_server(name, ip, port):
    print("Hello, this is the first version of the bench not a lot of function here :/")
    print("You've entered as the server, clients will join to you")


    new_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    new_server.bind((ip, int(port)))
    new_server.listen()

    print("Created")
    conn, add = new_server.accept()
    client = (conn.recv(1024).decode())
    conn.send(name.encode())
    print(client, "\033[33m joined the server, say hi (o~O)/\033[0m")

    def check_new_messages():
        while True:
            message = (conn.recv(1024)).decode()
            print(client, ": ", message)

    def type_new_messages():
        while True:
            message = input()
            conn.send(message.encode())

    thr = threading.Thread(target=check_new_messages)
    thr.start()
    thr2 = threading.Thread(target=type_new_messages)
    thr2.start()


def start_as_client(name, ip, port):
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Hello, this is the first version of the bench not a lot of function here :/")
    print("You've entered as the client, you will will join to server")

    print("Connecting")
    print("Warning, you cannot use other alphabets except english right now")
    socket_server.connect((ip, int(port)))
    socket_server.send(name.encode())

    socket_name = socket_server.recv(1024)
    server_name = socket_name.decode()
    messages = [(port, ip), (name, "you've joined server by name")]

    print(server_name, "\033[33m joined the server, say hi (o~O)/\033[0m")
    messages.append(("\033[33m joined the server, say hi (o~O)/\033[0m", server_name))

    def check_new_messages():
        while True:
            message = (socket_server.recv(1024)).decode()
            print(server_name, ": ", message)
            messages.append((message, server_name))

    def type_new_messages():
        while True:
            message = input()
            if message.find("me: "):
                socket_server.send(message.encode())
                messages.append((message, "me"))

    thr = threading.Thread(target=check_new_messages)
    thr.start()
    thr2 = threading.Thread(target=type_new_messages)
    thr2.start()
def start(ip, port, name,mode):
    if mode == "client":
        start_as_client(name, ip, port)
    elif mode == "server":
        start_as_server(name, ip, port)
