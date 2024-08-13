import socket
import threading

def handle_client(client_socket, address):
    print(f"Accepted connection from {address}")
    
    while True:
        data = client_socket.recv(1024)
        if not data:
            print(f"Connection closed by {address}")
            break
        print(f"Received message from {address}: {data.decode()}")
        client_socket.send(data)

    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 5555))
    server_socket.listen(5)
    print("Server started, listening on port 5555")

    while True:
        client_socket, address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()

if __name__ == "__main__":
    start_server()
