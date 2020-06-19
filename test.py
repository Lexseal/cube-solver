from time import time
import sys
import numpy as np

start_time = time()
arr = np.load("edge_table2.npy")
for i, itm in enumerate(arr):
    if itm > 10:
        print(i, itm)
print(time()-start_time)
