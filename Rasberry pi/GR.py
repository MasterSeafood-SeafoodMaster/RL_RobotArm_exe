from dof2 import Arm
from picamera2 import Picamera2
import time
import cv2


import threading

picam2 = Picamera2()
picam2.start()
def cam_thread():
    while True:
        im = picam2.capture_array()
        im_bgr = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    
        cv2.imshow("Camera", im_bgr)
        cv2.waitKey(1)


st = threading.Thread(target=cam_thread)
st.daemon=True
st.start()

arm=Arm()
while True:
    for i in range(0, 55, 5):
        arm.pos=[0, i/10, 8]
        arm.move()
        time.sleep(0.05)
    arm.grab()
    for i in range(55, 0, -5):
        arm.pos=[0, i/10, 8]
        arm.move()
        time.sleep(0.05)
    time.sleep(1)
    
    for i in range(0, 55, 5):
        arm.pos=[0, i/10, 8]
        arm.move()
        time.sleep(0.05)
    arm.release()
    for i in range(55, 0, -5):
        arm.pos=[0, i/10, 8]
        arm.move()
        time.sleep(0.05)
    time.sleep(1) 

