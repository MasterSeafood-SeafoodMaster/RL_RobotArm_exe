import time
import board
import pwmio
from adafruit_motor import servo
from digitalio import DigitalInOut, Direction, Pull

class Arm:
    def __init__(self):
        self.pins=[board.D26, board.D25, board.D33, board.D32, board.D27]
        self.pwms=[]
        for p in self.pins: self.pwms.append(pwmio.PWMOut(p, duty_cycle=2 ** 15, frequency=50))
        self.servos=[]
        self.servos.append(servo.Servo(self.pwms[0], min_pulse = 500, max_pulse = 2500))
        self.servos.append(servo.Servo(self.pwms[1], min_pulse = 500, max_pulse = 2600))
        self.servos.append(servo.Servo(self.pwms[2], min_pulse = 400, max_pulse = 2500))
        self.servos.append(servo.Servo(self.pwms[3], min_pulse = 500, max_pulse = 2500))
        self.servos.append(servo.Servo(self.pwms[4], min_pulse = 500, max_pulse = 2500))
        self.reset()
    def reset(self):
        for s in self.servos: s.angle=90
        self.Open()

    def Close(self):
        for i in range(100, 140, 1):
            self.servos[4].angle=i
            time.sleep(0.05)
            
    def Open(self):
        for i in range(140, 100, -1):
            self.servos[4].angle=i        
            time.sleep(0.05)

    def setAngle(self, angList):
        print(angList)
        self.servos[0].angle=180-(angList[0]+90)
        self.servos[1].angle=180-(angList[1]+90)
        self.servos[2].angle=angList[2]+90
        self.servos[3].angle=180-(angList[3]+90)

filename = 'path.txt'
data_list = []
with open(filename, 'r') as file:
    for line in file:
        line_data = line.strip().split(',')
        data_list.append([int(num) for num in line_data])

btn = DigitalInOut(board.D35)
btn.direction = Direction.INPUT
btn.pull = Pull.UP
switch=False
arm=Arm()
while True:
    if btn.value:
       switch=not switch 
    if switch:
        for d in data_list:
            print(d)
            if -90<=d[0]<=90:
                arm.setAngle(d)
                time.sleep(0.05)
            elif d[0]<-90:
                arm.Close()
            elif d[0]>90:
                arm.Open()
        switch=not switch
    time.sleep(0.5)