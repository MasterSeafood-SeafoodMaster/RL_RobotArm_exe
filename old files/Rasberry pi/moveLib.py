from dof2 import Arm
from picamera2 import Picamera2
from opencv_mask import getRedCenter, getBlueCenter
import numpy as np
import time
import cv2

class movementManager:
    def __init__(self):
        self.picam2 = Picamera2()
        self.picam2.start()
        self.arm=Arm()
        
    def aim(self, color):
        ccount=0
        while(True):
            frame = self.picam2.capture_array()
            hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
            if color=="red": center=getRedCenter(hsv)
            elif color=="blue": center=getBlueCenter(hsv)

            if len(center)>0:
                xth=25; yth=25;
                if(320-xth<center[0]<320+xth)and(200-yth<center[1]<200+yth)and(ccount<=10):
                    print("check:", ccount)
                    ccount+=1
                elif ccount>10:
                    print(color+" aimed!")
                    ccount=0
                    break
                else:
                    self.arm.pos[0]+=(center[0]-320)/3200
                    self.arm.pos[1]=0
                    self.arm.pos[2]-=(center[1]-175)/2400
                    ccount=0
                self.arm.move()
            else:
                print("scanning")
                dr=0.1
                while True:
                    self.arm.pos[0]+=dr
                    self.arm.move()
                    if self.arm.pos[0]>4 or self.arm.pos[0]<-4:
                        dr*=-1
                        time.sleep(1)
                    frame = self.picam2.capture_array()
                    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
                    if color=="red": center=getRedCenter(hsv)
                    elif color=="blue": center=getBlueCenter(hsv)
                    if len(center)>0: 
                        print("scanned!")
                        time.sleep(1)
                        break
                    
                    time.sleep(0.01)
                    
    def try2grab(self):
        print("try to grab")
        time.sleep(1)
        for i in range(50):
            self.arm.pos[1]+=0.1
            self.arm.move()
            time.sleep(0.01)
        self.arm.grab()
        for i in range(50):
            self.arm.pos[1]-=0.1
            self.arm.move()
            time.sleep(0.01)
        time.sleep(1)
        
        for i in range(50):
            self.arm.pos[1]+=0.1
            self.arm.move()
            time.sleep(0.01)
        self.arm.release()
        for i in range(50):
            self.arm.pos[1]-=0.1
            self.arm.move()
            time.sleep(0.01)
        time.sleep(1)

    def reset(self):
        x=0-self.arm.pos[0]
        y=0.5-self.arm.pos[1]
        z=8-self.arm.pos[2]
        for i in range(10):
            self.arm.pos[0]+=x/10
            self.arm.pos[1]+=y/10
            self.arm.pos[2]+=z/10
            self.arm.move()
            time.sleep(0.05)
        time.sleep(1)


if __name__=='__main__':
    mm=movementManager()
    while True:
        mm.reset()
        mm.aim("red")
        mm.try2grab()
        mm.reset()
        mm.aim("blue")
        mm.try2grab()      



