from permutation import Permutation
from time import time
import numpy as np

def rank_corners(pos):
    '''
    Position should be 8 distinct numbers from 0 to 23
    '''
    return 2187*(Permutation(pos[0]%8+1, \
        pos[1]%8+1, \
            pos[2]%8+1, \
                pos[3]%8+1, \
                    pos[4]%8+1, \
                        pos[5]%8+1, \
                            pos[6]%8+1, \
                                pos[7]%8+1).lehmer(8)) + \
        pos[0]//8*729 + \
            pos[1]//8*243 + \
                pos[2]//8*81 + \
                    pos[3]//8*27 + \
                        pos[4]//8*9 + \
                            pos[5]//8*3 + \
                                pos[6]//8

if __name__ == "__main__":
    start_time = time()
    arr = np.zeros(100000000)
    for i in range(1000000):
        arr[i] = i
        arr[i]+1
    print(time()-start_time)
    pass