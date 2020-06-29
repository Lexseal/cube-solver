from permutation import Permutation
from itertools import permutations
from time import time
import numpy as np
import math

def co_ori(co_ori):
    '''
    co_perm_ori 8-bit ternary, but only the first 7 bits are used
    '''
    rank = 0
    for i in range(7):
        rank += co_ori[i]*(3**(6-i))
    return rank

def co_ori_inv(rank):
    '''
    0 <= rank < 3^7
    '''
    rank = np.base_repr(rank, base=3)
    co_ori = bytearray([0]*8)

    start = 7-len(rank)
    for i in range(start, 7):
        co_ori[i] = int(rank[i-start])
    
    co_ori[7] = (3-sum(co_ori)%3)%3
    return co_ori

def eg_ori(eg_ori):
    '''
    eg_ori is a 12-bit binary, but only the first 11 bits are used
    '''
    rank = 0
    for i in range(11):
        rank += eg_ori[i]*(2**(10-i))
    return rank

def eg_ori_inv(rank):
    '''
    0 <= rank < 2^11
    '''
    rank = np.base_repr(rank, base=2)
    eg_ori = bytearray([0]*12)

    start = 11-len(rank)
    for i in range(start, 11):
        eg_ori[i] = int(rank[i-start])
    eg_ori[11] = (2-sum(eg_ori)%2)%2
    return eg_ori

def ud_edges(egs):
    '''
    egs is a set of 12 numbers ranging from 0 to 11
    we are only interested in entries that are bigger than 7
    '''
    start = False
    k = -1
    sum = 0
    for n, eg in enumerate(egs):
        if eg >= 8:
            start = True
            k += 1
        elif start:
            sum += math.comb(n, k)
    return sum

def ud_edges_inv(rank):
    k = 3
    egs = [0]*12
    for n in reversed(range(12)):
        n_choose_k = math.comb(n, k)
        if rank-n_choose_k >= 0:
            rank -= n_choose_k
        else:
            egs[n] = 8+k
            k -= 1
            if k < 0:
                break
    return egs

def co_perm(co_perm):
    '''
    co_perm is a permutation of 0-7
    '''
    return Permutation(*[i+1 for i in co_perm]).lehmer(8)

def co_perm_inv(rank):
    return [i-1 for i in (Permutation.from_lehmer(rank, 8)).to_image(8)]

def eg_perm(eg_perm):
    '''
    eg_perm is a permutation of 0-7, so same as corners
    '''
    return Permutation(*[i+1 for i in eg_perm]).lehmer(8)

def eg_perm_inv(rank):
    return [i-1 for i in (Permutation.from_lehmer(rank, 8)).to_image(8)]

def ud_perm(ud_perm):
    '''
    We treat ud_perm as a permutation of 0-3
    '''
    return Permutation(*[i-7 for i in ud_perm]).lehmer(4)

def ud_perm_inv(rank):
    return [i+7 for i in (Permutation.from_lehmer(rank, 4)).to_image(4)]

if __name__ == "__main__":
    for i in range(24):
        print(ud_perm(ud_perm_inv(i)))
    #print(h2_co_permners([7, 6, 5, 4, 3, 2, 1, 0]))