import time
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

for i in range(5): 
    kit.servo[i].set_pulse_width_range(500, 2500)
kit.servo[2].set_pulse_width_range(390, 2400)   
kit.servo[3].set_pulse_width_range(440, 2500)
kit.servo[0].angle=90
kit.servo[1].angle=0
kit.servo[2].angle=90
kit.servo[3].angle=90
kit.servo[4].angle=90
time.sleep(3)

while True:
    for ang in range(0, 92, 2):
        #for i in range(5): 
        kit.servo[2].angle=ang
        time.sleep(0.01)
    time.sleep(1)
  
    for ang in range(90, 0, -2):
        #for i in range(5): 
        kit.servo[2].angle=ang
        time.sleep(0.01)
    time.sleep(1)