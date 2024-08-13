import time
from adafruit_servokit import ServoKit

with open('path.txt', 'r') as file:
    lines = file.readlines()

data_list = []
for line in lines:
    row = list(map(int, line.strip().split(',')))
    data_list.append(row)
for row in data_list:
    print(row)