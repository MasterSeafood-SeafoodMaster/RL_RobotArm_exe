

from TB_Arm import Arm
import time
import board
from digitalio import DigitalInOut, Direction, Pull

btn = DigitalInOut(board.D35)
btn.direction = Direction.INPUT
btn.pull = Pull.UP

arm=Arm()
while False:
    #arm.reset()
    arm.to90()
#time.sleep(1)

switch=False
ori=[2.5, 2.5]

while True:
    if btn.value:
       switch=not switch 
    if switch:
        D=0.5
        for i in range(5):
            arm.draw((ori[0]-D, ori[1]-(D)), (ori[0]+D, ori[1]-(D)))
            arm.draw((ori[0]+D, ori[1]-(D)), (ori[0]+D, ori[1]+(D)))
            arm.draw((ori[0]+D, ori[1]+(D)), (ori[0]-D, ori[1]+(D)))
            arm.draw((ori[0]-D, ori[1]+(D)), (ori[0]-D, ori[1]-(D)))
            D+=0.5
        

        arm.reset()
        switch=not switch
    time.sleep(0.1)
