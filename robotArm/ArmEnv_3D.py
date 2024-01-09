import matplotlib.pyplot as plt
import numpy as np
import random
import math

class ArmEnv_3D:
	def __init__(self, lList, vision=True):
		self.lenList = lList
		self.angList = [0, 0, 0, 0]
		self.target=[5, 5, 5]
		self.cord=[]
		self.lim = sum(self.lenList)
		self.vision=vision
		if vision:
			self.initPicture()
			self.updatePicture()

	# 基礎運算 (x, y) = [L*sin(theta), L*cos(theta)]
	def compVector(self, a, theta):
		radians = math.radians(theta)
		x = a*math.sin(radians)
		y = a*math.cos(radians)
		return x, y

	# 計算x, z方向
	def compCord(self):
		top = [0, 0]; theta=0
		cordList=[] # 將手臂的每個關節座標紀錄後，迭代運算出頂點
		for i in range(3):
			theta+=self.angList[i]
			x, z = self.compVector(self.lenList[i], theta)
			top[0] += x
			top[1] += z
			cordList.append([top[0], top[1]])
		return cordList

	# 修正x, y
	def compCord_y(self):
		cord = self.compCord()
		for i in range(3):
			x, z = cord[i]
			x, y = self.compVector(x, self.angList[3])
			cord[i] = [x, y, z]
		self.cord = cord

	def getObs_norm(self):
		angList = [item / 90 for item in self.angList] #Angle range(-90~90)
		target = [item / self.lim for item in self.target] #Target range (-15~15)
		return angList+target

	def setAction(self, action):
		for i in range(len(action)):
			r = self.angList[i]+action[i]*180
			self.angList[i] = max(-90, min(90, r))
		if self.vision: self.updatePicture()

	def getDistance(self):
		p1 = self.target
		p2 = self.cord[2]
		dis = math.sqrt( (p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 + (p2[2] - p1[2]) ** 2 )
		return dis

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
		cord.insert(0, [0, 0, 0])
		cord = np.array(cord)
		self.ax.plot(cord[:, 0], cord[:, 1], cord[:, 2], c='k')
		self.ax.scatter(cord[:, 0], cord[:, 1], cord[:, 2], c='r')
		self.ax.scatter(self.target[0], self.target[1], self.target[2], c='b')

		plt.draw()
		plt.pause(0.001)

if __name__ == '__main__':
	Arm = ArmEnv_3D([5, 5, 5], True)
	r=0; d=1
	while True:
		Arm.angList=[0, 0, r, 0]
		Arm.compCord_y()
		Arm.updatePicture()
		print(Arm.cord)
		r+=d
		if r==90 or r==-90: d*=-1
	
