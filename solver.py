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

def rotate_moves(move_list):
    ''' F->L L->U U->F -3
        B->R R->D D->B -3 '''
    for i, move in enumerate(move_list):
        if move < 9:
            move_list[i] = (move-3)%9
        else:
            move -= 9
            move = (move-3)%9
            move += 9
            move_list[i] = move       

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

def solve_single_thread(cube, max_move=23, rotation=0):
    stage1_min = 0
    times_failed = 0
    solution_found = False
    # state1 = [co_ori, eg_ori, ud_edges, last_move, depth]
    state1 = move_coord.stage1_coord(cube) # stage 1 cube represented by 3 coordinates
    while not solution_found:
        move_list1 = search.first_stage_search(state1, stage1_min)
        stage1_min = len(move_list1) # set min depth

        # here we need a copy of the original cube because we can't guarentee a solution
        tmp_cube = deepcopy(cube)
        for move in move_list1:
            tmp_cube.move(move)
            #print_move(move)
        # print(list(tmp_cube.corners), list(tmp_cube.edges))

        #print("second stage started", stage1_min, max_move-len(move_list1))
        # state2 = [co_perm, eg_perm, ud_perm, last_move, depth]
        state2 = move_coord.stage2_coord(tmp_cube)
        if len(move_list1) > 0:
            state2[-2] = move_list1[-1] # in this case we know what the last move is

        stage2_max = max_move-len(move_list1) # subtract the moves used by moving to G1

        solution_found, move_list2 = search.second_stage_search(state2, stage2_max)

        if solution_found:
            '''for move in move_list2:
                cube.move(move)
                print_move(move)
            print(list(cube.corners), list(cube.edges))'''
            return rotation, move_list1+move_list2
        else: # huristics to make stage1 solution longer so stage2 will be easier
            times_failed += 1
            if stage1_min < 9:
                stage1_min += 1
            elif times_failed%7 == 0:
                stage1_min = min(stage1_min+1, 12) # can't be greater than 12

rotation = 0
solution = []
pool = None
def solve(cube, max_move=23):
    global solution
    global pool
    global rotation # declare global
    pool = multiprocessing.Pool()
    for i in range(3): # do 3 transformations
        rot_cube = deepcopy(cube)
        for _ in range(i): # rotate
            rot_cube.rotate_z()
            for _ in range(3):
                rot_cube.rotate_x_rev() # 3 reverse is 1 forward
        #print(rot_cube)
        param = [rot_cube, max_move, i]
        pool.apply_async(solve_single_thread, param, callback=deposit_result)
    pool.close()
    pool.join()

    for _ in range(rotation): # we need to rotate the solution back
        rotate_moves(solution)

    # print(cube)
    # for move in solution:
    #    cube.move(move)
    # print(cube)
    # print(list(cube.corners), list(cube.edges))

    return solution

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
    for n in range(num_of_solves):
        if args.str != None:
            init_cube = move_coord.cube_from_str(args.str)
        elif args.moves != None:
            init_cube = move_coord.cube_from_scramble(args.moves)
        elif args.numeric_move != None:
            init_cube = move_coord.cube_from_scramble(args.numeric_move, numeric_scramble=True)
        elif args.camera:
            import recog_color
            cube_str = recog_color.scan()
            print(cube_str)
            init_cube = move_coord.cube_from_str(cube_str)
        else:
            shuffle_list, init_cube = move_coord.shuffle(num_of_shuffles)
        
        start_time = time()
        solution = solve(init_cube, max_move)

        print("#", n+1, "rot:", rotation, "total moves:", len(solution), "took", time() - start_time)
        time_list.append(time() - start_time)
        
        if args.display:
            print(init_cube)
            for move in solution:
                print_move(move)

    print("Avg time:", sum(time_list)/len(time_list))
