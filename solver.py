import numpy as np
import random
from copy import copy, deepcopy
from time import time
import argparse
import multiprocessing
import rank
from cube_model import MoveSpace as MS
import move_coord
import search

"""
Handles user input and constructs 3 search threads.
Each thread has a different cube that is rotated at 120 degree
from one another on the xz axis
"""

def print_move(move_num):
    for move in MS:
        if move_num == move:
            print(move)
            return

def deposit_result(result):
    global solution
    global pool
    global rotation
    rotation, solution = result
    pool.terminate()

def solve(init_cube, init_state, max_move=23, rotation=0):
    stage1_min = 0
    times_failed = 0
    solution_found = False
    while not solution_found:
        move_list1 = search.first_stage_search(init_state, stage1_min)
        stage1_min = len(move_list1) # set min depth

        # move the original cube to G1 state
        cube = deepcopy(init_cube)
        for move in move_list1:
            cube.move(move)
            #print_move(move)
        #print(list(cube.corners), list(cube.edges))
        #print("second stage started", stage1_min, max_move-len(move_list1))

        init_state2 = []
        init_state2.append(rank.co_perm(cube.get_co_perm()))
        init_state2.append(rank.eg_perm(cube.get_eg_perm()))
        init_state2.append(rank.ud_perm(cube.get_ud_perm())) # coords
        init_state2.append(move_list1[-1]) # last move
        init_state2.append(0) # takes 0 moves 

        stage2_max = max_move-len(move_list1)

        solution_found, move_list2 = search.second_stage_search(init_state2, stage2_max)

        if solution_found:
            '''for move in move_list2:
                cube.move(move)
                print_move(move)
            print(list(cube.corners), list(cube.edges))'''
            return rotation, move_list1+move_list2
        else:
            times_failed += 1
            if stage1_min < 9:
                stage1_min += 1
            elif times_failed%7 == 0:
                stage1_min = min(stage1_min+1, 12) # can't be greater than 12

global rotation
global solution
global pool
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--str", type=str, help="cube string")
    parser.add_argument("-m", "--moves", type=str, help="cube scramble")
    parser.add_argument("-d", "--display", action="store_true", help="print out solve")
    parser.add_argument("-n", "--number", type=int, help="number of solves")
    parser.add_argument("-c", "--camera", action="store_true", help="solve from camera")
    parser.add_argument("-nm", "--numeric_move", type=str, help="solve from a numerical scrmable")
    args = parser.parse_args()

    max_move = 23
    num_of_shuffles = 100
    num_of_solves = 1
    if args.number != None:
        num_of_solves = args.number
    time_list = []
    global solution
    solution = []
    for n in range(num_of_solves):

        # iterative deepening depth-first search
        if args.str != None:
            init_state, init_cube = move_coord.cube_from_str(args.str)
        elif args.moves != None:
            init_state, init_cube = move_coord.cube_from_scramble(args.moves)
        elif args.numeric_move != None:
            init_state, init_cube = move_coord.cube_from_scramble(args.numeric_move, numeric_scramble=True)
        elif args.camera:
            import recog_color
            cube_str = recog_color.scan()
            print(cube_str)
            init_state, init_cube = move_coord.cube_from_str(cube_str)
        else:
            init_state, shuffle_list, init_cube = move_coord.shuffle(num_of_shuffles)
        # init_state = [co_ori, eg_ori, ud_edges, last_move, depth]

        global pool
        pool = multiprocessing.Pool()
        start_time = time()
        for i in range(3): # do 6 transformations
            cube = deepcopy(init_cube)
            for _ in range(i): # rotate
                cube.rotate_z()
                cube.rotate_x_rev()
            state = copy(init_state)
            state[0] = rank.co_ori(cube.get_co_ori())
            state[1] = rank.eg_ori(cube.get_eg_ori())
            state[2] = rank.ud_edges(cube.get_ud_edges())
            param = [cube, state, max_move, i]
            pool.apply_async(solve, param, callback=deposit_result)
        pool.close()
        pool.join()

        print("#", n+1, "rot:", rotation, "total moves:", len(solution), "took", time() - start_time)
        time_list.append(time() - start_time)
        
        if args.display:
            for move in solution:
                print_move(move)

        #for move in solution:
        #    init_cube.move(move)
        #print(init_cube)
        #print(list(init_cube.corners), list(init_cube.edges))

    print("Avg time:", sum(time_list)/len(time_list))
