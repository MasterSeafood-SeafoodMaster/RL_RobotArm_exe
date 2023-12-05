import socket
import cv2
import numpy as np

from ultralytics import YOLO
model = YOLO("yolov8n.pt")

socket.setdefaulttimeout(10)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.100.85'
port = 12345
server_socket.bind((host, port))
server_socket.listen(1)

print(f"Server listening on {host}:{port}...")

imgz=[480, 640]
while True:
    try:
        client_socket, addr = server_socket.accept()
        client_socket.settimeout(3)
        print(f"Connection from {addr}")

        while True:
            image_string = b""
            while len(image_string) < imgz[0] * imgz[1] * 5:  # 3 channels (BGR)
                data=client_socket.recv(8192)
                if not data:
                    break
                image_string += data


            rgbd_image = np.frombuffer(image_string[0:imgz[0] * imgz[1] * 5], dtype=np.uint8).reshape((imgz[0], imgz[1], 5))

            gbd_image = rgbd_image[:, :, :3].astype(np.uint8).copy()
            depth_image = rgbd_image[:, :, 3].astype(np.int64) * 100 + rgbd_image[:, :, 4].astype(np.int64)

            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
            print(depth_image)

            results = model(gbd_image, classes=[0])[0]
            b=results.boxes.xyxy[0]
            depth_colormap=cv2.rectangle(depth_colormap, (int(b[0]), int(b[2])), (int(b[1]), int(b[3])), (0, 0, 0), 2)

            print(b)
            center=((int(b[0])+int(b[2]))//2, (int(b[1])+int(b[3]))//2)
            print(center)
            depth_colormap = cv2.circle(depth_colormap, center, 10, (0,0,0), -1)
            image = np.vstack((gbd_image, depth_colormap))

            if center[0]<320:
                msg="right"
            else:
                msg="left"

            client_socket.send(msg.encode("utf-8"))
            cv2.imshow('Received Image', image)
            cv2.waitKey(1)

    except socket.error as e:
        print(f"Error occurred: {e}")
        print("Waiting for a new connection...")

cv2.destroyAllWindows()
client_socket.close()
server_socket.close()
