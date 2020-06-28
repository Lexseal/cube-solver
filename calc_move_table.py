import numpy as np
import random
import time
from cube_model import MoveSpace as MS
import rank

class MoveTable:
    def __init__(self, corners = bytearray(range(8)), edges = bytearray(range(12))):
        ''' Default position is solved, but can be changed to anything. '''
        self.corners = corners
        self.edges = edges
        #self.co_ori_table()
        #self.eg_ori_table()
        #self.ud_edges_table()

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

    def get_co_ori(self):
        co_ori = [0]*8
        for i, co in enumerate(self.corners):
            co_ori[i] = co//8
        return co_ori

    def set_co_ori(self, co_ori):
        for i, co in enumerate(self.corners):
            self.corners[i] = co%8+co_ori[i]*8

    def co_ori_table(self):
        co_ori_table = []
        for i in range(2187):
            cur_co_ori = rank.co_ori_inv(i)
            state_table = []
            for move in MS:
                self.set_co_ori(cur_co_ori)
                self.move(move)
                state_table.append(rank.co_ori(self.get_co_ori()))
            co_ori_table.append(state_table)
        np.save("table/co_ori_table", np.array(co_ori_table, dtype=np.int8))

    def get_eg_ori(self):
        eg_ori = [0]*12
        for i, co in enumerate(self.edges):
            eg_ori[i] = co//12
        return eg_ori

    def set_eg_ori(self, eg_ori):
        for i, co in enumerate(self.edges):
            self.edges[i] = co%12+eg_ori[i]*12

    def eg_ori_table(self):
        eg_ori_table = []
        for i in range(2048):
            cur_eg_ori = rank.eg_ori_inv(i)
            state_table = []
            for move in MS:
                self.set_eg_ori(cur_eg_ori)
                self.move(move)
                state_table.append(rank.eg_ori(self.get_eg_ori()))
            eg_ori_table.append(state_table)
        np.save("table/eg_ori_table", np.array(eg_ori_table, dtype=np.int8))

    def get_ud_edges(self):
        ud_edges = [0]*12
        for i, eg in enumerate(self.edges):
            if eg%12 >= 4 and eg%12 <= 7:
                ud_edges[i] = eg%12
        return ud_edges

    def set_ud_egdes(self, ud_edges):
        self.edges = ud_edges.copy()

    def ud_edges_table(self):
        ud_edges_table = []
        for i in range(495):
            cur_ud_edges = rank.ud_edges_inv(i)
            state_table = []
            for move in MS:
                self.set_ud_egdes(cur_ud_edges)
                self.move(move)
                state_table.append(rank.ud_edges(self.get_ud_edges()))
            ud_edges_table.append(state_table)
        np.save("table/ud_edges_table", np.array(ud_edges_table, dtype=np.int8))

    def shuffle(self, N):
        for _ in range(N):
            rand_move = random.randrange(len(MS))
            self.move(rand_move)

def random_client(N):
    cube = MoveTable()
    moves = []
    #ud_edge_table = cube.ud_edges()
    start_time = time.time()
    #small = 10000000
    #big = -1
    print(list(cube.corners), list(cube.edges))
    for _ in range(N):
        new_move = random.randrange(0, 18)
        #expected = ud_edge_table[rank.ud_edges(cube.get_ud_edges())][new_move]
        cube.move(new_move)
        #actual = rank.ud_edges(cube.get_ud_edges())
        #if actual < small:
        #    small = actual
        #if actual > big:
        #    big = actual
        #print(expected, actual)
        moves.append(new_move)
    #print(small, big)
    print(list(cube.corners), list(cube.edges))
    
    print(N, "random moves took", round(time.time()-start_time, 2), "seconds")

    for move in reversed(moves):
        if move in [0, 3, 6, 9, 12, 15]:
            move += 2
        elif move in [2, 5, 8, 11, 14, 17]:
            move -= 2
        cube.move(move)
    print(list(cube.corners), list(cube.edges))
    print("After reversing, the entire operation took", round(time.time()-start_time, 2), "seconds")

if __name__ == "__main__":
    #cube = MoveTable()
    pass