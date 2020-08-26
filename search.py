import random
from collections import deque
import numpy as np
import os.path
from copy import copy
from cube_model import MoveSpace as MS
from cube_model import G1Space
import move_coord
import calc_move_table
import permute
import rank

# load tables
if not os.path.exists("table/stage1_corners.npy") or\
    not os.path.exists("table/stage1_edges.npy") or\
    not os.path.exists("table/stage2_corners.npy") or\
    not os.path.exists("table/stage2_edges.npy"):
    print("making pruning tables...")
    permute.calc_stage1_corners()
    permute.calc_stage1_edges()
    permute.calc_stage2_corners()
    permute.calc_stage2_egdes()
    print("table finished. please run the program again")
    exit(0)

stage1_corners = bytearray(np.load("table/stage1_corners.npy"))
stage1_edges = bytearray(np.load("table/stage1_edges.npy"))
stage2_corners = bytearray(np.load("table/stage2_corners.npy"))
stage2_edges = bytearray(np.load("table/stage2_edges.npy"))

def h1(state):
    co_idx = state[0]
    eg_idx = state[1]*495+state[2]
    return max(stage1_corners[co_idx], stage1_edges[eg_idx])

def h2(state):
    co_idx = state[0]
    eg_idx = state[1]*24+state[2]
    return max(stage2_corners[co_idx], stage2_edges[eg_idx])

def is_goal(state):
    return state[0] == 0 and state[1] == 0 and state[2] == 0

def first_stage_search(state, stage1_min):
    move_list1 = []
    for max_depth in range(stage1_min, 13):
        state_stack = deque()
        move_stack = deque()

        state_stack.append(state)
        while len(state_stack) > 0:
            cur_state = state_stack.pop()
            cur_depth = cur_state[4] # get the depth of the state
            while (len(move_stack) > cur_depth):
                move_stack.pop()

            last_move = cur_state[3]
            move_stack.append(last_move)

            if cur_depth == max_depth:
                if is_goal(cur_state):
                    move_list1 = list(move_stack)[1:cur_depth+1]
                    #print("stage1 victory", cur_depth+1)
                    return move_list1
                continue
            
            move_space = bytearray(MS)
            random.shuffle(move_space)
            last_face = last_move//3
            for move in move_space:
                cur_face = move//3
                if cur_face == last_face: continue
                elif cur_face == 3 and last_face == 1: continue
                elif cur_face == 4 and last_face == 2: continue
                elif cur_face == 5 and last_face == 0: continue

                new_state = copy(cur_state)
                move_coord.stage1_move(new_state, move)
                next_depth = cur_depth+1
                # add if within the search range
                if next_depth + h1(new_state) <= max_depth:
                    new_state[3] = move # update last move
                    new_state[4] = next_depth # update depth
                    state_stack.append(new_state)
        #print("level", max_depth, "done")
    return [] # empty list as placeholer

def second_stage_search(state, stage2_max):
    move_list2 = []
    for max_depth in range(0, stage2_max+1):
        state_stack = deque()
        move_stack = deque()

        state_stack.append(state)
        while len(state_stack) > 0:
            cur_state = state_stack.pop()
            cur_depth = cur_state[4] # get the depth of the state
            while (len(move_stack) > cur_depth):
                move_stack.pop()

            last_move = cur_state[3]
            move_stack.append(last_move)

            if cur_depth == max_depth:
                if is_goal(cur_state):
                    #print("stage2 victory", cur_depth)
                    move_list2 = list(move_stack)[1:cur_depth+1]
                    return True, move_list2
                continue
            
            move_space = bytearray(G1Space)
            random.shuffle(move_space)
            last_face = last_move//3
            for move in move_space:
                cur_face = move//3
                if cur_face == last_face: continue
                elif cur_face == 3 and last_face == 1: continue
                elif cur_face == 4 and last_face == 2: continue
                elif cur_face == 5 and last_face == 0: continue

                new_state = copy(cur_state)
                move_coord.stage2_move(new_state, move)
                next_depth = cur_depth+1
                # add if within the search range
                if next_depth + h2(new_state) <= max_depth:
                    new_state[3] = move # update last move
                    new_state[4] = next_depth # update depth
                    state_stack.append(new_state)
        #print("level", max_depth, "done")
    return False, [] # not found