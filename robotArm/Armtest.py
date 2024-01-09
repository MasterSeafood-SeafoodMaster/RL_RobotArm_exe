from ArmEnv_3D_ori import ArmEnv_3D
import math
#import Cuplib as cup
import time
#arm = cup.Arm([8, 5, 4, 2, 1, 0])

Arm = ArmEnv_3D([0, 5, 5, 5], True)
Arm.angList=[0, 0, 0, 0]
Arm.target=[5, 5, 5]

radius = 4
print("Zero")
#arm.Zero()
time.sleep(3)
t=0
anglePath=[]
for ang in range(0, 360, 5):
    rad = ang * (math.pi / 180)
    r   = [5,
           0 + radius * math.cos(rad),
           10 + radius * math.sin(rad)]
    #top = Arm.forward_kinematics(Arm.angList)
    Arm.target=r
    Arm.gradient_policy(1000, 2)
    anglePath.append(Arm.angList.copy())
    top = Arm.forward_kinematics(Arm.angList)
    Arm.updatePicture()
    print(r, top)

while True:
    for a in anglePath:
        Arm.angList = a
        top = Arm.forward_kinematics(a)
        Arm.updatePicture()
        int_list = [int(x)+90 for x in a]
        int_list = int_list+[90]*2
        print(int_list)
        t+=1

