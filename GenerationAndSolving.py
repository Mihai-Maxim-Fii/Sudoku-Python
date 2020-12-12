
import numpy as np
import random
import copy
gameGrid=\
      [[0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0]]




def findNextCell(x,y,grid):
    for i in range(x,9):
        for j in range(y,9):
            if(grid[i][j]==0):
                return [i,j]
    for i in range(0,9):
        for j in range(0,9):
            if(grid[i][j]==0):
                return [i,j]
    return [-1,-1]



def isValid(x,y,grid,nr):
    blockX=x//3
    blockY=y//3
    for i in range(blockX*3,blockX*3+3):
        for j in range(blockY*3,blockY*3+3):
            if grid[i][j]==nr:
                return False

    for a in range(0,9):
        if grid[x][a]==nr:
            return False
        if grid[a][y]==nr:
            return False

    return True


def solveSudoku(grid,x,y):
    next=findNextCell(x,y,grid)
    if next[0]==-1:
        return True
    for nr in range(1,10):
        if isValid(next[0],next[1],grid,nr):
            grid[next[0]][next[1]]=nr
            if solveSudoku(grid,next[0],next[1]):
                return True
            grid[next[0]][next[1]]=0
    return False



def fillDiagonalSquares(gameGrid):
   numbers=[1,2,3,4,5,6,7,8,9]
   counter=0
   random.shuffle(numbers)
   for i in range(0,3):
       for j in range(0,3):
           gameGrid[i][j]=numbers[counter]
           counter+=1
   counter=0
   random.shuffle(numbers)
   for i in range(3,6):
       for j in range(3,6):
           gameGrid[i][j]=numbers[counter]
           counter+=1
   counter = 0
   random.shuffle(numbers)
   for i in range(6, 9):
       for j in range(6, 9):
           gameGrid[i][j] = numbers[counter]
           counter += 1


def createGame(level):
    temp=copy.deepcopy(gameGrid)
    fillDiagonalSquares(temp)
    solveSudoku(temp,0,0)
    while(level>0):
        x=random.randint(0,8)
        y=random.randint(0,8)
        if temp[x][y]!=0:
            temp[x][y]=0
            level-=1
    return temp





