#!/usr/bin/python3 -B

# This library assists in determining where the tiles will be placed on
# the game board.

# Import the pyglet library
import pyglet, sys

# A function to cleate a useful grid from the board file...
def board2grid(board, tilepath='sprites/tiles', returnSize=False):
    board = board.split('\n')[1:-2]
    board.reverse()
    results = {}
    resultsType = {}
    row = 0
    max_cols = 0
    for line in board:
        col = 0
        line = line[2:]
        while len(line) > 2:
            current = line[:3].strip()
            line = line[3:]
            if current != '':
                if not row in results:
                    results[row] = {}
                    resultsType[row] = {}
                try:
                    results[row][col] = pyglet.image.load(tilepath+"/"+current+".png")
                    resultsType[row][col] = current
                except:
                    print('Bad definition at row='+str(row) +', col='+str(col)+', image='+current+'.png')
            if col > max_cols:
                max_cols = col
            col += 1
        row += 1
    if returnSize:
        return results, row, max_cols
    return results

# Here is a function that will determine where the enemies should start
# based on the definition above.
def positionEnemies(board):
    board = board.split('\n')[1:-2]
    board.reverse()
    results = []
    row = 0
    max_cols = 0
    for line in board:
        col = 0
        line = line[2:]
        while len(line) > 2:
            current = line[:3].strip()
            line = line[3:]
            if current != '':
                results.append([col,row,current])
            if col > max_cols:
                max_cols = col
            col += 1
        row += 1
    return results
