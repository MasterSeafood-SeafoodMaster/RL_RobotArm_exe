import socket

def main():
    host = '192.168.100.115'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        message = input("Enter message to send (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        client_socket.sendall(message.encode())

        data = client_socket.recv(1024)
        print("Received from server:", data.decode())

    client_socket.close()

if __name__ == "__main__":
    main()
