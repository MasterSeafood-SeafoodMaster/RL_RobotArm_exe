import torch
import torch.nn as nn
from torch.optim import Optimizer
import pyswarm
import numpy as np

class CustomNN(nn.Module):
	def __init__(self):
		super(CustomNN, self).__init__()
		self.fc1 = nn.Linear(8, 64)
		self.fc2 = nn.Linear(64, 1)

	def forward(self, x):
		x = torch.relu(self.fc1(x))  
		x = self.fc2(x)
		return x

class CustomLoss(nn.Module):
	def __init__(self):
		super(CustomLoss, self).__init__()

	def forward(self, Rn, Rn1, Qn, Qn1):
		if (Qn1-Qn)==0:
			return torch.tensor(-1.0, requires_grad=True).float()
		reg = (Rn1-Rn)/(Qn1-Qn)
		if reg<0:
			loss=-1.0
		elif reg>0:
			loss=1.0
		else:
			loss=0.0
		
		return torch.tensor(loss, requires_grad=True).float()

class CustomOptimizer(Optimizer):
	def __init__(self, params, lr=0.01, momentum=0.0):
		defaults = {
            'lr': lr,
            'momentum': momentum
        }
		super(CustomOptimizer, self).__init__(params, defaults)
		self.lr = lr
		self.momentum = momentum

	def step(self, closure=None):
		for group in self.param_groups:
			for p in group['params']:
				if p.grad is None:
					continue
				d_p = p.grad
				p.data.add_(self.lr, d_p)

Q_net = CustomNN()
optimizer = CustomOptimizer(Q_net.parameters(), lr=0.001, momentum=0.9)
criterion = CustomLoss()

fixed_values = [0]*5
lb = [-1.0] * 3
ub = [1.0] * 3

def fitness_function(input_data):
	input_data = np.hstack((fixed_values, input_data))
	input_data[0]/=90
	input_data[1]/=90
	input_data[2]/=90

	input_data[3]/=15
	input_data[4]/=15

	#print("input_data", input_data)
	input_tensor = torch.tensor(input_data, dtype=torch.float32)
	output = Q_net(input_tensor)
	
	return -output.item()

def get_Action(epsilon):
	if random.random()>epsilon:
		action, _ = pyswarm.pso(fitness_function, lb, ub, swarmsize=10, maxiter=100)
	else:
		action = np.random.rand(3)*2-1
	Q_value = -fitness_function(action)
	
	return Q_value, action


from ArmEnv import ArmEnv
import random

Arm = ArmEnv([5, 5, 5], False)
epoch = 100000
#epsilon = (i/epoch)*2
epsilon = 0.1
for i in range(epoch):
	Arm.ResetArm()
	Arm.resetTarget()
	maxstep=1000; Rn=0; Qn=0
	for j in range(maxstep):
		fixed_values = Arm.getObs()
		
		Qn1, action = get_Action(epsilon)
		Arm.setAction(action*180)
		Rn1 = Arm.getReward()

		
		if Rn1==-1:
			Arm.setAngle(Arm.last.copy())
			#print("Arm.last", Arm.last)

		rounded_obs = [round(num, 2) for num in fixed_values]

		log = f"step: {j}\nobs: {rounded_obs}\nAction: {action*180}\nRn: {Rn}\nQn: {Qn}\nRn1: {Rn1}\nQn1: {Qn1}\nepsilon: {epsilon}\n"
		print(log, end='\r', flush=True)

		loss = criterion(Rn, Rn1, Qn, Qn1)
		print(loss)
		optimizer.zero_grad()
		loss.backward()
		optimizer.step()

		Rn=Rn1; Qn=Qn1



