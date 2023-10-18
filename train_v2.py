

import torch
import torch.nn as nn
import torch.optim as optim
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

Q_net = CustomNN()
optimizer = optim.Adam(Q_net.parameters(), lr=0.001)
criterion = nn.MSELoss()

fixed_values = [0]*5
lb = [0.0] * 3
ub = [1.0] * 3
def fitness_function(input_data):
	input_data = np.hstack((fixed_values, input_data))
	input_tensor = torch.tensor(input_data, dtype=torch.float32)
	output = Q_net(input_tensor)
	
	return -output.item()


from ArmEnv import ArmEnv
import random

Arm = ArmEnv([5, 5, 5])
for i in range(10000):
	fixed_values = Arm.getObs()

	if random.random()>0.5:
		optimal_input, _ = pyswarm.pso(fitness_function, lb, ub)
	else:
		optimal_input = np.random.rand(3)*2-1
	best_Q_value = -fitness_function(optimal_input)

	moves=optimal_input*180
	reward = Arm.setAction(moves)

	rounded_list = [round(num, 2) for num in fixed_values]
	print("obs:", rounded_list)
	print("Action:", moves)
	#print("Max_Q_value", best_Q_value)
	print("reward", reward)

	predicted_value = torch.tensor(best_Q_value, requires_grad=True).float()
	target_value = torch.tensor(reward, requires_grad=False).float()

	loss = criterion(predicted_value, target_value)
	print("loss:", loss.item())
	print()
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()




