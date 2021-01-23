import numpy as np
import os.path
import random
from array import array
from cube import Cube
from calc_move_table import MoveTable
import rank
from cube_model import MoveSpace as MS

"""
This file moves the cube in the coordinate level according to the move table
"""

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

def stage1_coord(cube):
    co_ori   = rank.co_ori(cube.get_co_ori())
    eg_ori   = rank.eg_ori(cube.get_eg_ori())
    ud_edges = rank.ud_edges(cube.get_ud_edges())
    state = array('I', [co_ori, eg_ori, ud_edges])
    state.append(255) # use 255 to denote the -1st move
    state.append(0) # takes 0 moves to get there
    return state

def stage2_coord(cube):
    co_perm = rank.co_perm(cube.get_co_perm())
    eg_perm = rank.eg_perm(cube.get_eg_perm())
    ud_perm = rank.ud_perm(cube.get_ud_perm())
    state = array('I', [co_perm, eg_perm, ud_perm])
    state.append(255) # use 255 to denote the -1st move
    state.append(0) # takes 0 moves to get there
    return state

def shuffle(N):
    cube = Cube()
    move_list = cube.shuffle(N)
    return move_list, cube

def cube_from_str(cube_str):
    return Cube(cube_str=cube_str)

def cube_from_scramble(scramble, numeric_scramble=False):
    return Cube(cube_scramble=scramble, numeric_scramble=numeric_scramble)

def verify():
    cube = Cube()
    move_list = cube.shuffle(1000)

    expected_co_ori = rank.co_ori(cube.get_co_ori())
    expected_eg_ori = rank.eg_ori(cube.get_eg_ori())
    expected_ud_edges = rank.ud_edges(cube.get_ud_edges())

    state = array('I', [0, 0, 0]) # a new cube
    for move in move_list:
        stage1_move(state, move)
    
    print(expected_co_ori, expected_eg_ori, expected_ud_edges)
    print(state)

if __name__ == "__main__":
    verify()
    pass