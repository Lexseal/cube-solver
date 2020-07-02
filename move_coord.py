import numpy as np
import os.path
import random
from calc_move_table import MoveTable
import rank
from array import array
from sys import getsizeof

co_ori_table = np.load("table/co_ori_table.npy").tolist()
eg_ori_table = np.load("table/eg_ori_table.npy").tolist()
ud_edges_table = np.load("table/ud_edges_table.npy").tolist()

def stage1_move(state, move):
    return [co_ori_table[state[0]][move], eg_ori_table[state[1]][move], ud_edges_table[state[2]][move]]

co_perm_table = np.load("table/co_perm_table.npy").tolist()
eg_perm_table = np.load("table/eg_perm_table.npy").tolist()
ud_perm_table = np.load("table/ud_perm_table.npy").tolist()

def stage2_move(state, move):
    return [co_perm_table[state[0]][move], eg_perm_table[state[1]][move], ud_perm_table[state[2]][move]]

def verify():
    cube = MoveTable()
    move_list = cube.shuffle_G1(1000)

    expected_co_perm = rank.co_perm(cube.get_co_perm())
    expected_eg_perm = rank.eg_perm(cube.get_eg_perm())
    expected_ud_perm = rank.ud_perm(cube.get_ud_perm())

    state = array('I', [0, 0, 0]) # a new cube
    #print(getsizeof(state))
    for move in move_list:
        state = stage2_move(state, move)
    
    print(expected_co_perm, expected_eg_perm, expected_ud_perm)
    print(state)
    #print(getsizeof(state))

if __name__ == "__main__":
    verify()
    pass