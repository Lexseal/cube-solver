from time import time
import sys
import array

start_time = time()
arr1 = []
arr2 = array()
for i, itm in enumerate(arr):
    if itm > 10:
        print(i, itm)
print(time()-start_time)
