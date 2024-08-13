import socket
import cv2
import numpy as np
socket.setdefaulttimeout(10)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 12345

server_socket.connect((host, port))

from rs_tool import rs_Camera
cap = rs_Camera()

while True:
    image, depth_image = cap.getframe()

    h, w, c = image.shape
    rgbd_image = np.zeros((h, w, 5), dtype=np.uint8)
    rgbd_image[:, :, :3] = image
    rgbd_image[:, :, 3] = depth_image//100
    rgbd_image[:, :, 4] = depth_image%100
    print(rgbd_image.shape)

    image_string = rgbd_image.tobytes()
    server_socket.sendall(image_string)

    success=server_socket.recv(1024)
    print(success.decode("utf-8"))
server_socket.close()