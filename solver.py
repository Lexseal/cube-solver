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

def solve_single_thread(cube, max_move=22, rotation=0):
    solution = search.search(cube, max_move)
    return rotation, solution

rotation = 0
solution = []
pool = None
def solve(cube, max_move=22):
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

    max_move = 22
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
