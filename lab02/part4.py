import numpy as np
from graphics import *

def randel():
    return np.random.random_sample((1,3))[0]

def randomCube(fll, bur, n):
    vdiag = (bur - fll).v
    return [Point3D(vdiag * randel() + fll.v) for _ in range(n)]



if __name__ == '__main__':
    print('\n'.join([str(x) for x in randomCube( Point3D(10,10,10), Point3D(20,20,20), 10000 )]))
