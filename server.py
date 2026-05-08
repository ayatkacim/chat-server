import socket, threading, struct, os

HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', 5000))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

clients = []
print("Server started...")

def recv_frame(sock):
    header = b""
    while len(header) < 4:
        chunk = sock.recv(4 - len(header))
        if not chunk:
            raise ConnectionError("disconnected")
        header += chunk
    (length,) = struct.unpack("!I", header)
    data = b""
    while len(data) < length:
        chunk = sock.recv(min(8192, length - len(data)))
        if not chunk:
            raise ConnectionError("disconnected")
        data += chunk
    return header + data

def broadcast(frame, sender):
    dead = []
    for c in clients:
        if c != sender:
            try:
                c.sendall(frame)
            except:
                dead.append(c)
    for c in dead:
        clients.remove(c)
        c.close()

def handle(client):
    while True:
        try:
            frame = recv_frame(client)
            broadcast(frame, client)
        except:
            if client in clients:
                clients.remove(client)
            client.close()
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected: {address}")
        clients.append(client)
        threading.Thread(target=handle, args=(client,), daemon=True).start()

receive()
