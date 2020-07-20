import numpy as np
import random
import time
from cube_model import MoveSpace as MS
from cube_model import G1Space
import rank
from cube import Cube

class MoveTable:
    def __init__(self):
        ''' make a cube '''
        self.cube = Cube()

    def co_ori_table(self):
        co_ori_table = []
        for i in range(2187):
            cur_co_ori = rank.co_ori_inv(i)
            state_table = []
            for move in MS:
                self.cube.set_co_ori(cur_co_ori)
                self.cube.move(move)
                state_table.append(rank.co_ori(self.cube.get_co_ori()))
            co_ori_table.append(state_table)
        np.save("table/co_ori_table", np.array(co_ori_table, dtype=np.uint16))

    def eg_ori_table(self):
        eg_ori_table = []
        for i in range(2048):
            cur_eg_ori = rank.eg_ori_inv(i)
            state_table = []
            for move in MS:
                self.cube.set_eg_ori(cur_eg_ori)
                self.cube.move(move)
                state_table.append(rank.eg_ori(self.cube.get_eg_ori()))
            eg_ori_table.append(state_table)
        np.save("table/eg_ori_table", np.array(eg_ori_table, dtype=np.uint16))

    def ud_edges_table(self):
        ud_edges_table = []
        for i in range(495):
            cur_ud_edges = rank.ud_edges_inv(i)
            state_table = []
            for move in MS:
                self.cube.set_ud_egdes(cur_ud_edges)
                self.cube.move(move)
                state_table.append(rank.ud_edges(self.cube.get_ud_edges()))
            ud_edges_table.append(state_table)
        np.save("table/ud_edges_table", np.array(ud_edges_table, dtype=np.uint16))

    def co_perm_table(self):
        co_perm_table = []
        for i in range(40320):
            cur_co_perm = rank.co_perm_inv(i)
            state_table = [-1]*18
            for move in G1Space:
                self.cube.set_co_perm(cur_co_perm)
                self.cube.move(move)
                state_table[move] = rank.co_perm(self.cube.get_co_perm())
            co_perm_table.append(state_table)
        np.save("table/co_perm_table", np.array(co_perm_table, dtype=np.uint16))
        return co_perm_table

    def eg_perm_table(self):
        eg_perm_table = []
        for i in range(40320):
            cur_eg_perm = rank.eg_perm_inv(i)
            state_table = [-1]*18
            for move in G1Space:
                self.cube.set_eg_perm(cur_eg_perm)
                self.cube.move(move)
                state_table[move] = rank.eg_perm(self.cube.get_eg_perm())
            eg_perm_table.append(state_table)
        np.save("table/eg_perm_table", np.array(eg_perm_table, dtype=np.uint16))
    
    def ud_perm_table(self):
        ud_perm_table = []
        for i in range(24):
            cur_ud_perm = rank.ud_perm_inv(i)
            state_table = [-1]*18
            for move in G1Space:
                self.cube.set_ud_perm(cur_ud_perm)
                self.cube.move(move)
                state_table[move] = rank.ud_perm(self.cube.get_ud_perm())
            ud_perm_table.append(state_table)
        np.save("table/ud_perm_table", np.array(ud_perm_table, dtype=np.uint8))

    def make_tables(self):
        self.co_ori_table()
        self.eg_ori_table()
        self.ud_edges_table()

        self.co_perm_table()
        self.eg_perm_table()
        self.ud_perm_table()

if __name__ == "__main__":
    table_maker = MoveTable()
    table_maker.make_tables()
    pass