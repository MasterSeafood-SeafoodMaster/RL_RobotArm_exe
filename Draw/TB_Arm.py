import math
import time
import board
import pwmio
from ulab import numpy as np
from adafruit_motor import servo

class Arm:
    def __init__(self):
        self.armLen=[4, 5, 4.5]
        self.pos=[7.5, 0, -1.5]
        self.grabAng=90
        self.pins=[board.D26, board.D25, board.D33, board.D32]
        self.pwms=[]
        for p in self.pins: self.pwms.append(pwmio.PWMOut(p, duty_cycle=2 ** 15, frequency=50))
        self.servos=[]
        self.servos.append(servo.Servo(self.pwms[0], min_pulse = 450, max_pulse = 2450))
        self.servos.append(servo.Servo(self.pwms[1], min_pulse = 495, max_pulse = 2440))
        self.servos.append(servo.Servo(self.pwms[2], min_pulse = 545, max_pulse = 2500))
        self.servos.append(servo.Servo(self.pwms[3], min_pulse = 535, max_pulse = 2495))
        self.isD=False
        #self.reset()
        self.move()
        time.sleep(2)
        #self.servos.append(servo.Servo(self.pwms[4], min_pulse = 500, max_pulse = 2500))

        time.sleep(2)

    def Adjustment(self, idx):
        for s in self.servos: s.angle=90
        for i in range(0, 180, 1):
            self.servos[idx].angle=i
            time.sleep(0.01)
        time.sleep(2)
        for i in range(180, 0, -1):
            self.servos[idx].angle=i
            time.sleep(0.01)
        time.sleep(2)
        
    def penup(self):
        if self.isD:
            print("UP!!!")
            for i in range(5):
                self.pos[2]=-1.5+(i/5)
                self.move(uping=i*2)
                time.sleep(0.05)
            self.pos[2]=-0.5
            self.move(uping=10)
            self.isD=False
    def pendown(self):
        if not self.isD:
            print("DOWN!!!")
            for i in range(5):
                self.pos[2]=-0.5-(i/5)
                self.move()
                time.sleep(0.05)
            self.pos[2]=-1.5
            self.move()
            self.isD=True
    def pos2angle(self, px, py, pz):
        #dis = math.sqrt(x**2 + y**2 + z**2)
        z=pz+self.armLen[2]
        py*=0.65
        if True:#self.armLen[0]<dis<self.armLen[0]+self.armLen[1]:
            b=math.atan(py/px)*(180/math.pi)+90
            fix_x=2*math.cos(math.radians(b-90))
            fix_y=2*math.sin(math.radians(b-90))
            x=px-fix_x
            y=py-fix_y
            print(x, y, z)
            l=math.sqrt(x**2 + y**2)
            h=math.sqrt(l**2 + z**2)

            phi=math.atan(z/l)*(180/math.pi)
            theta=math.acos(h/9)*(180/math.pi)

            a1=phi+theta
            a2=180-(a1-phi+theta)
            a3=180-(90+phi-theta)

            #a1=180-a1
            #a2=180-a2
            return [b, a1, a2, a3]
        #else:
            #return [-1, -1, -1, -1]

    def move(self, uping=0):
        b, a1, a2, a3=self.pos2angle(self.pos[0], self.pos[1], self.pos[2])
        #print(b, a1, a2, a3, self.isD)
        if b>-1:
            self.servos[0].angle=min(180,max(0, b))
            self.servos[1].angle=min(180,max(0, a1))
            self.servos[2].angle=min(180,max(0, a2))
            self.servos[3].angle=min(180,max(0, a3))+uping
 

    def moveto(self, x, y, z):
        From=self.pos.copy()
        diff = abs(np.array(From) - np.array([x, y, z]))
        num_points=int(np.max(diff)*15)
        lx=np.linspace(From[0], x, num_points)
        ly=np.linspace(From[1], y, num_points)
        lz=np.linspace(From[2], z, num_points)
        #la=np.linspace(self.grabAng, ang, num_points)


        for i in range(num_points):
            self.pos=[lx[i], ly[i], lz[i]]
            #self.grabAng=la[i]
            self.move()
            time.sleep(0.01)
    def draw(self, f, t):
        f=self.vec2trans(f)
        t=self.vec2trans(t)
        if not (self.pos[0]==f[0] and self.pos[1]==f[1]):
            self.penup()
            self.moveto(f[0], f[1], self.pos[2])
            self.pendown()
        self.moveto(t[0], t[1], self.pos[2])

    def reset(self):
        self.penup()
        self.moveto(7.5, 0, self.pos[2])
        
    def vec2trans(self, vec):
        #ori=[7.5, 0] =[2.5, -2.5]
        x, y=vec
        return [x+5, y-2.5]

    def to90(self):
        for s in self.servos:
            s.angle=90
        