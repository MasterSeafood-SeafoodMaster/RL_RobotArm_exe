#LLM 呼叫的函式庫

from dof2 import Arm
from picamera2 import Picamera2
from l298n_test import l298n
from opencv_mask import getRedCenter, getBlueCenter, getGreenCenter
import numpy as np
import time
import cv2

class movementManager:
    def __init__(self):
        self.picam2 = Picamera2()
        self.picam2.start()
        self.arm=Arm()
        self.block=False
        self.foward=False
        self.loaded=False
        #self.Driver=l298n()
        
    def getCubeCenter(self, color):
        frame = self.picam2.capture_array()
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        if color=="red": center=getRedCenter(hsv)
        elif color=="blue": center=getBlueCenter(hsv)
        elif color=="green": center=getGreenCenter(hsv)
        return center
                    
    """
    def find(self, color):
        print("find:", color)
        while True:
            center=self.getCubeCenter(color)
            if len(center)>0:
                self.Driver.s()
                time.sleep(1)
                print(color+" found!")
                break
            else:
                self.Driver.l()
        
        while True:
            center=self.getCubeCenter(color)
            xth=25; yth=25;
            if(center[1]<180+yth):
                self.Driver.s()
                break
            else:
                xd=center[0]-320
                yd=center[1]-180
                sList=[0, 0]
                if yd>0:
                    sList=[-37, -37]
                elif yd<0:
                    sList=[37, 37]
                 
                if xd>0:
                    sList[1]=0
                elif xd<0:
                    sList[0]=0                   
                self.Driver.set_motor_speed(sList[0], sList[1])
    """
            
                    
    def aim(self, color):
        print("aim:", color)
        ccount=0
        while(True):
            center=self.getCubeCenter(color)
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
            """"""
                    
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
    
    def grab(self):
        print("grab")
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
        self.block=True
        time.sleep(1)
        
    
    def putdown(self):
        print("putdown")
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
        
        self.block=False
        self.reset()
        time.sleep(1)
    
    
    def reset(self):
        ca3=self.arm.aList[3]
        a3=(120-ca3)/10
        
        x=0-self.arm.pos[0]
        y=0.5-self.arm.pos[1]
        z=8-self.arm.pos[2]
        for i in range(10):
            self.arm.pos[0]+=x/10
            self.arm.pos[1]+=y/10
            self.arm.pos[2]+=z/10
            self.arm.move(mode="load", va3=ca3+int(a3*i))
            time.sleep(0.05)
        self.foward=False
    
    def ToLoadPos(self):
        self.reset()
        ca3=self.arm.aList[3]
        a3=(140-ca3)/10
        
        x=0-self.arm.pos[0]
        y=2.75-self.arm.pos[1]
        z=4-self.arm.pos[2]
        
        for i in range(1, 11):
            self.arm.pos[0]+=x/10
            self.arm.pos[1]+=y/10
            self.arm.pos[2]+=z/10
            self.arm.move(mode="load", va3=ca3+int(a3*i))
            time.sleep(0.05)
    
    def ToUnloadPos(self):
        self.reset()
        ca3=self.arm.aList[3]
        a3=(140-ca3)/10
        
        x=0-self.arm.pos[0]
        y=0.5-self.arm.pos[1]
        z=8-self.arm.pos[2]
        for i in range(1, 11):
            self.arm.pos[0]+=x/10
            self.arm.pos[1]+=y/10
            self.arm.pos[2]+=z/10
            self.arm.move(mode="load", va3=ca3+int(a3*i))
            time.sleep(0.05)
    
    def ToFowardPos(self):
        self.reset()
        ca3=self.arm.aList[3]
        a3=(30-ca3)/10
        
        x=0-self.arm.pos[0]
        y=4-self.arm.pos[1]
        z=7-self.arm.pos[2]
        for i in range(10):
            self.arm.pos[0]+=x/10
            self.arm.pos[1]+=y/10
            self.arm.pos[2]+=z/10
            self.arm.move(mode="load", va3=ca3+int(a3*i))
            time.sleep(0.05)
        
    def load(self):
        
        if self.loaded==False:
            print("load")
            self.arm.grab()
            self.ToLoadPos()
            self.arm.release()
            self.loaded=True
    
    def unload(self):
        
        if self.loaded==True:
            print("unload")
            self.arm.release()
            self.ToLoadPos()
            self.arm.grab()
            self.ToUnloadPos()
            self.loaded=False
    
    def lookForward(self):
        if self.foward==False:
            self.arm.release()
            self.ToFowardPos()
            self.foward=True


if __name__=='__main__':
    mm=movementManager()
    while True:
        #mm.aim("red")
        mm.grab()
        mm.load()
        mm.lookForward()
        time.sleep(3)
        mm.unload()
        mm.putdown()
        mm.reset()
        time.sleep(3)
    



