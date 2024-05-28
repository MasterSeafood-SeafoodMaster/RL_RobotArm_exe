from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import numpy as np
import seaborn as sns

from tqdm import tqdm
import gymnasium as gym

env = gym.make('Blackjack-v1', sab=True, render_mode="rgb_array")

#Obs
done=False
observation, info = env.reset()

#Observation = (16, 9, False)