from permutation import Permutation
from itertools import permutations
from time import time
import numpy as np

def h2_corners(cor):
    return Permutation(cor[0]%8+1, \
        cor[1]%8+1, \
            cor[2]%8+1, \
                cor[3]%8+1, \
                    cor[4]%8+1, \
                        cor[5]%8+1, \
                            cor[6]%8+1, \
                                cor[7]%8+1).lehmer(8)

def h2_edges(eg):
    pos = [eg[0]%12, eg[1]%12, eg[2]%12, eg[3]%12, eg[4]%12, eg[5]%12]
    a0 = 55440*pos[0]

    subtract = 0
    if pos[0] < pos[1]:
        subtract += 1
    a1 = 5040*(pos[1]-subtract)

    subtract = 0
    if pos[0] < pos[2]:
        subtract += 1
    if pos[1] < pos[2]:
        subtract += 1
    a2 = 504*(pos[2]-subtract)

    subtract = 0
    if pos[0] < pos[3]:
        subtract += 1
    if pos[1] < pos[3]:
        subtract += 1
    if pos[2] < pos[3]:
        subtract += 1
    a3 = 56*(pos[3]-subtract)

    subtract = 0
    if pos[0] < pos[4]:
        subtract += 1
    if pos[1] < pos[4]:
        subtract += 1
    if pos[2] < pos[4]:
        subtract += 1
    if pos[3] < pos[4]:
        subtract += 1
    a4 = 7*(pos[4]-subtract)

    subtract = 0
    if pos[0] < pos[5]:
        subtract += 1
    if pos[1] < pos[5]:
        subtract += 1
    if pos[2] < pos[5]:
        subtract += 1
    if pos[3] < pos[5]:
        subtract += 1
    if pos[4] < pos[5]:
        subtract += 1
    a5 = pos[5]-subtract

    return a0+a1+a2+a3+a4+a5


def rank_corners(cor):
    '''
    cor should be 8 distinct numbers from 0 to 23
    '''
    return 2187*(Permutation(cor[0]%8+1, \
        cor[1]%8+1, \
            cor[2]%8+1, \
                cor[3]%8+1, \
                    cor[4]%8+1, \
                        cor[5]%8+1, \
                            cor[6]%8+1, \
                                cor[7]%8+1).lehmer(8)) + \
        cor[0]//8*729 + \
            cor[1]//8*243 + \
                cor[2]//8*81 + \
                    cor[3]//8*27 + \
                        cor[4]//8*9 + \
                            cor[5]//8*3 + \
                                cor[6]//8

def rank_edges(eg):
    '''
    eg should contain 6 distinct numbers from 0 to 23
    '''
    pos = [eg[0]%12, eg[1]%12, eg[2]%12, eg[3]%12, eg[4]%12, eg[5]%12]
    ori = [eg[0]//12, eg[1]//12, eg[2]//12, eg[3]//12, eg[4]//12, eg[5]//12]

    a0 = 55440*pos[0]

    subtract = 0
    if pos[0] < pos[1]:
        subtract += 1
    a1 = 5040*(pos[1]-subtract)

    subtract = 0
    if pos[0] < pos[2]:
        subtract += 1
    if pos[1] < pos[2]:
        subtract += 1
    a2 = 504*(pos[2]-subtract)

    subtract = 0
    if pos[0] < pos[3]:
        subtract += 1
    if pos[1] < pos[3]:
        subtract += 1
    if pos[2] < pos[3]:
        subtract += 1
    a3 = 56*(pos[3]-subtract)

    subtract = 0
    if pos[0] < pos[4]:
        subtract += 1
    if pos[1] < pos[4]:
        subtract += 1
    if pos[2] < pos[4]:
        subtract += 1
    if pos[3] < pos[4]:
        subtract += 1
    a4 = 7*(pos[4]-subtract)

    subtract = 0
    if pos[0] < pos[5]:
        subtract += 1
    if pos[1] < pos[5]:
        subtract += 1
    if pos[2] < pos[5]:
        subtract += 1
    if pos[3] < pos[5]:
        subtract += 1
    if pos[4] < pos[5]:
        subtract += 1
    a5 = pos[5]-subtract

    return (a0+a1+a2+a3+a4+a5)*64 + ori[0]*32 + ori[1]*16 + \
        ori[2]*8 + ori[3]*4 + ori[4]*2 + ori[5]

if __name__ == "__main__":
    print(h2_corners([7, 6, 5, 4, 3, 2, 1, 0]))
    '''start_time = time()
    perm = permutations(list(range(12)), 6)
    n = 0
    for itm in list(perm):
        itm = list(itm)
        #print(itm)
        for ori in range(64):
            binary = list(str(bin(ori))[2:])
            compensation = 6-len(binary)
            binary = ([0]*compensation)+binary
            #print(binary)
            eg = itm.copy()
            for i, bi in enumerate(binary):
                eg[i] += 12*int(bi)
            print(eg, rank_edges(eg))
            n+=1
            if n > 665280:
                exit()
    print(time()-start_time)
    pass'''