import torch
import torch.nn as nn
from torch.optim import Optimizer

class CustomNN(nn.Module):
	def __init__(self):
		super(CustomNN, self).__init__()
		self.fc1 = nn.Linear(11, 64)
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