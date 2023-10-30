import numpy as np

# 定义一个向量（示例中使用的向量为[3, 4]）
vector = np.array([3, 4])

# 定义Y轴单位向量
y_axis = np.array([0, 1])

# 使用内积计算向量与Y轴的夹角（弧度）
angle_rad = np.arccos(np.dot(vector, y_axis) / (np.linalg.norm(vector) * np.linalg.norm(y_axis)))

# 将弧度转换为度
angle_deg = np.degrees(angle_rad)

print(f"向量与Y轴的夹角（弧度）: {angle_rad}")
print(f"向量与Y轴的夹角（度）: {angle_deg}")