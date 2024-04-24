import numpy as np
import math

def dist(x, y):
    dist_grid = np.empty([len(x), len(y)])
    for i in range(len(x)):
        for j in range(len(y)):
            if i == j:
                dist_grid[i, j] = 100000
            else:
                dist_grid[i, j] = math.sqrt(
                    (x[i] - x[j])**2 + (y[i] - y[j])**2)
    return dist_grid
