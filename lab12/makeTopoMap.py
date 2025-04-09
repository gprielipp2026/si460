#!/usr/bin/python

# Simple library to create a matrix for use with contour mapping (isolines)
# SI460, Fall AY17, J. Kenney

def get(DB, row, col):
    if row in DB and col in DB[row]:
        return DB[row][col]
    else:
        return -1

def set(DB, row, col, val):
    if not row in DB:
        DB[row] = {}
    DB[row][col] = val

def get_matrix(seed=42, rows=400, cols=400, delta=3, maxval=20):
    import random, numpy
    random.seed(seed)
    DB = {}
    for row in range(rows):
        for col in range(cols):
            up = get(DB, row-1, col)
            lf = get(DB, row, col-1)
            if up == -1 and lf == -1:
                val = random.randint(1,10)
                val = 0
            elif up != -1 and lf == -1:
                val = random.randint(max(0, up-delta), up+delta)
            elif up == -1 and lf != -1:
                val = random.randint(max(0, lf-delta), lf+delta)
            else:
                if max(0, up-delta, lf-delta) == min(lf+delta, up+delta):
                    val = max(0, up-delta, lf-delta)
                elif max(0, up-delta, lf-delta) > min(lf+delta, up+delta):
                    val = random.randint(min(lf+delta, up+delta), max(0, up-delta, lf-delta))
                else:
                    val = random.randint(max(0, up-delta, lf-delta), min(lf+delta, up+delta))
            if val > maxval:
                val = maxval
            set(DB, row, col, val)
    M = []
    for row in range(rows):
        t = []
        for col in range(cols):
            t.append(get(DB,row,col))
        M.append(t)
    return numpy.array(M)

if __name__ == '__main__':
    M = get_matrix(rows=10, cols=10)
