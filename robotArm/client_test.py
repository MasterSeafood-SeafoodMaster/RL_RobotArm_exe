import socket

# CircuitPython裝置的IP地址和端口號
server_address = ('192.168.137.85', 5000)

# 建立Socket Client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.connect(server_address)
client_socket.settimeout(5)
# 連接到CircuitPython Socket Server


# 接收來自Server的歡迎訊息
#welcome_message = client_socket.recv(1024)
#print(welcome_message.decode())

# 向Server發送數據
for i in range(100):

	data_to_send = "Hello from PC!"+str(i)
	client_socket.send(data_to_send.encode())
	print("send:", data_to_send)

	msg = client_socket.recv(1024)
	print("get:", msg.decode())

# 關閉連接
client_socket.close()
