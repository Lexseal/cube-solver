from enum import IntEnum

class Facelets(IntEnum):
    '''
                 /------------\ 
                 | U1  U2  U3 |
                 |            |
                 | U4  U5  U6 |
                 |            |
                 | U7  U8  U9 |
    /------------|------------|-------------------------\ 
    | L1  L2  L3 | F1  F2  F3 | R1  R2  R3 | B1  B2  B3 |
    |            |            |            |            |
    | L4  L5  L6 | F4  F5  F6 | R4  R5  R6 | B4  B5  B6 |
    |            |            |            |            |
    | L7  L8  L9 | F7  F8  F9 | R7  R8  R9 | B7  B8  B9 |
    \------------|------------|-------------------------/
                 | D1  D2  D3 |
                 |            |
                 | D4  D5  D6 |
                 |            |
                 | D7  D8  D9 |
                 \------------/
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
        /---\ 
        | U |
    /---|---|-------\ 
    | L | F | R | B |
    \---|---|-------/
        | D |
        \---/
    U for Up Color
    L for Left Color...
    '''
    U=1

    L=2; F=3; R=4; B=5

    D=6

    '''
         /----\ 
         | BL |
    /----|----|---------\ 
    | OR | WI | RE | YE |
    \----|----|---------/
         | GR |
         \----/
    Alternatively, use the actual color to represent a cube.
    Note that the color scheme on each cube might differ.
    B for Blue
    O for Orange...
    '''
    BL=1

    OR=2; WI=3; RE=4; YE=5

    GR=6


class MoveSpace(IntEnum):
    '''
    U1 means rotate upper face by 90* clockwise.
    U2 means 180* and U3 means 270* or -90*.
    '''
    U1 = 1; U2 = 2; U3 = 3
    L1 = 1; L2 = 2; L3 = 3
    F1 = 1; F2 = 2; F3 = 3
    R1 = 1; R2 = 2; R3 = 3
    B1 = 1; B2 = 2; B3 = 3
    D1 = 1; D2 = 2; D3 = 3


class Corner(IntEnum):
    ''' Staring from upper left back, we go clockwise. '''
    ULB = 1; URB = 2
    ULF = 4; URF = 3

    DLB = 5; DRB = 6
    DLF = 8; DRF = 7


class Edge(IntEnum):
    ''' Starting from upper left, we go clockwise. '''
    UB = 1
    UL = 4; UR = 2
    UF = 3

    LB = 5; RB = 6
    LF = 8; RF = 7

    DB = 9
    DL = 12; DR = 10
    DF = 11


# unit testing
if __name__ == "__main__":
    pass