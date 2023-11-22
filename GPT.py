from ArmEnv_3D_ori import ArmEnv_3D
import numpy as np
import time

Arm = ArmEnv_3D([4.25, 5.5, 4.3, 8.3], True)
Arm.ylenList = [0, -2.25, 2.25, -2.25]

path = []

# Move to the initial position
path += Arm.moveto([2, -4.25, 13], 40)

# Move to the position of the ball
path += Arm.moveto([2, -4.25, -1], 60)

# Close the claw to grasp the ball
path += [[-91, 0, 0, 0]]

# Move to a safe position outside the tower's radius (radius 7)
safe_position = [2, -4.25, 13]
path += Arm.moveto(safe_position, 60)

# Move to the top of the tower
path += Arm.moveto([10, 0.5, 13], 30)

# Open the claw to release the ball
path += [[91, 0, 0, 0]]
path += Arm.moveto([10, 0.5, 13], 30)
path += [[91, 0, 0, 0]]
path += [[91, 0, 0, 0]]

# Additional movements (you can customize these movements as needed)
# path += Arm.moveto([destination_x, destination_y, destination_z], steps)

# Save the path to a file
path_np = np.array(path)
path_np[:, 0] = path_np[:, 0] + 90
path_np[:, 1] = 180 - (path_np[:, 1] + 90)
path_np[:, 2] = path_np[:, 2] + 90
path_np[:, 3] = 180 - (path_np[:, 3] + 90)
f_path = path_np.tolist()

# Add intermediate points for smoother motion (adjust the number of points as needed)
a_values = np.linspace(f_path[-3][0], f_path[0][0], 10)
b_values = np.linspace(f_path[-3][1], f_path[0][1], 10)
c_values = np.linspace(f_path[-3][2], f_path[0][2], 10)
d_values = np.linspace(f_path[-3][3], f_path[0][3], 10)

points = np.column_stack((a_values, b_values, c_values, d_values)).astype(int)
f_path += points.tolist()
try:
	# Save the final path to a file
	with open('F:\\path.txt', 'w') as file:
	    for sublist in f_path:
	        line = ','.join(map(str, sublist))
	        file.write(line + '\n')
except:
	print("no device connected")

# Execute the path
while True:
    for pa in path:
        if -91 < pa[0] < 91:
            Arm.forward_kinematics(pa)
            Arm.updatePicture()
