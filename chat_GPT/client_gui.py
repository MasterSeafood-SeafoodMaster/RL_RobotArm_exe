from gui import GUI

import socket

HOST = '192.168.137.116'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    gui=GUI(client_socket)

