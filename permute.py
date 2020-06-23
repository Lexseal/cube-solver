from queue import SimpleQueue
import numpy as np
from time import time
from cube_model import MoveSpace as MS
from cube_model import G1Space
from cube import Cube
#from rank import rank_corners, rank_edges
from rank import h2_corners, h2_edges

def calc_corner_table():
    cube = Cube()
    queue = SimpleQueue()

    # works because all corner states can be achieved in 10 moves or fewer
    corner_table = bytearray([10]*40320)

    cube.corners.append(255)
    queue.put(cube.corners)
    corner_table[0] = 0 # first entry is solved
    n = 0
    last_print = 0
    start_time = time()
    while queue.qsize() > 0:
        cur_state = queue.get() # pop
        move_count = corner_table[h2_corners(cur_state)] # get the move count up to this state

        last_move = cur_state[8]
<<<<<<< HEAD
        for move in MS:
            cur_face = move//3
            last_face = last_move//3
            if cur_face == last_face: continue
            elif cur_face == 3 and last_face == 1: continue
            elif cur_face == 4 and last_face == 2: continue
            elif cur_face == 5 and last_face == 0: continue
=======
        for move in G1Space:
            if move == last_move or \
                move//3 == last_move//3 and \
                    abs(move-last_move) == 2:
                continue
>>>>>>> implemented a correct h2 database, but not space efficient

            next_state = cur_state.copy() # get a copy of cur state
            cube.move_corners(next_state, move) # compute next state
            next_idx = h2_corners(next_state) # rank next state
            next_count = corner_table[next_idx] # get moves count
            if next_count > move_count+1:
                corner_table[next_idx] = move_count+1
                next_state[8] = move
                queue.put(next_state)
                n += 1

        if (n-last_print > 100000):
            last_print = n
            print(str(n//1000)+'k', str(queue.qsize()//1000)+'k', move_count, round((time()-start_time)/60, 2))
    print(n)
    np.save("table/corner_table_h2", np.array(corner_table, dtype=np.int8))

def calc_edge_table1():
    cube = Cube()
    queue = SimpleQueue()

    # works because all edge states can be achieved in 10 moves or fewer
    edge_table1 = bytearray([10]*665280)

    cube.edges1.append(255)
    queue.put(cube.edges1)
    edge_table1[0] = 0 # first entry is solved
    n = 0
    last_print = 0
    start_time = time()
    while queue.qsize() > 0:
        cur_state = queue.get() # pop
        move_count = edge_table1[h2_edges(cur_state)] # get the move count up to this state

        last_move = cur_state[6]
<<<<<<< HEAD
        for move in MS:
            cur_face = move//3
            last_face = last_move//3
            if cur_face == last_face: continue
            elif cur_face == 3 and last_face == 1: continue
            elif cur_face == 4 and last_face == 2: continue
            elif cur_face == 5 and last_face == 0: continue
=======
        for move in G1Space:
            if move == last_move or \
                move//3 == last_move//3 and \
                    abs(move-last_move) == 2:
                continue
>>>>>>> implemented a correct h2 database, but not space efficient

            next_state = cur_state.copy() # get a copy of cur state
            cube.move_edges1(next_state, move) # compute next state
            next_idx = h2_edges(next_state) # rank next state
            next_count = edge_table1[next_idx] # get moves count
            if next_count > move_count+1:
                edge_table1[next_idx] = move_count+1
                next_state[6] = move
                queue.put(next_state)
                n += 1

        if (n-last_print > 100000):
            last_print = n
            print(str(n//1000)+'k', str(queue.qsize()//1000)+'k', move_count, round((time()-start_time)/60, 2))
    print(n)
    np.save("table/edge_table1_h2", np.array(edge_table1, dtype=np.int8))

def calc_edge_table2():
    cube = Cube()
    queue = SimpleQueue()

    # works because all edge states can be achieved in 10 moves or fewer
    edge_table2 = bytearray([10]*665280)

    cube.edges2.append(255)
    queue.put(cube.edges2)
    edge_table2[h2_edges(cube.edges2)] = 0 # first entry is solved
    n = 0
    last_print = 0
    start_time = time()
    while queue.qsize() > 0:
        cur_state = queue.get() # pop
        move_count = edge_table2[h2_edges(cur_state)] # get the move count up to this state

        last_move = cur_state[6]
<<<<<<< HEAD
        for move in MS:
            cur_face = move//3
            last_face = last_move//3
            if cur_face == last_face: continue
            elif cur_face == 3 and last_face == 1: continue
            elif cur_face == 4 and last_face == 2: continue
            elif cur_face == 5 and last_face == 0: continue
=======
        for move in G1Space:
            if move == last_move or \
                move//3 == last_move//3 and \
                    abs(move-last_move) == 2:
                continue
>>>>>>> implemented a correct h2 database, but not space efficient

            next_state = cur_state.copy() # get a copy of cur state
            cube.move_edges2(next_state, move) # compute next state
            next_idx = h2_edges(next_state) # rank next state
            next_count = edge_table2[next_idx] # get moves count
            if next_count > move_count+1:
                edge_table2[next_idx] = move_count+1
                next_state[6] = move
                queue.put(next_state)
                n += 1

        if (n-last_print > 100000):
            last_print = n
            print(str(n//1000)+'k', str(queue.qsize()//1000)+'k', move_count, round((time()-start_time)/60, 2))
<<<<<<< HEAD
<<<<<<< HEAD
    print(n)
    np.save("table/edge_table2", np.array(edge_table2, dtype=np.int8))

if __name__ == "__main__":
    #calc_corner_table()
    #calc_edge_table1()
=======

=======
    print(n)
>>>>>>> more efficient pruning in G1 stage
    np.save("table/edge_table2_h2", np.array(edge_table2, dtype=np.int8))

if __name__ == "__main__":
    calc_corner_table()
    calc_edge_table1()
>>>>>>> implemented a correct h2 database, but not space efficient
    calc_edge_table2()
    pass