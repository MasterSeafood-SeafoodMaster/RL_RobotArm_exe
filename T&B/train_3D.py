from model import CustomNN, CustomOptimizer, CustomLoss
import pyswarm
import numpy as np
import random
import torch
import torch.nn as nn
from torchsummary import summary
Q_net = CustomNN()
optimizer = CustomOptimizer(Q_net.parameters(), lr=0.001, momentum=0.9)
criterion = CustomLoss()
summary(Q_net, input_size=(11))

observation = [0]*7 #ang(1~4), target(xyz)
lb = [-1.0] * 4
ub = [1.0] * 4 #delta ang(1~4)

def fitness_function(input_data):
	input_data = np.hstack((observation, input_data))
	input_tensor = torch.tensor(input_data, dtype=torch.float32)
	output = Q_net(input_tensor)
	
	return -output.item()

def get_Action(epsilon):
	if random.random()>epsilon:
		action, _ = pyswarm.pso(fitness_function, lb, ub, swarmsize=10, maxiter=100)
	else:
		action = np.random.rand(4)*2-1
	Q_value = -fitness_function(action)
	
	return Q_value, action

from ArmEnv_3D import ArmEnv_3D
Arm = ArmEnv_3D([5, 5, 5], False)
epoch = 100000
epsilon = 0.1


Arm.angList = [0, 0, 0, 0]
Arm.target = [10, 10, 10]
#Arm.updatePicture()

Last_Q=0; Last_R=0
for i in range(epoch):
	observation = Arm.getObs_norm()
	Q_value, action = get_Action(epsilon)
	Arm.setAction(action)
	Arm.compCord_y()
	#Arm.updatePicture()

	rDis = 1-(Arm.getDistance()/30) # (rad=15)
	rAng = 1-(sum(abs(item) for item in action)/4) #action (-1~1)*3

	reward = (rDis*0.9)+(rAng*0.1)

	#Q_value = torch.tensor(Q_value, requires_grad=True).float()
	#reward = torch.tensor(reward, requires_grad=False).float()
	loss = criterion(Last_R, reward, Last_Q, Q_value)
	Last_R=reward; Last_Q=Q_value

	print("step", i)
	print("observation", observation)
	print("action", action)
	print("Q_value", Q_value)
	print("reward", reward)
	formatted_list = [format(item, '.2f') for item in Arm.cord[2]]
	print("top", formatted_list)
	print()
