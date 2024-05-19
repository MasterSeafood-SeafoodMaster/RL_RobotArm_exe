from ArmEnv_3D_ori import ArmEnv_3D
import numpy as np
import time

Arm = ArmEnv_3D([5.942, 6.81, 8.747, 7.523], True)
Arm.ylenList = [0, 0, 0, 0]
path = []

# Move to the initial position
path += Arm.moveto([8, -7.5, 5], 90)

# Open the claw
path += [["O", "P", "E", "N"]]

# Move to the ball position
path += Arm.moveto([8, -6.5, 1], 60)

# Close the claw to catch the ball
path += [["C", "L", "O", "S"]]

# Move above the tower with detour
path += Arm.moveto([15, 2, 20], 90)

# Move down to the top of the tower while avoiding the sides
path += Arm.moveto([15, 2, 17], 90)

# Open the claw to release the ball on top of the tower
path += [["O", "P", "E", "N"]]

# Save the path to a file
with open('./path.txt', 'w') as file:
    for sublist in path:
        line = ','.join(map(str, sublist))
        file.write(line + '\n')

# Execute the path
while True:
    for pa in path:
        if type(pa[0]) == int:
            Arm.forward_kinematics(pa)
            Arm.updatePicture()
