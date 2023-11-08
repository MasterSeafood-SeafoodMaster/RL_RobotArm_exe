import matplotlib.pyplot as plt
import numpy as np
import random
import math
import keyboard
import time

class ArmEnv_3D:
    def __init__(self, lList, vision=True):
        self.lenList = lList
        self.angList = [0, 0, 0, 0]
        self.angDir = ["Z", "Y", "Y", "Y"]
        self.target=[5, 5, 5]
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
                          [0, 1, 0, 0],
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
                self.angList[i] += -slope*speed
                self.angList[i] = min(max(self.angList[i], -90), 90)
            top=self.forward_kinematics(self.angList)
            dis=np.linalg.norm(np_target - top0)
            if dis<0.1:
                break



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



