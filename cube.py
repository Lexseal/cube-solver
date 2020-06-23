import numpy as np
import os.path
import random
from time import time
from cube_model import MoveSpace as MS
from cube_model import G1Space
from calc_move_table import MoveTable

class Cube:
    def __init__(self, corners = bytearray(range(8)), edges = bytearray(range(12))):
        ''' Default position is solved, but can be changed to anything. '''
        self.corners = corners

        # split edges into two sets
        self.edges1 = edges[:6]
        self.edges2 = edges[6:]

        # make a move table if it doesn't exist
        if not os.path.exists("move_table_corner.npy") or not os.path.exists("move_table_edge.npy"):
            move_table = MoveTable()
            move_table.make_table()

        # load move_table
        self.corner_table = np.load("move_table_corner.npy").tolist()
        self.edge_table = np.load("move_table_edge.npy").tolist()

    def move_corners(self, corners, move):
        ct = self.corner_table[move]
        corners[0] = ct[corners[0]]
        corners[1] = ct[corners[1]]
        corners[2] = ct[corners[2]]
        corners[3] = ct[corners[3]]
        corners[4] = ct[corners[4]]
        corners[5] = ct[corners[5]]
        corners[6] = ct[corners[6]]
        corners[7] = ct[corners[7]]

    def move_edges1(self, edges1, move):
        et = self.edge_table[move]
        edges1[0] = et[edges1[0]]
        edges1[1] = et[edges1[1]]
        edges1[2] = et[edges1[2]]
        edges1[3] = et[edges1[3]]
        edges1[4] = et[edges1[4]]
        edges1[5] = et[edges1[5]]

    def move_edges2(self, edges2, move):
        et = self.edge_table[move]
        edges2[0] = et[edges2[0]]
        edges2[1] = et[edges2[1]]
        edges2[2] = et[edges2[2]]
        edges2[3] = et[edges2[3]]
        edges2[4] = et[edges2[4]]
        edges2[5] = et[edges2[5]]

    def move(self, move):
        ct = self.corner_table[move]
        self.corners[0] = ct[self.corners[0]]
        self.corners[1] = ct[self.corners[1]]
        self.corners[2] = ct[self.corners[2]]
        self.corners[3] = ct[self.corners[3]]
        self.corners[4] = ct[self.corners[4]]
        self.corners[5] = ct[self.corners[5]]
        self.corners[6] = ct[self.corners[6]]
        self.corners[7] = ct[self.corners[7]]

        et = self.edge_table[move]
        self.edges1[0] = et[self.edges1[0]]
        self.edges1[1] = et[self.edges1[1]]
        self.edges1[2] = et[self.edges1[2]]
        self.edges1[3] = et[self.edges1[3]]
        self.edges1[4] = et[self.edges1[4]]
        self.edges1[5] = et[self.edges1[5]]

        self.edges2[0] = et[self.edges2[0]]
        self.edges2[1] = et[self.edges2[1]]
        self.edges2[2] = et[self.edges2[2]]
        self.edges2[3] = et[self.edges2[3]]
        self.edges2[4] = et[self.edges2[4]]
        self.edges2[5] = et[self.edges2[5]]

    def shuffle(self, N):
        move_list = []
        for _ in range(N):
            rand_move = random.sample(list(MS), 1)[0]
            self.move(rand_move)
            move_list.append(rand_move)
        return move_list


def random_client(N):
    cube = Cube()
    moves = []
    start_time = time()
    for _ in range(N):
        new_move = random.randrange(0, 18)
        #new_move = random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 17], 1)[0]
        cube.move(new_move)
        moves.append(new_move)
    print(list(cube.corners), list(cube.edges1), list(cube.edges2))
    print(N, "random moves took", round(time()-start_time, 2), "seconds")

    for move in reversed(moves):
        if move in [0, 3, 6, 9, 12, 15]:
            move += 2
        elif move in [2, 5, 8, 11, 14, 17]:
            move -= 2
        cube.move(move)
    print(list(cube.corners), list(cube.edges1), list(cube.edges2))
    print("After reversing, the entire operation took", round(time()-start_time, 2), "seconds")

if __name__ == "__main__":
    #random_client(1000)
    pass