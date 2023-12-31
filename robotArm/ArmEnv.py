import matplotlib.pyplot as plt
import numpy as np
import random
import math

class ArmEnv:
	def __init__(self, lList, vision=True):
		self.lenList = lList
		self.angList = [0]*len(self.lenList)
		self.last = self.angList.copy()
		self.cordList= self.compCord(self.angList)
		self.target = [0, 0]
		self.Reward=0
		self.lim=sum(self.lenList)

		self.vision=vision
		
		if self.vision: self.initPicture()
		
	def compVector(self, a, theta):
		radians = math.radians(theta)
		x = a*math.sin(radians)
		y = a*math.cos(radians)
		return x, y

	def compCord(self, angList):
		top = [0, 0]; theta=0
		cordList=[]
		for i in range(len(self.lenList)):
			theta+=angList[i]
			x, y = self.compVector(self.lenList[i], theta)
			top[0] += x
			top[1] += y
			cordList.append([top[0], top[1]])
		return cordList

	def setAngle(self, aList):
		self.angList=aList
		#self.angList = aList
		#print("curr:", self.angList[i])
		self.cordList = self.compCord(self.angList)

	def resetTarget(self):
		angle = random.uniform(0, 360)
		angle_in_radians = math.radians(angle)
		distance = random.uniform(self.lenList[0], self.lim)
		x = distance * math.cos(angle_in_radians)
		y = distance * math.sin(angle_in_radians)
		self.target = [x, abs(y)]

	def ResetArm(self):
		self.angList = []
		for i in range(len(self.lenList)):
			self.angList.append(random.randint(-90, 90))
		self.last = self.angList.copy()
		self.cordList = self.compCord(self.angList)

	def getReward(self):
		distance = math.sqrt((self.target[0] - self.cordList[-1][0]) ** 2 + (self.target[1] - self.cordList[-1][1]) ** 2)
		if not all(-90 < x < 90 for x in self.angList): #若角度超出範圍
			self.Reward=-1.0
		elif distance<0.5:
			self.Reward=1.0
		else:
			self.Reward=1-(distance/(self.lim*2))
		return self.Reward

	def getObs(self):
		return self.angList+self.target

	def setAction(self, mList):
		for i in range(len(self.angList)):
			self.angList[i] += mList[i]
		self.cordList = self.compCord(self.angList)
		if self.vision: self.updatePicture()
		
	def initPicture(self):
		plt.ion()
		plt.figure()

	def updatePicture(self):
		#print(self.last)
		#print(self.angList)

		plt.clf()
		plt.xlim(-self.lim*1.5, self.lim*1.5)
		plt.ylim(-self.lim*1.5, self.lim*1.5)
		#plt.ylim(0, self.lim*1.5)
		
		cordList_np = np.array(self.cordList)
		cordList_np = np.vstack(([0, 0], cordList_np))
		colors = ['r', 'y', 'g', 'b']
		plt.plot(cordList_np[:, 0], cordList_np[:, 1], 'k-', zorder=1)
		plt.scatter(cordList_np[:, 0], cordList_np[:, 1], c=colors, zorder=2)

		plt.scatter(self.target[0], self.target[1], c='purple', marker='o', s=100, zorder=2)
		self.getReward()
		
		plt.draw()
		plt.pause(0.0001)




