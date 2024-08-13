import socket

HOST = "192.168.137.243"  # The server's hostname or IP address
PORT = 80  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(5)

    print("Connecting")
    s.connect((HOST, PORT))

    print("Sending")
    s.send(b"Hello, world")

    print("Receiving")
    data = s.recv(1024)
    print("Received", repr(data))