from queue import SimpleQueue
import numpy as np
from time import time
import random
from array import array
from copy import copy
import cube_model
from cube import Cube
import rank
from move_coord import stage1_move, stage2_move

"""
Permutes through most of the cube positions in the coordinate level to
calculate a pruning table.
"""

def calc_stage1_corners_ud():
    # stage 1 can be completed in 12 moves or fewer
    stage1_corners_ud = bytearray([12]*cube_model.StateSize.CO_ORI*cube_model.StateSize.UD_COMB)
    stage1_corners_ud[0] = 0 # first entry is solved so takes 0 move to get to

    # [co_ori, eg_ori, ud_edges, last_move]
    state = array('I', [0, 0, 0, 255]) # a new cube
    queue = SimpleQueue()
    queue.put(state)

    n = 0
    last_print = 0
    start_time = time() # logs
    while queue.qsize() > 0:
        cur_state = queue.get() # pop
        cur_idx = cur_state[0]*cube_model.StateSize.UD_COMB + cur_state[2]
        move_count = stage1_corners_ud[cur_idx] # get the move count up to this state

        last_move = cur_state[3]
        for move in cube_model.MoveSpace:
            cur_face = move//3
            last_face = last_move//3
            if cur_face == last_face: continue
            elif cur_face == 3 and last_face == 1: continue
            elif cur_face == 4 and last_face == 2: continue
            elif cur_face == 5 and last_face == 0: continue

            next_state = copy(cur_state) # get a copy of cur state
            stage1_move(next_state, move) # compute next state

            next_idx = next_state[0]*cube_model.StateSize.UD_COMB + next_state[2]
            next_count = stage1_corners_ud[next_idx] # get moves count
            if next_count > move_count+1:
                stage1_corners_ud[next_idx] = move_count+1
                next_state[3] = move
                queue.put(next_state)
                n += 1

        if (n-last_print > 100):
            last_print = n
            print(n, str(queue.qsize()//1000)+'k', move_count, round((time()-start_time)/60, 2))
    print(n)
    np.save("table/stage1_corners", np.array(stage1_corners_ud, dtype=np.uint8))

def calc_stage1_edges_ud():
    # works because stage 1 can be completed in 12 moves or fewer
    stage1_edges = bytearray([12]*cube_model.StateSize.EG_ORI*cube_model.StateSize.UD_COMB)
    stage1_edges[0] = 0 # first entry is solved so takes 0 move to get to

    # [co_ori, eg_ori, ud_edges, last_move]
    state = array('I', [0, 0, 0, 255]) # a new cube
    queue = SimpleQueue()
    queue.put(state)

    n = 0
    last_print = 0
    start_time = time() # logs
    while queue.qsize() > 0:
        cur_state = queue.get() # pop
        cur_idx = cur_state[1]*cube_model.StateSize.UD_COMB + cur_state[2]
        move_count = stage1_edges[cur_idx] # get the move count up to this state

        last_move = cur_state[3]
        for move in cube_model.MoveSpace:
            cur_face = move//3
            last_face = last_move//3
            if cur_face == last_face: continue
            elif cur_face == 3 and last_face == 1: continue
            elif cur_face == 4 and last_face == 2: continue
            elif cur_face == 5 and last_face == 0: continue

            next_state = copy(cur_state) # get a copy of cur state
            stage1_move(next_state, move) # compute next state

            next_idx = next_state[1]*cube_model.StateSize.UD_COMB + next_state[2]
            next_count = stage1_edges[next_idx] # get moves count
            if next_count > move_count+1:
                stage1_edges[next_idx] = move_count+1
                next_state[3] = move
                queue.put(next_state)
                n += 1

        if (n-last_print > 1000):
            last_print = n
            print(n, str(queue.qsize()//1000)+'k', move_count, round((time()-start_time)/60, 2))
    print(n)
    np.save("table/stage1_edges", np.array(stage1_edges, dtype=np.uint8))

def calc_stage2_corners_ud():
    # stage 2 can be completed in 18 moves or fewer
    stage2_corners_ud = bytearray([18]*cube_model.StateSize.CO_PERM*cube_model.StateSize.UD_PERM)
    stage2_corners_ud[0] = 0 # first entry is solved so takes 0 move to get to

    # [co_perm, eg_perm, ud_perm, last_move]
    state = array('I', [0, 0, 0, 255]) # a new cube
    queue = SimpleQueue()
    queue.put(state)

    n = 0
    last_print = 0
    start_time = time() # logs
    while queue.qsize() > 0:
        cur_state = queue.get() # pop
        cur_idx = cur_state[0]*cube_model.StateSize.UD_PERM + cur_state[2]
        move_count = stage2_corners_ud[cur_idx] # get the move count up to this state

        last_move = cur_state[3]
        for move in cube_model.G1Space: # we don't use the entire move space
            cur_face = move//3
            last_face = last_move//3
            if cur_face == last_face: continue
            elif cur_face == 3 and last_face == 1: continue
            elif cur_face == 4 and last_face == 2: continue
            elif cur_face == 5 and last_face == 0: continue

            next_state = copy(cur_state) # get a copy of cur state
            stage2_move(next_state, move) # compute next state

            next_idx = next_state[0]*cube_model.StateSize.UD_PERM + next_state[2]
            next_count = stage2_corners_ud[next_idx] # get moves count
            if next_count > move_count+1:
                stage2_corners_ud[next_idx] = move_count+1
                next_state[3] = move
                queue.put(next_state)
                n += 1

        if (n-last_print > 1000):
            last_print = n
            print(n, str(queue.qsize()//1000)+'k', move_count, round((time()-start_time)/60, 2))
    print(n)
    np.save("table/stage2_corners", np.array(stage2_corners_ud, dtype=np.uint8))

def calc_stage2_egdes_ud():
    # stage 2 can be completed in 18 moves or fewer
    stage2_edges_ud = bytearray([18]*cube_model.StateSize.EG_PERM*cube_model.StateSize.UD_PERM)
    stage2_edges_ud[0] = 0 # first entry is solved so takes 0 move to get to

    # [co_perm, eg_perm, ud_perm, last_move]
    state = array('I', [0, 0, 0, 255]) # a new cube
    queue = SimpleQueue()
    queue.put(state)

    n = 0
    last_print = 0
    start_time = time() # logs
    while queue.qsize() > 0:
        cur_state = queue.get() # pop
        cur_idx = cur_state[1]*cube_model.StateSize.UD_PERM + cur_state[2]
        move_count = stage2_edges_ud[cur_idx] # get the move count up to this state

        last_move = cur_state[3]
        for move in cube_model.G1Space: # we don't use the entire move space
            cur_face = move//3
            last_face = last_move//3
            if cur_face == last_face: continue
            elif cur_face == 3 and last_face == 1: continue
            elif cur_face == 4 and last_face == 2: continue
            elif cur_face == 5 and last_face == 0: continue

            next_state = copy(cur_state) # get a copy of cur state
            stage2_move(next_state, move) # compute next state

            next_idx = next_state[1]*cube_model.StateSize.UD_PERM + next_state[2]
            next_count = stage2_edges_ud[next_idx] # get moves count
            if next_count > move_count+1:
                stage2_edges_ud[next_idx] = move_count+1
                next_state[3] = move
                queue.put(next_state)
                n += 1

        if (n-last_print > 1000):
            last_print = n
            print(n, str(queue.qsize()//1000)+'k', move_count, round((time()-start_time)/60, 2))
    print(n)
    np.save("table/stage2_edges", np.array(stage2_edges_ud, dtype=np.uint8))

if __name__ == "__main__":
    calc_stage1_corners_ud()
    calc_stage1_edges_ud()
    calc_stage2_corners_ud()
    calc_stage2_egdes_ud()
    pass