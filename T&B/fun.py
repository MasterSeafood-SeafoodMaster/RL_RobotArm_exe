import torch
import torch.nn as nn
import pyswarm





input_data = torch.tensor([1]*11, dtype=torch.float32)
output = net(input_data)
print("网络输出:", output)

# 定义适应度函数，接受输入数据并返回神经网络输出的负值


# 使用PSO进行优化
lb = [0.0] * 11  # 输入数据的下限
ub = [1.0] * 11  # 输入数据的上限

# 使用PSO找到最大化输出的输入
optimal_input, _ = pyswarm.pso(fitness_function, lb, ub)

print("最佳输入数据:", optimal_input)
input_tensor = torch.tensor(optimal_input, dtype=torch.float32)
print(net(input_tensor))

fixed_values = [0.0, 0.0, 0.0, 0.0, 0.18798643350601196, 0.5904695987701416, 0.3423038721084595]
lb=[0.0] * 4

fixed_values = np.array(fixed_values)
lb = np.array(lb)
print(np.hstack((array1, array2)))