import numpy as np
import random
from time import time
import argparse
import cube_model
from cube_model import Facelets
from cube_model import corner_to_char, edge_to_char
from cube_model import str_to_cor, str_to_eg
import rank

"""
This file models how a cube should rotate move
and how to construct a cube either from a sequence of moves
or from a string of colors
"""

class Cube:
    def __init__(self, cube_str = None, cube_scramble = None):
        ''' Default position is solved, but can be changed to anything. '''
        self.corners = bytearray(range(8))
        self.edges = bytearray(range(12))
        if cube_str != None:
            self.read_str(cube_str)
        elif cube_scramble != None:
            self.read_scramble(cube_scramble)

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
        4 5 6 7
        '''
        self.permute(self.corners, 4, 5, 6, 7)
        self.permute(self.edges, 4, 5, 6, 7)

    def d2(self):
        self.swap(self.corners, 4, 6)
        self.swap(self.corners, 5, 7)
        self.swap(self.edges, 4, 6)
        self.swap(self.edges, 5, 7)

    def d3(self):
        self.permute(self.corners, 7, 6, 5, 4)
        self.permute(self.edges, 7, 6, 5, 4)

    def l1(self):
        '''
        0 3 4 7 corner
        3 10 5 11 edge
        '''
        self.permute(self.corners, 0, 3, 4, 7)
        self.permute(self.edges, 3, 10, 5, 11)
        self.rotateCorner(0, 2)
        self.rotateCorner(3, 1)
        self.rotateCorner(4, 2)
        self.rotateCorner(7, 1)
        self.flipEdge(3)
        self.flipEdge(10)
        self.flipEdge(5)
        self.flipEdge(11)

    def l2(self):
        self.swap(self.corners, 0, 4)
        self.swap(self.corners, 3, 7)
        self.swap(self.edges, 3, 5)
        self.swap(self.edges, 10, 11)

    def l3(self):
        self.permute(self.corners, 7, 4, 3, 0)
        self.permute(self.edges, 11, 5, 10, 3)
        self.rotateCorner(0, 2)
        self.rotateCorner(3, 1)
        self.rotateCorner(4, 2)
        self.rotateCorner(7, 1)
        self.flipEdge(3)
        self.flipEdge(10)
        self.flipEdge(5)
        self.flipEdge(11)

    def r1(self):
        '''
        1 6 5 2 corner
        1 8 7 9 edge
        '''
        self.permute(self.corners, 1, 6, 5, 2)
        self.permute(self.edges, 1, 8, 7, 9)
        self.rotateCorner(1, 1)
        self.rotateCorner(6, 2)
        self.rotateCorner(5, 1)
        self.rotateCorner(2, 2)
        self.flipEdge(1)
        self.flipEdge(8)
        self.flipEdge(7)
        self.flipEdge(9)

    def r2(self):
        self.swap(self.corners, 1, 5)
        self.swap(self.corners, 6, 2)
        self.swap(self.edges, 1, 7)
        self.swap(self.edges, 8, 9)

    def r3(self):
        self.permute(self.corners, 2, 5, 6, 1)
        self.permute(self.edges, 9, 7, 8, 1)
        self.rotateCorner(1, 1)
        self.rotateCorner(6, 2)
        self.rotateCorner(5, 1)
        self.rotateCorner(2, 2)
        self.flipEdge(1)
        self.flipEdge(8)
        self.flipEdge(7)
        self.flipEdge(9)

    def f1(self):
        '''
        2 5 4 3
        2 9 6 10
        '''
        self.permute(self.corners, 2, 5, 4, 3)
        self.permute(self.edges, 2, 9, 6, 10)
        self.rotateCorner(2, 1)
        self.rotateCorner(5, 2)
        self.rotateCorner(4, 1)
        self.rotateCorner(3, 2)

    def f2(self):
        self.swap(self.corners, 2, 4)
        self.swap(self.corners, 5, 3)
        self.swap(self.edges, 2, 6)
        self.swap(self.edges, 9, 10)

    def f3(self):
        self.permute(self.corners, 3, 4, 5, 2)
        self.permute(self.edges, 10, 6, 9, 2)
        self.rotateCorner(2, 1)
        self.rotateCorner(5, 2)
        self.rotateCorner(4, 1)
        self.rotateCorner(3, 2)

    def b1(self):
        '''
        0 7 6 1
        0 11 4 8
        '''
        self.permute(self.corners, 0, 7, 6, 1)
        self.permute(self.edges, 0, 11, 4, 8)
        self.rotateCorner(0, 1)
        self.rotateCorner(7, 2)
        self.rotateCorner(6, 1)
        self.rotateCorner(1, 2)

    def b2(self):
        self.swap(self.corners, 0, 6)
        self.swap(self.corners, 7, 1)
        self.swap(self.edges, 0, 4)
        self.swap(self.edges, 11, 8)

    def b3(self):
        self.permute(self.corners, 1, 6, 7, 0)
        self.permute(self.edges, 8, 4, 11, 0)
        self.rotateCorner(0, 1)
        self.rotateCorner(7, 2)
        self.rotateCorner(6, 1)
        self.rotateCorner(1, 2)

    def move(self, command):
        if command == cube_model.MoveSpace.U1:
            self.u1()
        elif command == cube_model.MoveSpace.U2:
            self.u2()
        elif command == cube_model.MoveSpace.U3:
            self.u3()
        elif command == cube_model.MoveSpace.L1:
            self.l1()
        elif command == cube_model.MoveSpace.L2:
            self.l2()
        elif command == cube_model.MoveSpace.L3:
            self.l3()
        elif command == cube_model.MoveSpace.F1:
            self.f1()
        elif command == cube_model.MoveSpace.F2:
            self.f2()
        elif command == cube_model.MoveSpace.F3:
            self.f3()
        elif command == cube_model.MoveSpace.R1:
            self.r1()
        elif command == cube_model.MoveSpace.R2:
            self.r2()
        elif command == cube_model.MoveSpace.R3:
            self.r3()
        elif command == cube_model.MoveSpace.B1:
            self.b1()
        elif command == cube_model.MoveSpace.B2:
            self.b2()
        elif command == cube_model.MoveSpace.B3:
            self.b3()
        elif command == cube_model.MoveSpace.D1:
            self.d1()
        elif command == cube_model.MoveSpace.D2:
            self.d2()
        elif command == cube_model.MoveSpace.D3:
            self.d3()

    @staticmethod
    def rotate_color(str):
        return str[2]+str[5]+str[8]+str[1]+str[4]+str[7]+str[0]+str[3]+str[6]

    @staticmethod
    def rotate_color_rev(str):
        return str[6]+str[3]+str[0]+str[7]+str[4]+str[1]+str[8]+str[5]+str[2]

    def rotate_z(self):
        cube_str = self.__str__()
        cube_str = cube_str.replace("F", "r")
        cube_str = cube_str.replace("R", "b")
        cube_str = cube_str.replace("B", "l")
        cube_str = cube_str.replace("L", "f")
        cube_str = cube_str.replace("f", "F")
        cube_str = cube_str.replace("l", "L")
        cube_str = cube_str.replace("b", "B")
        cube_str = cube_str.replace("r", "R")
        up_face = self.rotate_color(cube_str[0:9])
        left_face = cube_str[9:18]
        front_face = cube_str[18:27]
        right_face = cube_str[27:36]
        back_face = cube_str[36:45]
        down_face = self.rotate_color_rev(cube_str[45:54])
        cube_str = up_face+back_face+left_face+front_face+right_face+down_face
        self.read_str(cube_str)

    def rotate_x_rev(self):
        cube_str = self.__str__()
        cube_str = cube_str.replace("U", "r")
        cube_str = cube_str.replace("R", "d")
        cube_str = cube_str.replace("D", "l")
        cube_str = cube_str.replace("L", "u")
        cube_str = cube_str.replace("r", "R")
        cube_str = cube_str.replace("d", "D")
        cube_str = cube_str.replace("l", "L")
        cube_str = cube_str.replace("u", "U")
        up_face = self.rotate_color_rev(cube_str[0:9])
        left_face = self.rotate_color_rev(cube_str[9:18])
        front_face = self.rotate_color_rev(cube_str[18:27])
        right_face = self.rotate_color_rev(cube_str[27:36])
        back_face = self.rotate_color(cube_str[36:45])
        down_face = self.rotate_color_rev(cube_str[45:54])
        cube_str = left_face+down_face+front_face+up_face+back_face+right_face
        self.read_str(cube_str)

    @staticmethod
    def flip_face(face):
        return face[2]+face[1]+face[0]+face[5]+face[4]+face[3]+face[8]+face[7]+face[6]

    def flip_cube(self):
        cube_str = self.__str__()
        cube_str = cube_str.replace("L", "r")
        cube_str = cube_str.replace("R", "L")
        cube_str = cube_str.replace("r", "R") # replace left with right
        up_face = self.flip_face(cube_str[0:9])
        left_face = self.flip_face(cube_str[27:36]) # gets the right face
        front_face = self.flip_face(cube_str[18:27])
        right_face = self.flip_face(cube_str[9:18]) # gets the left face
        back_face = self.flip_face(cube_str[36:45])
        down_face = self.flip_face(cube_str[45:54]) # get faces
        cube_str = up_face+left_face+front_face+right_face+back_face+down_face
        self.read_str(cube_str)

    def get_co_ori(self):
        co_ori = [0]*8
        for i, co in enumerate(self.corners):
            co_ori[i] = co//8
        return co_ori

    def set_co_ori(self, co_ori):
        for i, co in enumerate(self.corners):
            self.corners[i] = co%8+co_ori[i]*8

    def get_eg_ori(self):
        eg_ori = [0]*12
        for i, co in enumerate(self.edges):
            eg_ori[i] = co//12
        return eg_ori

    def set_eg_ori(self, eg_ori):
        for i, co in enumerate(self.edges):
            self.edges[i] = co%12+eg_ori[i]*12

    def get_ud_edges(self):
        ud_edges = [0]*12
        for i, eg in enumerate(self.edges):
            if eg%12 >= 8:
                ud_edges[i] = eg%12
        return ud_edges

    def set_ud_egdes(self, ud_edges):
        self.edges = ud_edges.copy()

    def get_co_perm(self):
        return [co%8 for co in self.corners]

    def set_co_perm(self, co_perm):
        self.corners = co_perm.copy()

    def get_eg_perm(self):
        return [eg%12 for eg in self.edges[:8]] 

    def set_eg_perm(self, eg_perm):
        self.edges[:8] = eg_perm.copy()

    def get_ud_perm(self):
        return [eg%12 for eg in self.edges[8:]]

    def set_ud_perm(self, ud_perm):
        self.edges[8:] = ud_perm.copy()

    def shuffle(self, N):
        move_list = []
        for _ in range(N):
            rand_move = random.randrange(18)
            self.move(rand_move)
            move_list.append(rand_move)
        return move_list

    def shuffle_G1(self, N):
        move_list = []
        for _ in range(N):
            rand_move = random.sample(list(cube_model.G1Space), 1)[0]
            self.move(rand_move)
            move_list.append(rand_move)
        return move_list

    def __str__(self):
        cube_str = ['']*54
        cube_str[Facelets.U5] = 'U'
        cube_str[Facelets.L5] = 'L'
        cube_str[Facelets.F5] = 'F'
        cube_str[Facelets.R5] = 'R'
        cube_str[Facelets.B5] = 'B'
        cube_str[Facelets.D5] = 'D'
        cube_str[Facelets.U1], cube_str[Facelets.B3], cube_str[Facelets.L1] = corner_to_char(self.corners[0])
        cube_str[Facelets.U3], cube_str[Facelets.R3], cube_str[Facelets.B1] = corner_to_char(self.corners[1])
        cube_str[Facelets.U9], cube_str[Facelets.F3], cube_str[Facelets.R1] = corner_to_char(self.corners[2])
        cube_str[Facelets.U7], cube_str[Facelets.L3], cube_str[Facelets.F1] = corner_to_char(self.corners[3])
        cube_str[Facelets.D1], cube_str[Facelets.F7], cube_str[Facelets.L9] = corner_to_char(self.corners[4])
        cube_str[Facelets.D3], cube_str[Facelets.R7], cube_str[Facelets.F9] = corner_to_char(self.corners[5])
        cube_str[Facelets.D9], cube_str[Facelets.B7], cube_str[Facelets.R9] = corner_to_char(self.corners[6])
        cube_str[Facelets.D7], cube_str[Facelets.L7], cube_str[Facelets.B9] = corner_to_char(self.corners[7])
        cube_str[Facelets.U2], cube_str[Facelets.B2] = edge_to_char(self.edges[0])
        cube_str[Facelets.U6], cube_str[Facelets.R2] = edge_to_char(self.edges[1])
        cube_str[Facelets.U8], cube_str[Facelets.F2] = edge_to_char(self.edges[2])
        cube_str[Facelets.U4], cube_str[Facelets.L2] = edge_to_char(self.edges[3])
        cube_str[Facelets.D8], cube_str[Facelets.B8] = edge_to_char(self.edges[4])
        cube_str[Facelets.D4], cube_str[Facelets.L8] = edge_to_char(self.edges[5])
        cube_str[Facelets.D2], cube_str[Facelets.F8] = edge_to_char(self.edges[6])
        cube_str[Facelets.D6], cube_str[Facelets.R8] = edge_to_char(self.edges[7])
        cube_str[Facelets.R6], cube_str[Facelets.B4] = edge_to_char(self.edges[8])
        cube_str[Facelets.R4], cube_str[Facelets.F6] = edge_to_char(self.edges[9])
        cube_str[Facelets.L6], cube_str[Facelets.F4] = edge_to_char(self.edges[10])
        cube_str[Facelets.L4], cube_str[Facelets.B6] = edge_to_char(self.edges[11])
        return "".join(cube_str)

    def read_str(self, cube_str):
        self.corners[0] = str_to_cor(cube_str[Facelets.U1]+cube_str[Facelets.B3]+cube_str[Facelets.L1])
        self.corners[1] = str_to_cor(cube_str[Facelets.U3]+cube_str[Facelets.R3]+cube_str[Facelets.B1])
        self.corners[2] = str_to_cor(cube_str[Facelets.U9]+cube_str[Facelets.F3]+cube_str[Facelets.R1])
        self.corners[3] = str_to_cor(cube_str[Facelets.U7]+cube_str[Facelets.L3]+cube_str[Facelets.F1])
        self.corners[4] = str_to_cor(cube_str[Facelets.D1]+cube_str[Facelets.F7]+cube_str[Facelets.L9])
        self.corners[5] = str_to_cor(cube_str[Facelets.D3]+cube_str[Facelets.R7]+cube_str[Facelets.F9])
        self.corners[6] = str_to_cor(cube_str[Facelets.D9]+cube_str[Facelets.B7]+cube_str[Facelets.R9])
        self.corners[7] = str_to_cor(cube_str[Facelets.D7]+cube_str[Facelets.L7]+cube_str[Facelets.B9])
        self.edges[0] = str_to_eg(cube_str[Facelets.U2]+cube_str[Facelets.B2])
        self.edges[1] = str_to_eg(cube_str[Facelets.U6]+cube_str[Facelets.R2])
        self.edges[2] = str_to_eg(cube_str[Facelets.U8]+cube_str[Facelets.F2])
        self.edges[3] = str_to_eg(cube_str[Facelets.U4]+cube_str[Facelets.L2])
        self.edges[4] = str_to_eg(cube_str[Facelets.D8]+cube_str[Facelets.B8])
        self.edges[5] = str_to_eg(cube_str[Facelets.D4]+cube_str[Facelets.L8])
        self.edges[6] = str_to_eg(cube_str[Facelets.D2]+cube_str[Facelets.F8])
        self.edges[7] = str_to_eg(cube_str[Facelets.D6]+cube_str[Facelets.R8])
        self.edges[8] = str_to_eg(cube_str[Facelets.R6]+cube_str[Facelets.B4])
        self.edges[9] = str_to_eg(cube_str[Facelets.R4]+cube_str[Facelets.F6])
        self.edges[10] = str_to_eg(cube_str[Facelets.L6]+cube_str[Facelets.F4])
        self.edges[11] = str_to_eg(cube_str[Facelets.L4]+cube_str[Facelets.B6])

    def read_scramble(self, cube_scramble):
        scramble_list = cube_scramble.split(" ")
        for move in scramble_list:
            #print(move)
            self.move(cube_model.convert_move(move))
            #print(self)
            #print(list(self.corners), list(self.edges))

def verify(N):
    cube = Cube()
    start_time = time()
    moves = cube.shuffle(N)
    print(list(cube.corners), list(cube.edges))
    print(N, "random moves took", round(time()-start_time, 2), "seconds")

    for move in reversed(moves):
        if move in [0, 3, 6, 9, 12, 15]:
            move += 2
        elif move in [2, 5, 8, 11, 14, 17]:
            move -= 2
        cube.move(move)
    print(list(cube.corners), list(cube.edges))
    print("After reversing, the entire operation took", round(time()-start_time, 2), "seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--str", type=str, help="cube string")
    parser.add_argument("-m", "--moves", type=str, help="cube scramble")
    args = parser.parse_args()
    if args.str != None:
        cube = Cube(cube_str=args.str)
        print(cube)
        print(list(cube.corners), list(cube.edges))
    elif args.moves != None:
        cube = Cube(cube_scramble=args.moves)
        print(cube)
        print(list(cube.corners), list(cube.edges))
    pass
