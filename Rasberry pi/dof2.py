import math
import time
from adafruit_servokit import ServoKit
class Arm:
    def __init__(self):
        self.pos=[0, 0, 7]
        self.lastAva=self.pos.copy()
        self.kit = ServoKit(channels=16)
        self.kit.servo[0].set_pulse_width_range(500, 2500)
        self.kit.servo[1].set_pulse_width_range(500, 2500)
        self.kit.servo[2].set_pulse_width_range(475, 2375)
        self.kit.servo[2].set_pulse_width_range(390, 2400)   
        self.kit.servo[3].set_pulse_width_range(440, 2500)
        self.move()
        self.release()
        time.sleep(3)

    def move(self, mode="grab"):
        b, a1, a2, a3=self.pos2angle(self.pos[0], self.pos[1]+0.01, self.pos[2]+0.01, mode)
        #print(b, a1, a2, a3)
        if b>-1:
            self.kit.servo[0].angle=b
            self.kit.servo[1].angle=a1
            self.kit.servo[2].angle=a2
            self.kit.servo[3].angle=a3
    
    def grab(self):
        for i in range(90, 180, 5): 
            self.kit.servo[4].angle=i
            time.sleep(0.05)
    
    def release(self):
        for i in range(180, 90, -5): 
            self.kit.servo[4].angle=i
            time.sleep(0.05)
 
    def pos2angle(self, x, y, z, mode):
        
        dis = math.sqrt(x**2 + y**2 + z**2)
        #print(dis)
        if 5<dis<14:
            b=math.atan2(z, x)*(180/math.pi)
            l=math.sqrt((x*x)+(z*z))
            h=math.sqrt((l*l)+(y*y))
            
            phi=math.atan(l/y)*(180/math.pi)
            theta=math.acos(h/14)*(180/math.pi)
    
            a1=180-(phi+theta)
            a2=180-(phi-theta)-a1
            if mode == "grab":
                a3=90+(phi-theta)+5
            elif mode=="scan":
                a3=(phi-theta)
            self.lastAva=self.pos.copy()
            return [b, a1, a2, a3]
        else:
            self.pos=self.lastAva.copy()
            return [-1, -1, -1, -1]
