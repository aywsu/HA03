import socket
import threading

def handle_client(conn):
    while True:
        msg_length = conn.recv(HEADER_SIZE).decode('utf-8')
        if not msg_length:
            break

        msg_length = int(msg_length.strip())
        data = conn.recv(msg_length).decode('utf-8')

        if data == "FILE_TRANSFER":
            file_size = int(conn.recv(HEADER_SIZE).strip())
            with open('received_file', 'wb') as f:
                bytes_read = 0
                while bytes_read < file_size:
                    bytes_to_read = min(1024, file_size - bytes_read)
                    file_data = conn.recv(bytes_to_read)
                    bytes_read += len(file_data)
                    f.write(file_data)
            print("File received!")
        else:
            print(f"Received message: {data}")

    conn.close()

HEADER_SIZE = 10
SERVER = "127.0.0.1"
PORT = 9999
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)
server.listen()

print(f"[*] Listening on {SERVER}:{PORT}")

while True:
    conn, addr = server.accept()
    print(f"[*] Connection from {addr[0]}:{addr[1]}")
    client_thread = threading.Thread(target=handle_client, args=(conn,))
    client_thread.start()
