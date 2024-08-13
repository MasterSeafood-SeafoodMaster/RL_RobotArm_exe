
import socket
from moveLib import movementManager
mm=movementManager()
ht={"aim":mm.aim, "grab": mm.try2grab, "reset":mm.reset}

HOST = '192.168.137.116'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Server is listening on", PORT)
    conn, addr = server_socket.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                conn.sendall(b"no Data")
                break
            
            conn.sendall(b"Executing")
            cmd=data.decode().replace(" ", "")
            cmd_list=cmd.split(",")
            
            for c in cmd_list:
                if c[0:3]=="aim":
                    print(c[4:-2])
                    ht["aim"](c[4:-1])
                else:
                    ht[c]()
            conn.sendall(b"Server received: " + data)
            mm.reset()
            conn.sendall(b"Execution ends")
            
