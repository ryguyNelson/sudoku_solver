## Sudoku Solver 
# Author: Ryan Nelson
#
# Description: Automatic sudoku puzzle solver. 
# Pass puzzle as command line arguments in the form show below. Results printed with updates
# in yellow.
#
# Example puzzle.
# 39_6_1__8 4__7_____ 58__42__7 ____63__2 2___87_5_ 8735_9_1_ ______89_ ___8_4_2_ 9_____4__
#
# 6/29/2020

import sys
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

sudoku_arr = sys.argv[1:len(sys.argv)]

#sudoku_arr = ['39_6_1__8','4__7_____','58__42__7','____63__2','2___87_5_','8735_9_1_','______89_','___8_4_2_','9_____4__']
#sudoku_arr = ['___3_74__','9____4__8','37_____6_','82_9__6__','__12__9_4','_4__38_5_','2_869_7__','_9_______','75______6']
sudoku = []

for i in sudoku_arr:
    sudoku.append(list(i))

sudoku_cpy = [x[:] for x in sudoku] #copy of initial puzzle for printing change highlights

def printBoard():
    for i in range(len(sudoku)):
        if i == 0:
            print('┏━━━┯━━━┯━━━┳━━━┯━━━┯━━━┳━━━┯━━━┯━━━┓')
        elif i % 3 == 0:
            print('┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫')
        else: 
            print('┠───┼───┼───╂───┼───┼───╂───┼───┼───┨')
        for j in range(len(sudoku[i])):
            if j == 0:
                print("┃", end='')
            elif j % 3 == 0:
                print('┃', end='')
            else: 
                print('│', end='')
            if (sudoku[i][j] != sudoku_cpy[i][j]):
                print(bcolors.WARNING + ' {0} '.format(sudoku[i][j]) + bcolors.ENDC, end='')
                #print(' {0} '.format(sudoku[i][j]), end='')
            else:
                print(' {0} '.format(sudoku[i][j]), end='')
        print('┃')
    print('┗━━━┷━━━┷━━━┻━━━┷━━━┷━━━┻━━━┷━━━┷━━━┛')

def getSimilar(list1, list2):
    list_diff = []
    for item in list1:
        if item in list2:
            list_diff.append(item)
    return list_diff

def getPossibles():
    pos = []
    for n in range(1, 10):
        pos.append(str(n))
    return pos

def getSquareIndex(val):
    if (val > 5):
        return 6
    elif (val > 2):
        return 3
    else:
        return 0

#used in the compute Grid algorithm
def getValue(i, j):
    h_pos = getPossibles()
    v_pos = getPossibles()
    s_pos = getPossibles()

    for k in range(len(sudoku[i])):
        if sudoku[i][k] in v_pos:
            v_pos.remove(sudoku[i][k])
    
    for l in range(len(sudoku)):
        if sudoku[l][j] in h_pos:
            h_pos.remove(sudoku[l][j])

    s_h = getSquareIndex(i)
    s_v = getSquareIndex(j)
    for h in range(s_h, s_h + 3):
        for g in range(s_v, s_v + 3):
            if (sudoku[h][g] in s_pos):
                s_pos.remove(sudoku[h][g])

    similar = getSimilar(getSimilar(v_pos, h_pos), s_pos)
    # print(similar)
    if (len(similar) == 1):
        return similar[0]
    else:
        return '_'  ##only return a number if the difference of the three possible arrays only returns 1 value

#used in the calculate game method which uses a more robust algorithm
def getPossibleValues(i, j):
    h_pos = getPossibles()
    v_pos = getPossibles()
    s_pos = getPossibles()

    for k in range(len(sudoku[i])):
        if sudoku[i][k] in v_pos:
            v_pos.remove(sudoku[i][k])
    
    for l in range(len(sudoku)):
        if sudoku[l][j] in h_pos:
            h_pos.remove(sudoku[l][j])

    s_h = getSquareIndex(i)
    s_v = getSquareIndex(j)
    for h in range(s_h, s_h + 2):
        for g in range(s_v, s_v + 2):
            if (sudoku[h][g] in s_pos):
                s_pos.remove(sudoku[h][g])

    similar = getSimilar(getSimilar(v_pos, h_pos), s_pos)
    return similar      #return possible values for cell

def computeGrid():
    for i in range(len(sudoku)):
        for j in range(len(sudoku[i])):
            if (sudoku[i][j] == '_'):
                sudoku[i][j] = getValue(i, j)


def calculateGame():
    s_vals = getPossibles()

    for n in s_vals:
        for i in range(len(sudoku)): #for each row
            s_poss = []
            for j in range(len(sudoku[i])): #for each spot
                if (sudoku[i][j] == n):
                    continue
                if (sudoku[i][j] == '_'):
                    if (n in getPossibleValues(i,j)):
                        s_poss.append([i,j])
            if (len(s_poss) == 1):
                sudoku[s_poss[0][0]][s_poss[0][1]] = n
    
    for n in s_vals:
        for i in range(0,9): #for each row
            s_poss = []
            for j in range(0,9): #for each spot
                if (sudoku[j][i] == n):
                    continue
                if (sudoku[j][i] == '_'):
                    if (n in getPossibleValues(j,i)):
                        s_poss.append([j,i])
            if (len(s_poss) == 1):
                sudoku[s_poss[0][0]][s_poss[0][1]] = n

#check for incomplete squares
def checkDone():
    for i in range(len(sudoku)):
        if '_' in sudoku[i]:
            return False
    return True

iterations = 0
#repeat calculations if puzzle incomplete
#restrict to 100 iterations in case no solution is able to be found
while not checkDone() and iterations < 100:
    calculateGame()
    computeGrid()
    iterations += 1
printBoard()
