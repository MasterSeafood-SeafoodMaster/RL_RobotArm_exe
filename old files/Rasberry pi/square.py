from dof2 import Arm
import time

arm=Arm()
arm.pos=[-2.5, 0, 7]
while True:
    for i in range(50):
        arm.pos[2] +=0.1
        arm.move()
        time.sleep(0.01)
    for i in range(50):
        arm.pos[0] +=0.1
        arm.move()
        time.sleep(0.01)
    for i in range(50):
        arm.pos[2] -=0.1
        arm.move()
        time.sleep(0.01)
    for i in range(50):
        arm.pos[0] -=0.1
        arm.move()
        time.sleep(0.01)



