#!/usr/bin/env python3

# load in pyglet libraries
import pyglet
from pyglet.gl import *
import math
import sys
# the window
window = pyglet.window.Window(400,400,resizable=False, caption='ex1.py')

if len(sys.argv) != 1:
    print('usage: python3 circle.py <numVertices>')
    exit(0)

numVertices = int(sys.argv)

def drawCircle(X, Y, R):#, numVertices=100):
    global numVertices
    theta = 0.0
    deltaTheta = 2.0 * math.pi / float(numVertices)
    glBegin(GL_LINE_LOOP)
    while theta < 2.0 * math.pi:
        # point on circle
        x, y = X + R * math.cos(theta), Y + R * math.sin(theta)
        glVertex3f(x, y, 0.0)
        theta += deltaTheta
    glEnd()


# how to draw whats inside the window
@window.event
def on_draw():
    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 100.0, 0.0, 100.0, -2.0, 1.0)
    glMatrixMode(gl.GL_MODELVIEW)
    glLoadIdentity()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # create a circle:
    # centered at (X,Y) with radius R:
    glColor3f(0.5, 0.0, 0.7)
    drawCircle(100.0,100.0, 25.0)    

    # you can create any curve with GL_LINE_STRIP if you can find points along it


pyglet.app.run()
