from queue import SimpleQueue
import numpy as np
from time import time
import sys
from cube_model import MoveSpace as MS
from cube import Cube
from rank import rank_corners

cube = Cube()
queue = SimpleQueue()
corner_table = bytearray([-1]*88179840)

queue.put(cube.corners)
corner_table[0] = 0 # first entry is solved
n = 0
last_print = 0
start_time = time()
while queue.qsize() != 0:
    cur_state = queue.get() # pop
    move_count = corner_table[rank_corners(cur_state)] # get the move count up to this state

    last_move = -999
    for move in MS:
        if move == last_move or \
            move//3 == last_move//3 and \
            abs(move-last_move) == 2:
           continue
        last_move = move

        next_state = cube.move_corners(cur_state, move)
        next_idx = rank_corners(next_state)
        next_count = corner_table[next_idx]
        if next_count == -1 or \
           next_count > move_count+1:
           corner_table[next_idx] = move_count+1
           queue.put(next_state)
           n += 1

    if (n-last_print > 100000):
        last_print = n
        print(n, queue.qsize(), move_count, round(time()-start_time, 2))

np.save("corner_table", np.array(corner_table, dtype=np.int8))
