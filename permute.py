from queue import SimpleQueue
import numpy as np
from time import time
import sys
from cube_model import MoveSpace as MS
from cube import Cube
from rank import rank_corners

def calc_corner_table():
    cube = Cube()
    queue = SimpleQueue()

    # optimization trick to use 11 as default value
    # works because all corner states can be achieved in 11 moves or fewer
    corner_table = bytearray([11]*88179840)

    cube.corners.append(255)
    queue.put(cube.corners)
    corner_table[0] = 0 # first entry is solved
    n = 0
    last_print = 0
    start_time = time()
    while queue.qsize() != 0:
        cur_state = queue.get() # pop
        move_count = corner_table[rank_corners(cur_state)] # get the move count up to this state

        last_move = cur_state[8]
        for move in MS:
            if move == last_move or \
                move//3 == last_move//3 and \
                abs(move-last_move) == 2:
                continue

            next_state = cur_state.copy() # get a copy of cur state
            cube.move_corners(next_state, move) # compute next state
            next_idx = rank_corners(next_state) # rank next state
            next_count = corner_table[next_idx] # get moves count
            if next_count > move_count+1:
                corner_table[next_idx] = move_count+1
                next_state[8] = move
                queue.put(next_state)
                n += 1

        if (n-last_print > 100000):
            last_print = n
            print(str(n//1000)+'k', str(queue.qsize()//1000)+'k', move_count, round((time()-start_time)/60, 2))

    np.save("corner_table", np.array(corner_table, dtype=np.int8))

def calc_edge_table1():
    cube = Cube()
    queue = SimpleQueue()

    # optimization trick to use 10 as default value
    # works because all 6 edge states can be achieved in 10 moves or fewer
    edge_table1 = bytearray([10]*42577920)

    cube.edges1.append(255)
    queue.put(cube.edges1)
    edge_table1[0] = 0 # first entry is solved
    n = 0
    last_print = 0
    start_time = time()
    while queue.qsize() != 0:
        cur_state = queue.get() # pop
        move_count = edge_table1[rank_edges(cur_state)] # get the move count up to this state

        last_move = cur_state[6]
        for move in MS:
            if move == last_move or \
                move//3 == last_move//3 and \
                abs(move-last_move) == 2:
                continue

            next_state = cur_state.copy() # get a copy of cur state
            cube.move_edges1(next_state, move) # compute next state
            next_idx = rank_edges(next_state) # rank next state
            next_count = edge_table1[next_idx] # get moves count
            if next_count > move_count+1:
                edge_table1[next_idx] = move_count+1
                next_state[6] = move
                queue.put(next_state)
                n += 1

        if (n-last_print > 100000):
            last_print = n
            print(str(n//1000)+'k', str(queue.qsize()//1000)+'k', move_count, round((time()-start_time)/60, 2))

    np.save("corner_table", np.array(edge_table1, dtype=np.int8))