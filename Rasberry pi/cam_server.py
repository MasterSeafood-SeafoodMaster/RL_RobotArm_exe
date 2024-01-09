import socket
import cv2
import numpy as np

from ultralytics import YOLO
model = YOLO("best.pt")

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
            results=model(gbd_image, conf=0.3)
            boxes=results[0].boxes.xyxy
            objs=[]
            for b in boxes:
                gbd_image=cv2.rectangle(gbd_image, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (0, 255, 0), 2)
                depth_colormap=cv2.rectangle(depth_colormap, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (0, 255, 0), 2)
                mid=[(int(b[0])+int(b[2]))//2, (int(b[1])+int(b[3]))//2]
                objs.append(mid)
                depth_colormap=cv2.putText(depth_colormap, str(depth_image[mid[1]][mid[0]]), (int(b[0]), int(b[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)

            img=cv2.hconcat((gbd_image, depth_colormap))
            if len(objs)>0:
                deg = objs[0][0]-320
                if deg<0:
                    msg="right,"+str(-deg)
                else:
                    msg="left,"+str(deg)
            else:
                msg="none,0"

            client_socket.send(msg.encode("utf-8"))
            cv2.imshow('Received Image', img)
            cv2.waitKey(1)

    except socket.error as e:
        print(f"Error occurred: {e}")
        print("Waiting for a new connection...")

cv2.destroyAllWindows()
client_socket.close()
server_socket.close()
