import numpy as np
import random
import copy
import pygame
import sys
import math
#functions and classes to creat the game
rowOfBoard = 6
columnOfBoard = 7
#you can change difficulty between (0,5)
level=4
# RGB parameters
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

def creatBaord():
    board=np.zeros((rowOfBoard,columnOfBoard))
    return board

def checkMove(board,move):
    return board[rowOfBoard-1][move]==0

def findNextEmptyRow(board,column):
    for i in range(rowOfBoard):
        if board[i][column]==0:
            return i

def actionMove(board,row,column,player):
    board[row][column]=player

def isGoal(board,player):
    #check horizontaly
    for i in range(rowOfBoard):
        for j in range(columnOfBoard-3):
            if board[i][j]==player and board[i][j+1]==player and board[i][j+2]==player and board[i][j+3]==player:
                return True
    # check verticaly
    for i in range(rowOfBoard-3):
        for j in range(columnOfBoard):
            if board[i][j] == player and board[i+1][j] == player and board[i+2][j] == player and board[i+3][j] == player:
                return True
    #check positively sloped diameters
    for i in range(rowOfBoard-3):
        for j in range(columnOfBoard-3):
            if board[i][j] == player and board[i+1][j+1] == player and board[i+2][j+2] == player and board[i+3][j+3] == player:
                return True

    #chech negatively sloped diameters
    for i in range(3,rowOfBoard):
        for j in range(columnOfBoard-3):
            if board[i][j] == player and board[i-1][j+1] == player and board[i-2][j+2] == player and board[i-3][j+3] == player:
                return True

def boxValue(box,player):
    value=0
    opp_player=1
    if player==1:
        opp_player=2
    if box.count(player)==4:
        value+=100
    elif box.count(player)==3 and box.count(0)==1:
        value+=5
    elif box.count(player) == 2 and box.count(0) == 2:
        value+=2
    if box.count(opp_player)==3 and box.count(0)==1:
        value-=8
    if box.count(opp_player)==2 and box.count(0)==2:
        value-=2
    return value


def heuristic_evaluate(board,player):
    value=0
    #Horizone value
    for r in range(rowOfBoard):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(columnOfBoard - 3):
            box= row_array[c:c + 4]
            value += boxValue(box, player)
    #Vertical value
    for c in range(columnOfBoard):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(rowOfBoard - 3):
            box= col_array[r:r + 4]
            value += boxValue(box, player)
    #positive sloped diameter Value
    for r in range(rowOfBoard-3):
        for c in range(columnOfBoard - 3):
            box=[board[r + i][c + i] for i in range(4)]
            value += boxValue(box, player)
    #negative sloped diameter Value
    for r in range(rowOfBoard-3):
        for c in range(columnOfBoard - 3):
            box=[board[r+3 - i][c + i] for i in range(4)]
            value += boxValue(box, player)
    #center value
    centerArray=[int(i) for i in list(board[:,columnOfBoard//2])]
    numberOfCentersTaken=centerArray.count(player)
    value += numberOfCentersTaken*4
    return value

def getValidMoves(board):
    validMoves = []
    for i in range(columnOfBoard):
        if checkMove(board, i):
            validMoves.append(i)
    return validMoves

def bestMove(board,player):
    validMoves=getValidMoves(board)
    bestValue=-10000
    bestColumn=random.choice(validMoves)
    for column in validMoves:
        row=findNextEmptyRow(board,column)
        temporaryBoard=copy.deepcopy(board)
        actionMove(temporaryBoard,row,column,player)
        value=heuristic_evaluate(temporaryBoard,player)
        if value>bestValue:
            bestValue=value
            bestColumn=column
    return bestColumn

def isTherminal(board):
    return isGoal(board,1) or isGoal(board,2) or len(getValidMoves(board))==0

def alpha_beta_pruning(board,depth,alpha,beta,goalIsMax):
    validMoves=getValidMoves(board)
    if depth==0 or isTherminal(board):
        if isTherminal(board):
            if isGoal(board,1):
                return (None,-1000000)
            elif isGoal(board,2):
                return (None,1000000)
            else:
                return (None,0)
        else:#zero deph
            return (None,heuristic_evaluate(board,2))

    if goalIsMax:
        value=-math.inf
        column=random.choice(getValidMoves(board))
        for c in getValidMoves(board):
            row=findNextEmptyRow(board,c)
            tempBoard=copy.deepcopy(board)
            actionMove(tempBoard,row,c,2)
            newValue=alpha_beta_pruning(tempBoard,depth-1,alpha,beta,False)[1]
            if(newValue>value):
                value=newValue
                column=c
            alpha=max(alpha,value)
            if(alpha>=beta):
                break
        return column,value

    else:#goal is Minimize
        value = math.inf
        column = random.choice(getValidMoves(board))
        for c in getValidMoves(board):
            row = findNextEmptyRow(board,c)
            tempBoard = copy.deepcopy(board)
            actionMove(tempBoard, row, c, 1)
            newValue = alpha_beta_pruning(tempBoard, depth - 1, alpha, beta, True)[1]
            if (newValue < value):
                value = newValue
                column = c
            alpha = min(alpha, value)
            if (alpha >= beta):
                break
        return column, value
def draw_board(board):
    for c in range(columnOfBoard):
        for r in range(rowOfBoard):
            pygame.draw.rect(screen, YELLOW, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(columnOfBoard):
        for r in range(rowOfBoard):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, BLUE, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

gameFinished=False
turnOfPlayer1=bool(random.getrandbits(1))
board=creatBaord()
pygame.init()
SQUARESIZE = 100
width=columnOfBoard*SQUARESIZE
height=(rowOfBoard+1)*SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)





while not gameFinished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turnOfPlayer1:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            #player one turn
            if turnOfPlayer1:
                posx = event.pos[0]
                player1Move=int(math.floor(posx / SQUARESIZE))
                if checkMove(board,player1Move):
                    row=findNextEmptyRow(board,player1Move)
                    actionMove(board,row,player1Move,1)
                    if (isGoal(board, 1)):
                        label = myfont.render("Player 1 wins!", 1, RED)
                        screen.blit(label, (40, 10))
                        gameFinished = True
                    turnOfPlayer1 = not turnOfPlayer1
                    draw_board(board)

    #player two turn
    if not gameFinished and not turnOfPlayer1:
        player2Move,alphascore=alpha_beta_pruning(board,level,-math.inf,math.inf,True)
        if checkMove(board, player2Move) :
            row = findNextEmptyRow(board, player2Move)
            actionMove(board, row, player2Move, 2)
            if (isGoal(board, 2)):
                label = myfont.render("Player 2 wins!", 1, BLUE)
                screen.blit(label, (40, 10))
                gameFinished = True
            draw_board(board)
            turnOfPlayer1=not turnOfPlayer1

    if  gameFinished:
        pygame.time.wait(7000)



