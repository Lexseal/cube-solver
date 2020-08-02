from enum import IntEnum

class Facelets(IntEnum):
    '''
                 -------------- 
                 | U1  U2  U3 |
                 |            |
                 | U4  U5  U6 |
                 |            |
                 | U7  U8  U9 |
    -------------|------------|-------------------------- 
    | L1  L2  L3 | F1  F2  F3 | R1  R2  R3 | B1  B2  B3 |
    |            |            |            |            |
    | L4  L5  L6 | F4  F5  F6 | R4  R5  R6 | B4  B5  B6 |
    |            |            |            |            |
    | L7  L8  L9 | F7  F8  F9 | R7  R8  R9 | B7  B8  B9 |
    -------------|------------|--------------------------
                 | D1  D2  D3 |
                 |            |
                 | D4  D5  D6 |
                 |            |
                 | D7  D8  D9 |
                 --------------
    U for Up
    L for Left...
    '''
    U1=0;  U2=1;  U3=2

    U4=3;  U5=4;  U6=5

    U7=6;  U8=7;  U9=8

    L1=9;  L2=10; L3=11; F1=18; F2=19; F3=20; R1=27; R2=28; R3=29; B1=36; B2=37; B3=38

    L4=12; L5=13; L6=14; F4=21; F5=22; F6=23; R4=30; R5=31; R6=32; B4=39; B5=40; B6=41

    L7=15; L8=16; L9=17; F7=24; F8=25; F9=26; R7=33; R8=34; R9=35; B7=42; B8=43; B9=44

    D1=45; D2=46; D3=47

    D4=48; D5=49; D6=50

    D7=51; D8=52; D9=53


class Color(IntEnum):
    '''
        ----- 
        | U |
    ----|---|-------- 
    | L | F | R | B |
    ----|---|--------
        | D |
        -----
    U for Up Color
    L for Left Color...
    '''
    U=1

    L=2; F=3; R=4; B=5

    D=6


class MoveSpace(IntEnum):
    '''
    U1 means rotate upper face by 90* clockwise.
    U2 means 180* and U3 means 270* or -90*.
    '''
    U1 = 0; U2 = 1; U3 = 2
    L1 = 3; L2 = 4; L3 = 5
    F1 = 6; F2 = 7; F3 = 8
    R1 = 9; R2 = 10; R3 = 11
    B1 = 12; B2 = 13; B3 = 14
    D1 = 15; D2 = 16; D3 = 17

move_lookup = []
move_lookup.append("U1")
move_lookup.append("U2")
move_lookup.append("U3")
move_lookup.append("L1")
move_lookup.append("L2")
move_lookup.append("L3")
move_lookup.append("F1")
move_lookup.append("F2")
move_lookup.append("F3")
move_lookup.append("R1")
move_lookup.append("R2")
move_lookup.append("R3")
move_lookup.append("B1")
move_lookup.append("B2")
move_lookup.append("B3")
move_lookup.append("D1")
move_lookup.append("D2")
move_lookup.append("D3")
move_reverse_loopup = {}
for i, move in enumerate(move_lookup):
    move_reverse_loopup[move] = i
def convert_move(move):
    if (len(move) == 1):
        move += "1"
    elif (move[1] == "'"):
        move = move[0]+"3"
    return move_reverse_loopup[move]


class G1Space(IntEnum):
    '''
    U1 means rotate upper face by 90* clockwise.
    U2 means 180* and U3 means 270* or -90*.
    '''
    U1 = 0; U2 = 1; U3 = 2
    L2 = 4
    F2 = 7
    R2 = 10
    B2 = 13
    D1 = 15; D2 = 16; D3 = 17


class Corner(IntEnum):
    '''
    Staring from upper left back.
    Rotations are counter clockwise.
    '''
    UBL = 0; BLU = 8; LUB = 16
    URB = 1; RBU = 9; BUR = 17
    UFR = 2; FRU = 10; RUF = 18
    ULF = 3; LFU = 11; FUL = 19
    
    DFL = 4; FLD = 12; LDF = 20
    DRF = 5; RFD = 13; FDR = 21
    DBR = 6; BRD = 14; RDB = 22
    DLB = 7; LBD = 15; BDL = 23

