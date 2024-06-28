import numpy as np
import matplotlib.pyplot as plt

# 定義目標函數
def f(theta):
    # 假設距離函數為 (theta - target_angle)^2
    target_angle = np.pi / 4  # 目標角度為 45 度（以弧度表示）
    return (theta - target_angle)**2

# 定義目標函數的導數
def df(theta):
    target_angle = np.pi / 4
    return 2 * (theta - target_angle)

# 梯度下降算法
def gradient_descent(starting_angle, learning_rate, iterations):
    theta = starting_angle
    angles = [theta]  # 用於保存每一步的角度
    for _ in range(iterations):
        theta = theta - learning_rate * df(theta)
        angles.append(theta)
    return angles

# 設置參數
starting_angle = 0  # 起始角度（以弧度表示）
learning_rate = 0.1  # 學習率
iterations = 20  # 迭代次數

# 執行梯度下降算法
angles = gradient_descent(starting_angle, learning_rate, iterations)

# 準備畫圖
theta = np.linspace(-1, 2, 400)
distance = f(theta)

plt.figure(figsize=(10, 6))
plt.plot(theta, distance, 'b', label=r'$f(\theta) = (\theta - \frac{\pi}{4})^2$')
plt.scatter(angles, [f(angle) for angle in angles], color='red')
for i, angle in enumerate(angles):
    plt.text(angle, f(angle), f'{i}', fontsize=9)

plt.title('Gradient Descent for Motor Rotation Angle')
plt.xlabel(r'$\theta$ (radians)')
plt.ylabel('Distance')
plt.legend()
plt.grid(True)
plt.show()
