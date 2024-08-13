import socket
import pygame

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)
    print("已连接到服务器")

    pygame.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    try:
        while True:
            pygame.event.pump()
            s=""
            for i in range(4):
                s+=str(round(joystick.get_axis(i), 2))
                s+=","
            
            print(s[0:-1])
            client_socket.sendto(str(s[0:-2]).encode(), server_address)
    except KeyboardInterrupt:
        pass

    client_socket.close()

if __name__ == "__main__":
    HOST = '192.168.100.83'  # 服务器IP地址
    PORT = 12345        # 端口号
    start_client(HOST, PORT)