cor_char_lookup = []
cor_char_lookup.append(['U', 'B', 'L'])
cor_char_lookup.append(['U', 'R', 'B'])
cor_char_lookup.append(['U', 'F', 'R'])
cor_char_lookup.append(['U', 'L', 'F'])
cor_char_lookup.append(['D', 'F', 'L'])
cor_char_lookup.append(['D', 'R', 'F'])
cor_char_lookup.append(['D', 'B', 'R'])
cor_char_lookup.append(['D', 'L', 'B'])
def corner_to_char(corner, print=False):
    cor = corner%8
    cor_char = cor_char_lookup[cor].copy()

    cor_ori = corner//8
    if print:
        print(corner, cor, cor_ori, cor_char)
    if cor_ori == 1:
        tmp = cor_char[0]
        cor_char[0] = cor_char[1]        
        cor_char[1] = cor_char[2]        
        cor_char[2] = tmp
    elif cor_ori == 2:
        tmp = cor_char[2]
        cor_char[2] = cor_char[1]        
        cor_char[1] = cor_char[0]        
        cor_char[0] = tmp

    return cor_char

cor_num_loopup = {}
for i, chars in enumerate(cor_char_lookup):
    cor_num_loopup["".join(chars)] = i
def str_to_cor(cor_str):
    # reverse rotate
    cor_str_1stop = cor_str[1:3]+cor_str[0:1]
    cor_str_2stop = cor_str[2:3]+cor_str[0:2]
    if cor_str in cor_num_loopup:
        return cor_num_loopup[cor_str]
    elif cor_str_1stop in cor_num_loopup:
        return cor_num_loopup[cor_str_1stop]+8
    elif cor_str_2stop in cor_num_loopup:
        return cor_num_loopup[cor_str_2stop]+16


class Edge(IntEnum):
    ''' Starting from upper left. '''
    UB = 0; BU = 12
    UR = 1; RU = 13
    UF = 2; FU = 14
    UL = 3; LU = 15
    DB = 4; BD = 16
    DL = 5; LD = 17
    DF = 6; FD = 18
    DR = 7; RD = 19
    RB = 8; BR = 20
    RF = 9; FR = 21
    LF = 10; FL = 22
    LB = 11; BL = 23

eg_char_loopup = []
eg_char_loopup.append(['U', 'B'])
eg_char_loopup.append(['U', 'R'])
eg_char_loopup.append(['U', 'F'])
eg_char_loopup.append(['U', 'L'])
eg_char_loopup.append(['D', 'B'])
eg_char_loopup.append(['D', 'L'])
eg_char_loopup.append(['D', 'F'])
eg_char_loopup.append(['D', 'R'])
eg_char_loopup.append(['R', 'B'])
eg_char_loopup.append(['R', 'F'])
eg_char_loopup.append(['L', 'F'])
eg_char_loopup.append(['L', 'B'])


def edge_to_char(edge):
    eg = edge%12
    eg_char = eg_char_loopup[eg].copy()

    eg_ori = edge//12
    if eg_ori == 1:
        tmp = eg_char[0]
        eg_char[0] = eg_char[1]
        eg_char[1] = tmp
    
    return eg_char

eg_num_loopup = {}
for i, chars in enumerate(eg_char_loopup):
    eg_num_loopup["".join(chars)] = i
def str_to_eg(eg_str):
    # flip
    eg_flip = eg_str[1:2]+eg_str[0:1]
    if eg_str in eg_num_loopup:
        return eg_num_loopup[eg_str]
    elif eg_flip in eg_num_loopup:
        return eg_num_loopup[eg_flip]+12


# unit testing
if __name__ == "__main__":
    print(corner_to_char(7))
    pass