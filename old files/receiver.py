import socket

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print("等待客户端连接...")
    while True:
        data, client_address = server_socket.recvfrom(1024)
        #print(f"已连接到客户端：{client_address}")
        print("收到客户端消息:", data.decode())

if __name__ == "__main__":
    HOST = '127.0.0.1'  # 服务器IP地址
    PORT = 12345        # 端口号
    start_server(HOST, PORT)
