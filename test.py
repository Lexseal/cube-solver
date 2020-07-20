from time import time
import sys
import array
import numpy as np

start_time = time()
table = np.load("table/stage1_edges.npy")
for i, itm in enumerate(table):
    if itm >= 10:
        print(i, itm)
print(time()-start_time)