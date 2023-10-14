import socket

def send_file(client_socket, file_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()
        file_size = len(file_data)
        client_socket.send(f"{file_size:<{HEADER_SIZE}}".encode('utf-8'))
        client_socket.sendall(file_data)

HEADER_SIZE = 10
SERVER = "127.0.0.1"
PORT = 9999
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print("[*] Connected to server")

action = input("Enter 'message' to send a message or 'file' to send a file: ")

if action == "message":
    message = input("Enter your message: ")
    client.send(f"{len(message):<{HEADER_SIZE}}".encode('utf-8'))
    client.send(message.encode('utf-8'))
elif action == "file":
    file_path = input("Enter the path to the file: ")
    client.send(f"{len('FILE_TRANSFER'):<{HEADER_SIZE}}".encode('utf-8'))
    client.send("FILE_TRANSFER".encode('utf-8'))
    send_file(client, file_path)

client.close()
