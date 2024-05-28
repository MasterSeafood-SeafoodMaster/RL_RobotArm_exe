import matplotlib.pyplot as plt
import numpy as np
import random
import math
import keyboard
import time

class ArmEnv_3D:
    def __init__(self, lList, vision=True):
        self.lenList = lList
        self.ylenList=[0, 0, 0, 0]
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
        
    def gradient_policy(self,times=100, points=10, speed=5):
        np_target=np.array(self.target)
        d_theta=0.01
        path=[]
        for tp in range(times*points):
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
                
            if tp%times==0:
                top=self.forward_kinematics(self.angList)
                reg=self.angList.copy()
                for r in range(len(reg)):
                    reg[r]=round(reg[r])
                path.append(reg)
        return path
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
    Arm = ArmEnv_3D([5.942, 6.81, 8.747, 7.523], False)
    Arm.angList=[0, 0, 0, 0]
    anglePath=[]

    Arm.target=[-8, 2, 8]
    anglePath+=Arm.gradient_policy(points=20)
    Arm.target=[-8, 2, 15]
    anglePath+=Arm.gradient_policy(points=20)
    Arm.target=[8, 2, 8]
    anglePath+=Arm.gradient_policy(points=20)
    Arm.target=[8, 2, 15]
    anglePath+=Arm.gradient_policy(points=20)

    print(anglePath)
    print(len(anglePath))
    Arm.initPicture()
    while True:
        for ap in anglePath:
            Arm.angList=ap
            Arm.forward_kinematics(Arm.angList)
            Arm.updatePicture()





