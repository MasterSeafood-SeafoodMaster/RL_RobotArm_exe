import socket
import threading

def handle_client(client_socket, client_number):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print("Received from client {}: {}".format(client_number, data))
        if client_number == 1:
            client_socket.sendall(b"Hello from server to Client 1")
        elif client_number == 2:
            client_socket.sendall(b"Hello from server to Client 2")
    client_socket.close()

def main():
    host = '192.168.100.115'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)

    print("Server is listening on {}:{}".format(host, port))

    client_number = 0

    while True:
        client_number += 1
        client_socket, client_address = server_socket.accept()
        print("Connection from:", client_address)
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_number))
        client_handler.start()

if __name__ == "__main__":
    main()
