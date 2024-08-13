from dof2 import Arm
import threading
from picamera2 import Picamera2
import cv2

l=[0,0,0,0]
arm=Arm()
import socket
def server_thread(host, port):
    global l
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    

    print("waiting...")
    while True:
        data, client_address = server_socket.recvfrom(32)
        l=data.decode().split(',')
        print("received:", l)
        

st = threading.Thread(target=server_thread)
st.daemon=True
st.start()
lock=threading.Lock()

picam2 = Picamera2()
picam2.start()
while True:
    lock.acquire()
    if abs(float(l[2]))>0.5:
        arm.pos[2]+=float(l[2])*0.05
        
    if abs(float(l[3]))>0.5:
        arm.pos[0]+=float(l[3])*0.05
    lock.release()
    
    print(arm.pos)
    arm.move()
    im = picam2.capture_array()
    im_bgr = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)

    cv2.imshow("Camera", im_bgr)
    cv2.waitKey(1)


if __name__ == "__main__":
    HOST = '192.168.137.116'
    PORT = 12345 
    start_server(HOST, PORT)
