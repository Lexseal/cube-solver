import numpy as np
from collections import deque
from cube import Cube
from rank import rank_corners, rank_edges
from cube_model import MoveSpace as MS
from cube_model import G1Space

# load move_table
move_table_corner = np.load("table/move_table_corner.npy").tolist()
move_table_edge = np.load("table/move_table_edge.npy").tolist()

def move_cube(corners, edges1, edges2, move):
        ct = move_table_corner[move]
        corners[0] = ct[corners[0]]
        corners[1] = ct[corners[1]]
        corners[2] = ct[corners[2]]
        corners[3] = ct[corners[3]]
        corners[4] = ct[corners[4]]
        corners[5] = ct[corners[5]]
        corners[6] = ct[corners[6]]
        corners[7] = ct[corners[7]]

        et = move_table_edge[move]
        edges1[0] = et[edges1[0]]
        edges1[1] = et[edges1[1]]
        edges1[2] = et[edges1[2]]
        edges1[3] = et[edges1[3]]
        edges1[4] = et[edges1[4]]
        edges1[5] = et[edges1[5]]

        edges2[0] = et[edges2[0]]
        edges2[1] = et[edges2[1]]
        edges2[2] = et[edges2[2]]
        edges2[3] = et[edges2[3]]
        edges2[4] = et[edges2[4]]
        edges2[5] = et[edges2[5]]

def min_move(corners, edges1, edges2):
    min_corners = corner_table[rank_corners(corners)]
    min_edges1 = edge_table1[rank_edges(edges1)]
    min_edges2 = edge_table2[rank_edges(edges2)]
    return max(min_corners, min_edges1, min_edges2)

def print_move(move):
    for labeled_move in MS:
        if move == labeled_move:
            print(labeled_move)
            return

# load tables
corner_table = bytearray(np.load("table/corner_table.npy"))
edge_table1 = bytearray(np.load("table/edge_table1.npy"))
edge_table2 = bytearray(np.load("table/edge_table2.npy"))

# make a new solved cube
cube = Cube()

# apply some random moves
for move in cube.shuffle(12):
    print_move(move)

solved_corners = bytearray(range(8))
solved_edges = bytearray(range(12))
solved_edges1 = solved_edges[:6]
solved_edges2 = solved_edges[6:]

def ori_solved(corners, edges1, edges2):
    return corners[0] < 8 and \
        corners[1] < 8 and \
        corners[2] < 8 and \
        corners[3] < 8 and \
        corners[4] < 8 and \
        corners[5] < 8 and \
        corners[6] < 8 and \
        corners[7] < 8 and \
        edges1[0] < 12 and \
        edges1[1] < 12 and \
        edges1[2] < 12 and \
        edges1[3] < 12 and \
        edges1[4] <= 7 and edges1[4] >= 4 and \
        edges1[5] <= 7 and edges1[5] >= 4 and \
        edges2[0] <= 7 and edges2[0] >= 4 and \
        edges2[1] <= 7 and edges2[1] >= 4 and \
        edges2[2] < 12 and \
        edges2[3] < 12 and \
        edges2[4] < 12 and \
        edges2[5] < 12

# iterative deepening depth-first search
cube.corners.append(255) # use 255 to denote the -1st move
cube.corners.append(0) # takes 0 moves to get there
first_phase_complete = False
for max_depth in range(0, 12):
    corner_stack = deque()
    edge1_stack = deque()
    edge2_stack = deque()
    move_stack = deque()

    corner_stack.append(cube.corners)
    edge1_stack.append(cube.edges1)
    edge2_stack.append(cube.edges2)
    while len(corner_stack) > 0:
        cur_corners = corner_stack.pop()
        cur_edge1 = edge1_stack.pop()
        cur_edge2 = edge2_stack.pop()
        depth = cur_corners[9] # get the depth of the state
        while (len(move_stack) > depth):
            move_stack.pop()

        last_move = cur_corners[8]
        move_stack.append(last_move)

        if depth == max_depth:
            if ori_solved(cur_corners, cur_edge1, cur_edge2):
                    print("victory", depth)
                    cube.corners = cur_corners
                    cube.edges1 = cur_edge1
                    cube.edges2 = cur_edge2
                    move_list = []
                    for _ in range(depth):
                        move_list.insert(0, move_stack.pop())
                    for move in move_list:
                        print_move(move)
                    first_phase_complete = True
                    break
        else:
            for move in MS:
                if move == last_move or \
                    move//3 == last_move//3 and \
                        abs(move-last_move) == 2:
                    continue

                new_corners = cur_corners.copy()
                new_corners[8] = move
                new_corners[9] = depth+1

                new_edges1 = cur_edge1.copy()
                new_edges2 = cur_edge2.copy()
                move_cube(new_corners, new_edges1, new_edges2, move)

                # add if within the search range
                if min_move(new_corners, new_edges1, new_edges2) <= max_depth:
                    corner_stack.append(new_corners)
                    edge1_stack.append(new_edges1)
                    edge2_stack.append(new_edges2)
    if first_phase_complete: break
    print("level", max_depth, "done")

print("second phased started")
cube.corners[9] = 0 # takes 0 moves to get there
for max_depth in range(0, 18):
    corner_stack = deque()
    edge1_stack = deque()
    edge2_stack = deque()
    move_stack = deque()

    corner_stack.append(cube.corners)
    edge1_stack.append(cube.edges1)
    edge2_stack.append(cube.edges2)
    while len(corner_stack) > 0:
        cur_corners = corner_stack.pop()
        cur_edge1 = edge1_stack.pop()
        cur_edge2 = edge2_stack.pop()
        depth = cur_corners[9] # get the depth of the state
        while (len(move_stack) > depth):
            move_stack.pop()

        last_move = cur_corners[8]
        move_stack.append(last_move)

        if depth == max_depth:
            #print(len(move_stack))
            if cur_corners[:8] == solved_corners and \
                cur_edge1 == solved_edges1 and \
                    cur_edge2 == solved_edges2:
                    print("victory", depth)
                    move_list = []
                    for _ in range(depth):
                        move_list.insert(0, move_stack.pop())
                    for move in move_list:
                        print_move(move)
                    exit(0)
        else:
            for move in G1Space:
                cur_face = move//3
                last_face = last_move//3
                if cur_face == last_face: continue
                elif cur_face == 3 and last_face == 1: continue
                elif cur_face == 4 and last_face == 2: continue
                elif cur_face == 5 and last_face == 0: continue

                new_corners = cur_corners.copy()
                new_corners[8] = move
                new_corners[9] = depth+1

                new_edges1 = cur_edge1.copy()
                new_edges2 = cur_edge2.copy()
                move_cube(new_corners, new_edges1, new_edges2, move)

                # add if within the search range
                if depth + min_move(new_corners, new_edges1, new_edges2) <= max_depth:
                    corner_stack.append(new_corners)
                    edge1_stack.append(new_edges1)
                    edge2_stack.append(new_edges2)

    print("level", max_depth, "done")