import matplotlib.pyplot as plt
import numpy as np
import random
import math
import keyboard
import time

class ArmEnv_3D:
    def __init__(self, lList, vision=True):
        self.lenList = lList
        self.ylenList=[0, -2.25, 2.25, -2.25]
        self.angList = [0, 0, 0, 0]
        self.angDir = ["Z", "Y", "Y", "Y"]
        self.target=[0, 0, sum(lList)]
        self.cord=[]
        self.lim = sum(self.lenList)
        self.vision=vision

        if vision:
            self.initPicture()

    def forward_kinematics(self, joint_angles):
        arm_lengths = self.lenList
        rotation_axes = self.angDir

        if len(arm_lengths) != len(joint_angles) or len(joint_angles) != len(rotation_axes):
            raise ValueError("len error")
        self.cord=[]
        T = np.identity(4)
        for i in range(len(arm_lengths)):
            ang = math.radians(joint_angles[i])
            if rotation_axes[i] == "Z":
                R = np.array([[math.cos(ang), -math.sin(ang), 0, 0],
                              [math.sin(ang), math.cos(ang), 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])
            elif rotation_axes[i] == "Y":
                
                R = np.array([[math.cos(ang), 0, math.sin(ang), 0],
                              [0, 1, 0, 0],
                              [-math.sin(ang), 0, math.cos(ang), 0],
                              [0, 0, 0, 1]])

            D = np.array([[1, 0, 0, 0],
                          [0, 1, 0, self.ylenList[i]],
                          [0, 0, 1, arm_lengths[i]],
                          [0, 0, 0, 1]])
            
            T = np.dot(T, np.dot(R, D))
            self.cord.append(T[:3, 3].tolist())
            #rpos = np.around(T[:3, 3], decimals=2)
            #print(rpos)
        
        end_effector_position = T[:3, 3]
        return end_effector_position
        
    def gradient_policy(self, times, speed=1):
        np_target=np.array(self.target)
        #dis=np.linalg.norm(np_target)
        #if(dis>sum(self.lenList))or(dis<self.lenList[1]):
            #print("out of range!")
        #else:
        d_theta=0.01
        for e in range(times):
            for i in range(len(self.lenList)):
                top0=self.forward_kinematics(self.angList)
                dis0 = np.linalg.norm(np_target - top0)

                d_angList=self.angList.copy()
                d_angList[i] += d_theta
                top1=self.forward_kinematics(d_angList)

                dis1=np.linalg.norm(np_target - top1)
                slope = (dis1-dis0)/d_theta
                self.angList[i] += max(min(-slope*speed, 5), -5)
                self.angList[i] = min(max(self.angList[i], -90), 90)
            top=self.forward_kinematics(self.angList)
            dis=np.linalg.norm(np_target - top0)
            if dis<0.1:
                #print("break")
                break
            
    def generate_points(self, point1, point2, num_points=10):
        x_values = np.linspace(point1[0], point2[0], num_points)
        y_values = np.linspace(point1[1], point2[1], num_points)
        z_values = np.linspace(point1[2], point2[2], num_points)

        points = np.column_stack((x_values, y_values, z_values))
        return points

    def moveto(self, new_target, num_points,re_int=True):
        line=self.generate_points(self.target, new_target, num_points)
        print(line)
        ang_history=[]
        for l in line:
            r=self.angList.copy()
            self.target=l
            self.gradient_policy(500, 2)

            #self.updatePicture()
            if re_int: 
                int_angList = [int(num) for num in self.angList]
                #print(int_angList)
                ang_history.append(int_angList)
            else:
                ang_history.append(self.angList.copy())

        return ang_history

    #可視化(optional)
    def initPicture(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        plt.ion()

    def updatePicture(self):
        self.ax.cla()
        self.ax.set_xlim(-self.lim*1.2, self.lim*1.2)
        self.ax.set_ylim(-self.lim*1.2, self.lim*1.2)
        self.ax.set_zlim(0, self.lim*1.2)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        cord = self.cord.copy()
        #cord.insert(0, [0, 0, 0])
        cord = np.array(cord)
        #print(cord)
        self.ax.plot(cord[:, 0], cord[:, 1], cord[:, 2], c='k')
        self.ax.scatter(cord[:, 0], cord[:, 1], cord[:, 2], c='r')
        self.ax.scatter(self.target[0], self.target[1], self.target[2], c='b')

        plt.draw()
        plt.pause(0.001)

if __name__ == '__main__':
    Arm = ArmEnv_3D([0, 5, 5, 5], True)
    Arm.angList=[0, 0, 0, 0]
    Arm.target=[5, 5, 5]
    
    radius = 4

    anglePath=[]
    for ang in range(0, 360, 5):
        rad = ang * (math.pi / 180)
        r   = [-5,
               0 + radius * math.cos(rad),
               10 + radius * math.sin(rad)]
        #top = Arm.forward_kinematics(Arm.angList)
        Arm.target=r
        Arm.gradient_policy(1000, 2)
        anglePath.append(Arm.angList.copy())
        top = Arm.forward_kinematics(Arm.angList)
        #Arm.updatePicture()
        print(r, top)

    while True:
        for a in anglePath:
            Arm.angList = a
            top = Arm.forward_kinematics(a)
            Arm.target=top
            Arm.updatePicture()
            int_list = [int(x)+90 for x in a]
            int_list = int_list+[90]*2
            
            print(int_list)
            #time.sleep(0.001)
        time.sleep(0.5)



