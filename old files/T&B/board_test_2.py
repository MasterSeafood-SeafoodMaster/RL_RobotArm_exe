from ArmEnv_3D_ori import ArmEnv_3D
import numpy as np
import time
Arm=ArmEnv_3D([4.25, 5.5, 4.3, 8.3], True)
Arm.ylenList=[0, -2.25, 2.25, -2.25]

path=[]
#Please planning path form hear
#path+=Arm.moveto([2, -4.25, 13], 20)#Move to [2, -4.25, 13] in 25 steps
#path+=Arm.moveto([2, -4.25, 2], 30)#Move to [2, -4.25, 2] in 25 steps

#path+=Arm.moveto([2, -4.25, -1], 30)#Move to [2, -4.25, -1] in 25 steps
#path+=[[-91, 0, 0, 0]] #Close claw
#path+=Arm.moveto([2, -5, 17], 30)#Move to [2, -5, 17] in 25 steps
#path+=Arm.moveto([10, 0.5, 11.5], 30)#Move to [10, 0.5, 11.5] in 25 steps
#path+=[[91, 0, 0, 0]] #Open claw
#path+=Arm.moveto([10, 0.5, 11.5], 10)#Move to [10, 0.5, 11.5] in 25 steps
#path+=Arm.moveto([10, 1, 11.5], 10)#Move to [10, 1, 11.5] in 25 steps
#path+=Arm.moveto([10, 0.5, 11.5], 10)#Move to [10, 0.5, 11.5] in 25 steps
#path+=[[91, 0, 0, 0]] #Open claw
#path+=[[91, 0, 0, 0]] #Open claw


# backend process
path_np = np.array(path)
path_np[:,0]=path_np[:,0]+90
path_np[:,1]=180-(path_np[:,1]+90)
path_np[:,2]=path_np[:,2]+90
path_np[:,3]=180-(path_np[:,3]+90)
f_path=path_np.tolist()
a_values = np.linspace(f_path[-3][0], f_path[0][0], 10)
b_values = np.linspace(f_path[-3][1], f_path[0][1], 10)
c_values = np.linspace(f_path[-3][2], f_path[0][2], 10)
d_values = np.linspace(f_path[-3][3], f_path[0][3], 10)

points = np.column_stack((a_values, b_values, c_values, d_values)).astype(int)
f_path+=points.tolist()

with open('F:\\path.txt', 'w') as file:
    for sublist in f_path:
        line = ','.join(map(str, sublist))
        file.write(line + '\n')

while True:
    for pa in path:
        if -91<pa[0]<91:
            Arm.forward_kinematics(pa)
            Arm.updatePicture()


