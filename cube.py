from cube_model import MoveSpace as MS

class Cube:

    corners = list(range(8))
    edges = list(range(12))

    def swap(self, arr, idx1, idx2):
        tmp = arr[idx1]
        arr[idx1] = arr[idx2]
        arr[idx2] = tmp

    def permute(self, arr, idx1, idx2, idx3, idx4):
        list = [idx4, idx3, idx2, idx1]
        lastIdx = list[0]
        tmp = arr[lastIdx]
        for i in list[1:]:
            arr[lastIdx] = arr[i]
            lastIdx = i
        arr[lastIdx] = tmp

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


if __name__ == "__main__":
    cube = Cube()
    print(cube.corners, cube.edges)
    for i in range(6):
        cube.move(MS.R3)
        cube.move(MS.U1)
        cube.move(MS.R1)
        cube.move(MS.U3)
        print(cube.corners, cube.edges)