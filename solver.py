import numpy as np
from collections import deque
import random
from copy import copy
from cube import Cube
import rank
from cube_model import MoveSpace as MS
from cube_model import G1Space
import move_coord
from calc_move_table import MoveTable

def print_move(move_num):
    for move in MS:
        if move_num == move:
            print(move)
            return

# load tables
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

# iterative deepening depth-first search
state, shuffle_list, cube = move_coord.shuffle(200)
state.append(255) # use 255 to denote the -1st move
state.append(0) # takes 0 moves to get there
# state = [co_ori, eg_ori, ud_edges, last_move, depth]

move_list1 = []
first_phase_complete = False
for max_depth in range(0, 13):
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
                print("victory", cur_depth)
                for _ in range(cur_depth):
                    move_list1.insert(0, move_stack.pop())
                first_phase_complete = True
                break
        else:
            move_space = bytearray(MS)
            random.shuffle(move_space)
            for move in move_space:
                cur_face = move//3
                last_face = last_move//3
                if cur_face == last_face: continue
                elif cur_face == 3 and last_face == 1: continue
                elif cur_face == 4 and last_face == 2: continue
                elif cur_face == 5 and last_face == 0: continue

                new_state = copy(cur_state)
                move_coord.stage1_move(new_state, move)
                new_state[3] = move
                next_depth = cur_depth+1
                new_state[4] = next_depth

                # add if within the search range
                if next_depth + h1(new_state) <= max_depth:
                    state_stack.append(new_state)
    if first_phase_complete: break
    print("level", max_depth, "done")

for move in move_list1:
    cube.move(move)
    print_move(move)
print(list(cube.corners), list(cube.edges))

state[0] = rank.co_perm(cube.get_co_perm())
state[1] = rank.eg_perm(cube.get_eg_perm())
state[2] = rank.ud_perm(cube.get_ud_perm())
state[4] = 0 # depth is 0 to begin with
move_list2 = []
second_phase_complete = False
for max_depth in range(0, 19):
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
                print("victory", cur_depth)
                for _ in range(cur_depth):
                    move_list2.insert(0, move_stack.pop())
                second_phase_complete = True
                break
        else:
            move_space = bytearray(G1Space)
            random.shuffle(move_space)
            for move in move_space:
                cur_face = move//3
                last_face = last_move//3
                if cur_face == last_face: continue
                elif cur_face == 3 and last_face == 1: continue
                elif cur_face == 4 and last_face == 2: continue
                elif cur_face == 5 and last_face == 0: continue

                new_state = copy(cur_state)
                move_coord.stage2_move(new_state, move)
                new_state[3] = move
                next_depth = cur_depth+1
                new_state[4] = next_depth

                # add if within the search range
                if next_depth + h2(new_state) <= max_depth:
                    state_stack.append(new_state)
    if second_phase_complete: break
    print("level", max_depth, "done")

for move in move_list2:
    cube.move(move)
    print_move(move)
print(list(cube.corners), list(cube.edges))