import numpy as np
import random
import time
import cube_model
import rank
from cube import Cube

"""
This file calculates the move table for each coordinate
"""

class MoveTable:
    def __init__(self):
        ''' make a cube '''
        self.cube = Cube()

    def co_ori_table(self):
        co_ori_table = []
        for i in range(cube_model.StateSize.CO_ORI):
            cur_co_ori = rank.co_ori_inv(i)
            state_table = []
            for move in cube_model.MoveSpace:
                self.cube.set_co_ori(cur_co_ori)
                self.cube.move(move)
                state_table.append(rank.co_ori(self.cube.get_co_ori()))
            co_ori_table.append(state_table)
        np.save("table/co_ori_table", np.array(co_ori_table, dtype=np.uint16))

    def eg_ori_table(self):
        eg_ori_table = []
        for i in range(cube_model.StateSize.EG_ORI):
            cur_eg_ori = rank.eg_ori_inv(i)
            state_table = []
            for move in cube_model.MoveSpace:
                self.cube.set_eg_ori(cur_eg_ori)
                self.cube.move(move)
                state_table.append(rank.eg_ori(self.cube.get_eg_ori()))
            eg_ori_table.append(state_table)
        np.save("table/eg_ori_table", np.array(eg_ori_table, dtype=np.uint16))

    def ud_edges_table(self):
        ud_edges_table = []
        for i in range(cube_model.StateSize.UD_COMB):
            cur_ud_edges = rank.ud_edges_inv(i)
            state_table = []
            for move in cube_model.MoveSpace:
                self.cube.set_ud_egdes(cur_ud_edges)
                self.cube.move(move)
                state_table.append(rank.ud_edges(self.cube.get_ud_edges()))
            ud_edges_table.append(state_table)
        np.save("table/ud_edges_table", np.array(ud_edges_table, dtype=np.uint16))

    def co_perm_table(self):
        co_perm_table = []
        for i in range(cube_model.StateSize.CO_PERM):
            cur_co_perm = rank.co_perm_inv(i)
            state_table = [-1]*18
            for move in cube_model.G1Space:
                self.cube.set_co_perm(cur_co_perm)
                self.cube.move(move)
                state_table[move] = rank.co_perm(self.cube.get_co_perm())
            co_perm_table.append(state_table)
        np.save("table/co_perm_table", np.array(co_perm_table, dtype=np.uint16))
        return co_perm_table

    def eg_perm_table(self):
        eg_perm_table = []
        for i in range(cube_model.StateSize.EG_PERM):
            cur_eg_perm = rank.eg_perm_inv(i)
            state_table = [-1]*18
            for move in cube_model.G1Space:
                self.cube.set_eg_perm(cur_eg_perm)
                self.cube.move(move)
                state_table[move] = rank.eg_perm(self.cube.get_eg_perm())
            eg_perm_table.append(state_table)
        np.save("table/eg_perm_table", np.array(eg_perm_table, dtype=np.uint16))
    
    def ud_perm_table(self):
        ud_perm_table = []
        for i in range(cube_model.StateSize.UD_PERM):
            cur_ud_perm = rank.ud_perm_inv(i)
            state_table = [-1]*18
            for move in cube_model.G1Space:
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