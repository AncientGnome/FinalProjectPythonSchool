import threading
import socket

messages = []
conn, add = None,None
def send_message(msg, name):
    while True:
        conn.send(msg.encode())
        messages.append((msg, name))
def start_as_server(name, ip, port):

    new_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    new_server.bind((ip, int(port)))
    new_server.listen()

    print("Created")
    conn, add = new_server.accept()
    client = (conn.recv(1024).decode())
    conn.send(name.encode())
    def check_new_messages():
        while True:
            message = (conn.recv(1024)).decode()
            messages.append((message, client))


    thr = threading.Thread(target=check_new_messages)
    thr.start()



def start_as_client(name, ip, port):
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    socket_server.connect((ip, int(port)))
    socket_server.send(name.encode())

    socket_name = socket_server.recv(1024)
    server_name = socket_name.decode()


    def check_new_messages():
        while True:
            message = (socket_server.recv(1024)).decode()
            messages.append((message, server_name))



    thr = threading.Thread(target=check_new_messages)
    thr.start()

def start(ip, port, name,mode):
    if mode == "Client":
        start_as_client(name, ip, port)
    elif mode == "Server":
        start_as_server(name, ip, port)
