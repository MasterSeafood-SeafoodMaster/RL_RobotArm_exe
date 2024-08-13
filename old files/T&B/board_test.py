from ArmEnv_3D_ori import ArmEnv_3D
import keyboard
import socket

server_address = ('192.168.137.174', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.connect(server_address)

Arm=ArmEnv_3D([0, 5.5, 5.5, 8.5], True)
Arm.target=[0, 0, 19.5]
while True:
    #Arm.angList=[0, 0, 0, 0]
    Arm.gradient_policy(1000, 2)
    
    if keyboard.is_pressed('esc'):
        break
    elif keyboard.is_pressed('i'):
        Arm.target[0] += 1
    elif keyboard.is_pressed('k'):
        Arm.target[0] -= 1
    elif keyboard.is_pressed('j'):
        Arm.target[1] += 1
    elif keyboard.is_pressed('l'):
        Arm.target[1] -= 1
    elif keyboard.is_pressed('u'):
        Arm.target[2] += 1
    elif keyboard.is_pressed('o'):
        Arm.target[2] -= 1

    Arm.updatePicture()
    int_angList = [int(num)+90 for num in Arm.angList]
    int_angList[0]=180-int_angList[0]
    int_angList[2]=180-int_angList[2]
    data_to_send=str(int_angList)
    client_socket.send(data_to_send.encode())
    msg = client_socket.recv(1024)
    print("get:", msg.decode())
    #ser.write(bytes(int_angList))

"""
import serial

# 初始化串口通信
ser = serial.Serial('COM3', 9600)  # 将'COM3'更改为您的CircuitPython板的串口

# 发送数据
ser.write(b'Hello from computer!')

# 关闭串口
ser.close()
"""

"""
import board
import busio
import time

# 初始化串口通信
uart = busio.UART(board.TX, board.RX, baudrate=9600)

# 主循环
while True:
    data = uart.read(32)  # 读取串口数据，最多读取32字节
    if data is not None:
        print("Received:", data)
    time.sleep(0.1)  # 等待一段时间，避免频繁读取
"""