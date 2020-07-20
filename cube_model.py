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
    UBL = 0; LUB = 8; BLU = 16
    URB = 1; BUR = 9; RBU = 17
    UFR = 2; RUF = 10; FRU = 18
    ULF = 3; FUL = 11; LFU = 19
    
    DFL = 4; LDF = 12; FLD = 20
    DRF = 5; FDR = 13; RFD = 21
    DBR = 6; RDB = 14; BRD = 22
    DLB = 7; BDL = 15; LBD = 23

def conor_to_char(corner):
    cor = corner%8
    cor_char = []
    if cor == Corner.UBL:
        cor_char = ['U', 'B', 'L']
    elif cor == Corner.URB:
        cor_char = ['U', 'R', 'B']
    elif cor == Corner.UFR:
        cor_char = ['U', 'F', 'R']
    elif cor == Corner.ULF:
        cor_char = ['U', 'L', 'F']
    elif cor == Corner.DFL:
        cor_char = ['D', 'F', 'L']
    elif cor == Corner.DRF:
        cor_char = ['D', 'R', 'F']
    elif cor == Corner.DBR:
        cor_char = ['D', 'B', 'R']
    elif cor == Corner.DLB:
        cor_char = ['D', 'L', 'B']

    cor_ori = corner//8
    if cor_ori == 1:
        tmp = cor_char = cor_char[2]
        cor_char[2] = cor_char[1]        
        cor_char[1] = cor_char[0]        
        cor_char[0] = tmp
    elif cor_ori == 2:
        tmp = cor_char = cor_char[0]
        cor_char[0] = cor_char[1]        
        cor_char[1] = cor_char[2]        
        cor_char[2] = tmp

    return cor_char


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

def edge_to_char(edge):
    eg = edge%12
    eg_char = []
    if eg == Edge.UB:
        eg_char = ['U', 'B']
    elif eg == Edge.UR:
        eg_char = ['U', 'R']
    elif eg == Edge.UF:
        eg_char = ['U', 'F']
    elif eg == Edge.UL:
        eg_char = ['U', 'L']
    elif eg == Edge.LB:
        eg_char = ['L', 'B']
    elif eg == Edge.RB:
        eg_char = ['R', 'B']
    elif eg == Edge.RF:
        eg_char = ['R', 'F']
    elif eg == Edge.LF:
        eg_char = ['L', 'F']
    elif eg == Edge.DF:
        eg_char = ['D', 'F']
    elif eg == Edge.DR:
        eg_char = ['D', 'R']
    elif eg == Edge.DB:
        eg_char = ['D', 'B']
    elif eg == Edge.DL:
        eg_char = ['D', 'L']

    eg_ori = edge//12
    if eg_ori == 1:
        tmp = eg_char[0]
        eg_char[0] = eg_char[1]
        eg_char[1] = tmp
    
    return eg_char


class CornerColor(IntEnum): 
    BYO = 0
    BRY = 1
    BWR = 2
    BOW = 3
    GWO = 4
    GRW = 5
    GYR = 6
    GOY = 7


class EdgeColor(IntEnum):
    BY = 0
    BR = 1
    BW = 2
    BO = 3
    OY = 4
    RY = 5
    RW = 6
    OW = 7
    GW = 8
    GR = 9
    GY = 10
    GO = 11


# unit testing
if __name__ == "__main__":
    pass