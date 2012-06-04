import numpy as np
from corruptor import GaussianCorruptor

a = np.array([[1, 0, 2, 3, 4, 5], [0, 3, 4, 5, 6, 7]])
corruptor = GaussianCorruptor(stdev=0.1, rng=3310)
out = corruptor(a)
print out
