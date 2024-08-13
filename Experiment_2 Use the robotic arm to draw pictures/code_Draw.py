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
        """
        arm.draw([1.0, 1.0], [4.0, 1.0])
        arm.draw([4.0, 1.0], [4.0, 4.0])
        arm.draw([4.0, 4.0], [1.0, 4.0])
        arm.draw([1.0, 4.0], [1.0, 1.0])
        arm.draw([1.0, 4.0], [2.5, 5.0])
        arm.draw([2.5, 5.0], [4.0, 4.0])
        """
        
        arm.reset()
        switch=not switch
    time.sleep(0.1)