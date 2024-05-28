import ikpy.chain
import numpy as np
import ikpy.utils.plot as plot_utils
import matplotlib.pyplot as plt
import random
import math
my_chain = ikpy.chain.Chain.from_urdf_file("arm.URDF")
angList = my_chain.forward_kinematics([0, 0, math.radians(90), 0, ], full_kinematics=True)
for al in angList:
	print(al[:3, 3])


"""
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.ion()
target_position = [ 0, 0, 0.15]

for i in range(10000):

	
	angList = my_chain.inverse_kinematics(target_position)
	print("The angles of each joints are : ", angList)
	real_frame = my_chain.forward_kinematics(my_chain.inverse_kinematics(target_position))
	print("Computed position vector : %s, original position vector : %s" % (real_frame[:3, 3], target_position))

	ax.cla()
	angList[0]=0.5
	my_chain.plot(angList, ax, target=target_position)
	ax.set_xlim(-0.1, 0.1)
	ax.set_ylim(-0.1, 0.1)
	ax.set_zlim(-0.1, 0.1)

	plt.draw()
	plt.pause(0.01)
	#target_position[1] += (random.random()-0.5)*0.01
	#target_position[2] += (random.random()-0.5)*0.01
	target_position[1] = min(0.15, max(target_position[1], -0.15))
	target_position[2] = min(0.15, max(target_position[2], -0.15))
"""