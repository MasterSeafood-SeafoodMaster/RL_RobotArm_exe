from ArmEnv_3D_ori import ArmEnv_3D
import math

Arm = ArmEnv_3D([5.942, 6.81, 8.747, 7.523], False)
path = []
#Please planning path form hear
#path+=Arm.moveto([0, 0, 25], 20) explain: Move to [0, 0, 25] in 20 steps
#path+=[[-91, 0, 0, 0]] explain: Close claw
#path+=[[91, 0, 0, 0]] explain: Open claw


# Move to the ball's position [10.5, 12, 2] in 20 steps
path += Arm.moveto([10.5, 12, 2], 20)

# Close claw to catch the ball
path += [[-91, 0, 0, 0]]


# Move to the top of the tower [9.5, 0, 14.5] in 20 steps
path += Arm.moveto([9.5, 0, 14.5], 20)

# Open claw to release the ball
path += [[91, 0, 0, 0]]

#reset
end=path[-2].copy()
while not sum(end)==0:
    for i in range(len(end)):
        if end[i]>0: end[i]-=1
        elif end[i]<0: end[i]+=1
    path.append(end.copy())

# Save the final path to a file
with open('./path.txt', 'w') as file:
    for sublist in path:
        line = ','.join(map(str, sublist))
        file.write(line + '\n')

"""
Arm.initPicture()
while True:
    for ap in path:
        Arm.angList=ap
        Arm.forward_kinematics(Arm.angList)
        Arm.updatePicture()
"""

path = []
path += Arm.moveto([0, 0, 25], 20)
path += Arm.moveto([10.5, 12, 2], 20)
path+=[[-91, 0, 0, 0]]
path += Arm.moveto([10, 13, 15], 20)
path += Arm.moveto([9.5, 0, 14.5], 20)
path+=[[91, 0, 0, 0]]
print(path)