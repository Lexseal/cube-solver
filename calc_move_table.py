import numpy as np
import random
import time
from cube_model import MoveSpace as MS

class MoveTable:
    def __init__(self, corners = list(range(8)), edges = list(range(12))):
        ''' Default position is solved, but can be changed to anything. '''
        self.corners = corners
        self.edges = edges
        self.make_table()

    def swap(self, arr, idx1, idx2):
        tmp = arr[idx1]
        arr[idx1] = arr[idx2]
        arr[idx2] = tmp

    def permute(self, arr, idx1, idx2, idx3, idx4):
        tmp = arr[idx4]
        arr[idx4] = arr[idx3]
        arr[idx3] = arr[idx2]
        arr[idx2] = arr[idx1]
        arr[idx1] = tmp

    def rotateCorner(self, idx, stops):
        self.corners[idx] = (self.corners[idx]+stops*8)%24

    def flipEdge(self, idx):
        self.edges[idx] = (self.edges[idx]+12)%24

    def u1(self):
        '''
        0 1 2 3 corner
        0 1 2 3 edge
        '''
        self.permute(self.corners, 0, 1, 2 ,3)
        self.permute(self.edges, 0, 1, 2, 3)

    def u2(self):
        self.swap(self.corners, 0, 2)
        self.swap(self.corners, 1, 3)
        self.swap(self.edges, 0, 2)
        self.swap(self.edges, 1, 3)

    def u3(self):
        self.permute(self.corners, 3, 2, 1, 0)
        self.permute(self.edges, 3, 2, 1, 0)

    def d1(self):
        '''
        4 5 6 7
        8 9 10 11
        '''
        self.permute(self.corners, 4, 5, 6, 7)
        self.permute(self.edges, 8, 9, 10, 11)

    def d2(self):
        self.swap(self.corners, 4, 6)
        self.swap(self.corners, 5, 7)
        self.swap(self.edges, 8, 10)
        self.swap(self.edges, 9, 11)

    def d3(self):
        self.permute(self.corners, 7, 6, 5, 4)
        self.permute(self.edges, 11, 10, 9, 8)

    def l1(self):
        '''
        0 3 4 7 corner
        3 7 11 4 edge
        '''
        self.permute(self.corners, 0, 3, 4, 7)
        self.permute(self.edges, 3, 7, 11, 4)
        self.rotateCorner(0, 1)
        self.rotateCorner(3, 2)
        self.rotateCorner(4, 1)
        self.rotateCorner(7, 2)
        self.flipEdge(3)
        self.flipEdge(7)
        self.flipEdge(11)
        self.flipEdge(4)

    def l2(self):
        self.swap(self.corners, 0, 4)
        self.swap(self.corners, 3, 7)
        self.swap(self.edges, 3, 11)
        self.swap(self.edges, 7, 4)

    def l3(self):
        self.permute(self.corners, 7, 4, 3, 0)
        self.permute(self.edges, 4, 11, 7, 3)
        self.rotateCorner(0, 1)
        self.rotateCorner(3, 2)
        self.rotateCorner(4, 1)
        self.rotateCorner(7, 2)
        self.flipEdge(3)
        self.flipEdge(7)
        self.flipEdge(11)
        self.flipEdge(4)

    def r1(self):
        '''
        1 6 5 2 corner
        1 5 9 6 edge
        '''
        self.permute(self.corners, 1, 6, 5, 2)
        self.permute(self.edges, 1, 5, 9, 6)
        self.rotateCorner(1, 2)
        self.rotateCorner(6, 1)
        self.rotateCorner(5, 2)
        self.rotateCorner(2, 1)
        self.flipEdge(1)
        self.flipEdge(5)
        self.flipEdge(9)
        self.flipEdge(6)

    def r2(self):
        self.swap(self.corners, 1, 5)
        self.swap(self.corners, 6, 2)
        self.swap(self.edges, 1, 9)
        self.swap(self.edges, 5, 6)

    def r3(self):
        self.permute(self.corners, 2, 5, 6, 1)
        self.permute(self.edges, 6, 9, 5, 1)
        self.rotateCorner(1, 2)
        self.rotateCorner(6, 1)
        self.rotateCorner(5, 2)
        self.rotateCorner(2, 1)
        self.flipEdge(1)
        self.flipEdge(5)
        self.flipEdge(9)
        self.flipEdge(6)

    def f1(self):
        '''
        2 5 4 3
        2 6 8 7
        '''
        self.permute(self.corners, 2, 5, 4, 3)
        self.permute(self.edges, 2, 6, 8, 7)
        self.rotateCorner(2, 2)
        self.rotateCorner(5, 1)
        self.rotateCorner(4, 2)
        self.rotateCorner(3, 1)
        self.flipEdge(2)
        self.flipEdge(6)
        self.flipEdge(8)
        self.flipEdge(7)

    def f2(self):
        self.swap(self.corners, 2, 4)
        self.swap(self.corners, 5, 3)
        self.swap(self.edges, 2, 8)
        self.swap(self.edges, 6, 7)

    def f3(self):
        self.permute(self.corners, 3, 4, 5, 2)
        self.permute(self.edges, 7, 8, 6, 2)
        self.rotateCorner(2, 2)
        self.rotateCorner(5, 1)
        self.rotateCorner(4, 2)
        self.rotateCorner(3, 1)
        self.flipEdge(2)
        self.flipEdge(6)
        self.flipEdge(8)
        self.flipEdge(7)

    def b1(self):
        '''
        0 7 6 1
        0 4 10 5
        '''
        self.permute(self.corners, 0, 7, 6, 1)
        self.permute(self.edges, 0, 4, 10, 5)
        self.rotateCorner(0, 1)
        self.rotateCorner(7, 2)
        self.rotateCorner(6, 1)
        self.rotateCorner(1, 2)
        self.flipEdge(0)
        self.flipEdge(4)
        self.flipEdge(10)
        self.flipEdge(5)

    def b2(self):
        self.swap(self.corners, 0, 6)
        self.swap(self.corners, 7, 1)
        self.swap(self.edges, 0, 10)
        self.swap(self.edges, 4, 5)

    def b3(self):
        self.permute(self.corners, 1, 6, 7, 0)
        self.permute(self.edges, 5, 10, 4, 0)
        self.rotateCorner(0, 1)
        self.rotateCorner(7, 2)
        self.rotateCorner(6, 1)
        self.rotateCorner(1, 2)
        self.flipEdge(0)
        self.flipEdge(4)
        self.flipEdge(10)
        self.flipEdge(5)

    def move(self, command):
        if command == MS.U1:
            self.u1()
        elif command == MS.U2:
            self.u2()
        elif command == MS.U3:
            self.u3()
        elif command == MS.L1:
            self.l1()
        elif command == MS.L2:
            self.l2()
        elif command == MS.L3:
            self.l3()
        elif command == MS.F1:
            self.f1()
        elif command == MS.F2:
            self.f2()
        elif command == MS.F3:
            self.f3()
        elif command == MS.R1:
            self.r1()
        elif command == MS.R2:
            self.r2()
        elif command == MS.R3:
            self.r3()
        elif command == MS.B1:
            self.b1()
        elif command == MS.B2:
            self.b2()
        elif command == MS.B3:
            self.b3()
        elif command == MS.D1:
            self.d1()
        elif command == MS.D2:
            self.d2()
        elif command == MS.D3:
            self.d3()

    def find_corner(self, cr):
        cr %= 8
        for i, corner in enumerate(self.corners):
            if corner%8 == cr: return i, corner
    
    def find_edge(self, eg):
        eg %= 12
        for i, edge in enumerate(self.edges):
            if edge%12 == eg: return i, edge

    def make_table(self):
        corner_table = np.full((18, 24), -1, dtype=np.int8)
        edge_table = np.full((18, 24), -1, dtype=np.int8)

        # initial position
        self.corners = list(range(8))
        self.edges = list(range(12))
        corner_entries = 0
        edge_entries = 0
        while (corner_entries != 432 or edge_entries != 432):
            rand_move = random.randrange(0, 18)
            old_corners = self.corners.copy()
            old_edges = self.edges.copy()
            self.move(rand_move)
            move_corner_table = corner_table[rand_move]
            move_edge_table = edge_table[rand_move]

            for old_pos, old_corner in enumerate(old_corners):
                new_pos, new_corner = self.find_corner(old_corner)
                old_ori = old_corner//8
                new_ori = new_corner//8
                old_pos += 8*old_ori
                new_pos += 8*new_ori
                if move_corner_table[old_pos] == -1:
                    corner_entries += 1
                    move_corner_table[old_pos] = new_pos

            for old_pos, old_edge in enumerate(old_edges):
                new_pos, new_edge = self.find_edge(old_edge)
                old_ori = old_edge//12
                new_ori = new_edge//12
                old_pos += 12*old_ori
                new_pos += 12*new_ori
                if move_edge_table[old_pos] == -1:
                    edge_entries += 1
                    move_edge_table[old_pos] = new_pos

        # save
        #print(corner_table, edge_table)
        np.save("move_table_corner", corner_table)
        np.save("move_table_edge", edge_table)


def random_client(N):
    cube = MoveTable()
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