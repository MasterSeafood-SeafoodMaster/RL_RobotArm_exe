from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.side_channel.engine_configuration_channel import EngineConfigurationChannel
from mlagents_envs.environment import ActionTuple
import random

import time
import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
import pyswarm



class CustomNN(nn.Module):
	def __init__(self):
		super(CustomNN, self).__init__()
		self.fc1 = nn.Linear(11, 64)
		self.fc2 = nn.Linear(64, 1)

	def forward(self, x):
		x = torch.relu(self.fc1(x))  
		x = self.fc2(x)
		return x

Q_net = CustomNN()
optimizer = optim.Adam(Q_net.parameters(), lr=0.001)
criterion = nn.MSELoss()

fixed_values = [0, 0, 0, 0, 0, 0, 0]
lb = [-1.0] * 4
ub = [1.0] * 4
def fitness_function(input_data):
	input_data = np.hstack((fixed_values, input_data))
	input_tensor = torch.tensor(input_data, dtype=torch.float32)
	output = Q_net(input_tensor)
	
	return -output.item()

# init
channel = EngineConfigurationChannel()
env = UnityEnvironment("RobotArm", side_channels=[channel])
channel.set_configuration_parameters(time_scale = 1.0)
env.reset()
behavior_names = list(env.behavior_specs.keys())
behavior_value = list(env.behavior_specs.values())


discrete_action = None; continuous_action=None
for i in range(10000):
	
	try:
		env.step()
		print("step", i)

		DecisionStep, TerminalStep = env.get_steps(behavior_names[0])
		#print(DecisionStep.obs) #vector(7)

		# PSO_action(ep)
		#if random.random()>0.5:
		fixed_values = DecisionStep.obs[0].tolist()[0]
		optimal_input, _ = pyswarm.pso(fitness_function, lb, ub)
		#agentsNum = len(DecisionStep.agent_id)
		best_Q_value = -fitness_function(optimal_input)
		continuous_action = np.array([optimal_input])
		#else:
			#continuous_action = np.random.rand(1,4)*2-1
			#best_Q_value = -fitness_function(continuous_action)

		#setAction
		actions = ActionTuple(continuous_action, discrete_action)
		env.set_actions(behavior_names[0], actions)
		reward = TerminalStep.reward[0]

		rounded_list = [round(num, 2) for num in fixed_values]
		print("obs:", rounded_list)
		print("Action:", continuous_action)
		print("Max_Q_value", best_Q_value)
		print("reward", reward)

		# back
		predicted_value = torch.tensor(best_Q_value, requires_grad=True)
		target_value = torch.tensor(reward, requires_grad=False)
		
		loss = criterion(predicted_value, target_value)
		print("loss:", loss.item())
		print()
		optimizer.zero_grad()
		loss.backward()
		optimizer.step()
		
	except:
		env.close()


env.close()