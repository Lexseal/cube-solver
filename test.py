from time import time
import sys

start_time = time()
for i in range(1000000):
    arr = list(range(min(256, i)))
print(time()-start_time)
