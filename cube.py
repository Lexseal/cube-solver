import numpy as np
from cube_model import MoveSpace as MS

class Cube:

    def __init__(self, corners = list(range(8)), edges = list(range(12))):
        ''' Default position is solved, but can be changed to anything. '''
        self.corners = corners
        self.edges = edges
        self.corner_table = np.load("move_table_corner.npy").tolist()
        self.edge_table = np.load("move_table_edge.npy").tolist()

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
        self.edges[0] = et[self.edges[0]]
        self.edges[1] = et[self.edges[1]]
        self.edges[2] = et[self.edges[2]]
        self.edges[3] = et[self.edges[3]]
        self.edges[4] = et[self.edges[4]]
        self.edges[5] = et[self.edges[5]]
        self.edges[6] = et[self.edges[6]]
        self.edges[7] = et[self.edges[7]]
        self.edges[8] = et[self.edges[8]]
        self.edges[9] = et[self.edges[9]]
        self.edges[10] = et[self.edges[10]]
        self.edges[11] = et[self.edges[11]]

import random
import time
def random_client(N):
    cube = Cube()
    moves = []
    start_time = time.time()
    for _ in range(N):
        new_move = random.randrange(0, 18)
        #new_move = random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 17], 1)[0]
        cube.move(new_move)
        moves.append(new_move)
    print(cube.corners, cube.edges)
    
    print(N, "random moves took", round(time.time()-start_time, 2), "seconds")

    for move in reversed(moves):
        if move in [0, 3, 6, 9, 12, 15]:
            move += 2
        elif move in [2, 5, 8, 11, 14, 17]:
            move -= 2
        cube.move(move)
    print(cube.corners, cube.edges)
    print("After reversing, the entire operation took", round(time.time()-start_time, 2), "seconds")

if __name__ == "__main__":
    random_client(1000000)
    pass