import numpy as np
from collections import deque
import random
from copy import copy, deepcopy
from time import time
import os.path
import argparse
import rank
from cube_model import MoveSpace as MS
from cube_model import G1Space
import move_coord
import calc_move_table
import permute
import search

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--str", type=str, help="cube string")
parser.add_argument("-m", "--moves", type=str, help="cube scramble")
parser.add_argument("-d", "--display", action="store_true", help="print out solve")
parser.add_argument("-n", "--number", type=int, help="number of solves")
parser.add_argument("-c", "--camera", action="store_true", help="solve from camera")
args = parser.parse_args()

def print_move(move_num):
    for move in MS:
        if move_num == move:
            print(move)
            return

max_move = 23
num_of_shuffles = 100
num_of_solves = 1
one_solve = False
if args.number != None:
    num_of_solves = args.number

time_list = []
for n in range(num_of_solves):

    # iterative deepening depth-first search
    if args.str != None:
        init_state, init_cube = move_coord.cube_from_str(args.str)
        one_solve = True
    elif args.moves != None:
        init_state, init_cube = move_coord.cube_from_scramble(args.moves)
        one_solve = True
    elif args.camera:
        import recog_color
        cube_str = recog_color.scan()
        print(cube_str)
        init_state, init_cube = move_coord.cube_from_str(cube_str)
        one_solve = True
    else:
        init_state, shuffle_list, init_cube = move_coord.shuffle(num_of_shuffles)
    init_state.append(255) # use 255 to denote the -1st move
    init_state.append(0) # takes 0 moves to get there
    # init_state = [co_ori, eg_ori, ud_edges, last_move, depth]

    start_time = time()

    stage1_min = 0
    times_failed = 0
    solution_found = False
    solution = []

    last_move_lists = []
    while not solution_found:
        state = deepcopy(init_state)
        move_list1 = search.first_stage_search(state, stage1_min, last_move_lists)

        cube = deepcopy(init_cube)
        for move in move_list1:
            cube.move(move)
            #print_move(move)
        #print(list(cube.corners), list(cube.edges))

        state[0] = rank.co_perm(cube.get_co_perm())
        state[1] = rank.eg_perm(cube.get_eg_perm())
        state[2] = rank.ud_perm(cube.get_ud_perm())
        state[4] = 0 # depth is 0 to begin with
        stage2_max = max_move-len(move_list1)
        solution_found, move_list2 = search.second_stage_search(state, stage2_max)

        if solution_found:
            for move in move_list2:
                cube.move(move)
                #print_move(move)
            #print(list(cube.corners), list(cube.edges))
            solution = move_list1+move_list2
        else:
            times_failed += 1
            if stage1_min < 9:
                stage1_min += 1
            elif times_failed%7 == 0:
                stage1_min += 1
            stage1_min = min(stage1_min, 12) # can't be greater than 12

    if args.display:
        for move in solution:
            print_move(move)
    print("#", n+1, "total moves:", len(solution), "took", time() - start_time)
    time_list.append(time() - start_time)

    #for move in solution:
    #    init_cube.move(move)
    #print(init_cube)
    #print(list(init_cube.corners), list(init_cube.edges))
    
    if one_solve:
        break

print(sum(time_list)/len(time_list))
