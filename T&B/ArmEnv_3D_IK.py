import matplotlib.pyplot as plt
import numpy as np
import random
import math

class ArmEnv_3D:
	def __init__(self, lList, vision=True):
		self.lenList = lList
		self.lnum = len(lList)
		self.angList = [0]*self.lnum
		self.target=[5, 5, 5]
		self.cord=[0]*3; self.FK()

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
		for i in range(self.lnum):
			theta+=self.angList[i]
			x, z = self.compVector(self.lenList[i], theta)
			top[0] += x
			top[1] += z
			cordList.append([top[0], top[1]])
		return cordList

	# 修正x, y
	def FK(self):
		cord = self.compCord()
		for i in range(self.lnum):
			x, z = cord[i]
			x, y = self.compVector(x, self.angList[self.lnum-1])
			cord[i] = [x, y, z]
		self.cord = cord

	def IK(self):
		x, y, z = self.cord
		b = math.atan2(y, x)*(180/math.pi)
		l=math.sqrt(x*x + y*y)
		h=math.sqrt(l*l + z*z)
		phi = math.atan(z/l)*(180/math.pi)
		theta=math.acos(h/10)*(180/math.pi)
		
		a1=phi+theta
		a2=phi-theta

		self.angList=[a1, a2, b]

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
	Arm = ArmEnv_3D([5.5, 5.5, 8.5], True)
	r=0; d=1
	while True:
		Arm.cord=[5, 5, 5]
		print(Arm.cord)
		#Arm.FK()
		Arm.IK()
		Arm.FK()
		Arm.updatePicture()
		
		#r+=d
		#if r==90 or r==-90: d*=-1
	
