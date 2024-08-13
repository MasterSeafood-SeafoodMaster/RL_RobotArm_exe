from dof2 import Arm
from picamera2 import Picamera2
from opencv_mask import getRedCenter
import numpy as np
import time
import cv2

picam2 = Picamera2()
picam2.start()

arm=Arm()
ccount=0
while(True):
    frame = picam2.capture_array()
    bgr=cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    center=getRedCenter(hsv)

    if len(center)>0:
        cv2.circle(bgr, center, 5, (0, 255, 0), -1)

        print(center) 
        xth=25; yth=25;
        if(320-xth<center[0]<320+xth)and(200-yth<center[1]<200+yth)and(ccount<=10):
            print("ccount:", ccount)
            ccount+=1

        elif ccount>10:
            print("try to grab")
            time.sleep(3)
            for i in range(50):
                arm.pos[1]+=0.1
                arm.move()
                time.sleep(0.01)
            arm.grab()
            for i in range(50):
                arm.pos[1]-=0.1
                arm.move()
                time.sleep(0.01)
            time.sleep(1)
            
            for i in range(50):
                arm.pos[1]+=0.1
                arm.move()
                time.sleep(0.01)
            arm.release()
            for i in range(50):
                arm.pos[1]-=0.1
                arm.move()
                time.sleep(0.01)
            time.sleep(3)
            ccount=0
        else:
            arm.pos[0]+=(center[0]-320)/3200
            arm.pos[1]=0
            arm.pos[2]-=(center[1]-240)/2400
            
            """
            if center[0]>320: 
                arm.pos[0]+=0.1
            else:
                arm.pos[0]-=0.1

            if center[1]>240:
                arm.pos[2]-=0.1
            else:
                arm.pos[2]+=0.1
            print(arm.pos)
            """
            arm.move()       

    cv2.imshow('live', bgr)

    if cv2.waitKey(1) == ord('q'): break

cv2.destroyAllWindows()
