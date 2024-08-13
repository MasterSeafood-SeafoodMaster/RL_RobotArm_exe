from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)
kit.servo[0].set_pulse_width_range(500, 2500)
kit.servo[1].set_pulse_width_range(500, 2500)
kit.servo[2].set_pulse_width_range(400, 2375)
kit.servo[3].set_pulse_width_range(500, 2500)

kit.servo[0].angle=90
kit.servo[1].angle=75
kit.servo[2].angle=90
kit.servo[3].angle=90
time.sleep(3)
idx=4
while True:
	for i in range(0, 91, 1):
		kit.servo[idx].angle=i
		time.sleep(0.01)
	time.sleep(2)

	for i in range(91, 0, -1):
		kit.servo[idx].angle=i
		time.sleep(0.01)
	time.sleep(2)

