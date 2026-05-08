import socket
import threading
import os

HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', 5000))


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

clients = []

print("Server started...")

def broadcast(message, client):
    for c in clients:
        if c != client:
            c.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:  # لو الرسالة فاضية
                break
            broadcast(message, client)
        except:
            clients.remove(client)
            client.close()
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        clients.append(client)

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
