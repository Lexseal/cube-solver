import numpy as np
import os.path
import random
from array import array
from calc_move_table import MoveTable
import rank
from cube_model import MoveSpace as MS


def print_move(move_num):
    for move in MS:
        if move_num == move:
            print(move)
            return

if not os.path.exists("table/co_ori_table.npy") or\
    not os.path.exists("table/eg_ori_table.npy") or\
    not os.path.exists("table/ud_edges_table.npy") or\
    not os.path.exists("table/co_perm_table.npy") or\
    not os.path.exists("table/eg_perm_table.npy") or\
    not os.path.exists("table/ud_perm_table.npy"):
    print("making move tables...")
    move_table = MoveTable()
    move_table.make_tables()

co_ori_table = np.load("table/co_ori_table.npy").tolist()
eg_ori_table = np.load("table/eg_ori_table.npy").tolist()
ud_edges_table = np.load("table/ud_edges_table.npy").tolist()

def stage1_move(state, move):
    state[0] = co_ori_table[state[0]][move]
    state[1] = eg_ori_table[state[1]][move]
    state[2] = ud_edges_table[state[2]][move]

co_perm_table = np.load("table/co_perm_table.npy").tolist()
eg_perm_table = np.load("table/eg_perm_table.npy").tolist()
ud_perm_table = np.load("table/ud_perm_table.npy").tolist()

def stage2_move(state, move):
    state[0] = co_perm_table[state[0]][move]
    state[1] = eg_perm_table[state[1]][move]
    state[2] = ud_perm_table[state[2]][move]

def shuffle(N):
    cube = MoveTable()
    move_list = cube.shuffle(N)
    #for move in move_list:
    #    print_move(move)

    co_ori = rank.co_ori(cube.get_co_ori())
    eg_ori = rank.eg_ori(cube.get_eg_ori())
    ud_edges = rank.ud_edges(cube.get_ud_edges())

    return array('I', [co_ori, eg_ori, ud_edges]), move_list, cube

def verify():
    cube = MoveTable()
    move_list = cube.shuffle(1000)

    expected_co_ori = rank.co_ori(cube.get_co_ori())
    expected_eg_ori = rank.eg_ori(cube.get_eg_ori())
    expected_ud_edges = rank.ud_edges(cube.get_ud_edges())

    state = array('I', [0, 0, 0]) # a new cube
    #print(getsizeof(state))
    for move in move_list:
        stage1_move(state, move)
    
    print(expected_co_ori, expected_eg_ori, expected_ud_edges)
    print(state)
    #print(getsizeof(state))

if __name__ == "__main__":
    verify()
    pass