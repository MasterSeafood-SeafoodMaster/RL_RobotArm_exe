import time
from adafruit_servokit import ServoKit

class ServoBoard:
    def __init__(self):
        self.kit = ServoKit(channels=16, frequency=50)
        self.servos=[]
        for i in range(16): self.servos.append(self.kit.servo[i])

        self.servos[0].set_pulse_width_range(500, 2450)
        self.servos[1].set_pulse_width_range(500, 2350)
        self.servos[2].set_pulse_width_range(465, 2470)
        self.servos[3].set_pulse_width_range(470, 2485)
        self.servos[4].set_pulse_width_range(2000, 2500)

        for s in self.servos: s.angle = 90
        self.servos[4].angle=180
        time.sleep(3)

    def setAngle(angleList):
        for i, s in enumerate(self.servos): s.angle = angleList[i]
        time.sleep(0.05)