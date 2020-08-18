import numpy as np
import random
from copy import deepcopy
from time import time
import argparse
import multiprocessing
import rank
from cube_model import MoveSpace as MS
from cube_model import G1Space
import move_coord
import search

def stage1_result(result):
    global move_list1
    global pool
    move_list1 = result
    pool.terminate()

def stage2_result(result):
    global move_list2
    global pool
    global solution_found
    solution_found, move_list2 = result
    if solution_found:
        pool.terminate()

def print_move(move_num):
    for move in MS:
        if move_num == move:
            print(move)
            return

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--str", type=str, help="cube string")
parser.add_argument("-m", "--moves", type=str, help="cube scramble")
parser.add_argument("-d", "--display", action="store_true", help="print out solve")
parser.add_argument("-n", "--number", type=int, help="number of solves")
parser.add_argument("-c", "--camera", action="store_true", help="solve from camera")
args = parser.parse_args()

max_move = 23
num_of_shuffles = 100
num_of_solves = 1
one_solve = False
if args.number != None:
    num_of_solves = args.number

time_list = []
move_list1 = [] # global move list
move_list2 = []
pool = multiprocessing.Pool(8)
solution_found = False
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
        # TODO we are assuming the cube is not solved
        pool = multiprocessing.Pool(8)
        move_list1 = []
        move_space = list(MS)
        random.shuffle(move_space)
        for move in move_space:
            params = []
            state = deepcopy(init_state)
            move_coord.stage1_move(state, move)
            state[3] = move
            params.append(state)
            params.append(stage1_min-1)
            params.append(last_move_lists)
            pool.apply_async(search.first_stage_search, params, callback=stage1_result)
        pool.close()
        pool.join()
        
        last_move_lists.append(move_list1) # don't repeat that
        #print(last_move_lists)
        stage1_min = len(move_list1) # set min depth

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
        init_state2.append(move_list1[len(move_list1)-1]) # last move
        init_state2.append(0) # takes 0 moves 

        stage2_max = max_move-len(move_list1)

        move_list2 = []
        pool = multiprocessing.Pool(8)
        last_face = init_state[3]//3
        for move in G1Space:
            cur_face = move//3
            if cur_face == last_face: continue
            elif cur_face == 3 and last_face == 1: continue
            elif cur_face == 4 and last_face == 2: continue
            elif cur_face == 5 and last_face == 0: continue

            params = []
            state = deepcopy(init_state2)
            move_coord.stage2_move(state, move)
            state[3] = move
            params.append(state)
            params.append(stage2_max-1)
            pool.apply_async(search.second_stage_search, params, callback=stage2_result)
        pool.close()
        pool.join()

        #solution_found, move_list2 = search.second_stage_search(init_state2, stage2_max)

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
pool.terminate()