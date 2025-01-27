#!/usr/bin/env python3

# load in pyglet libraries
import pyglet
from pyglet.gl import *
import math

# the window
window = pyglet.window.Window(400,400,resizable=False, caption='ex1.py')

def drawCircle(X, Y, R, numVertices=100):
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

    # draws two triangles and some points with different colors
    """
    Color has the same convention:
    glColor(dimension)(type)
    dimension: 3 or 4 (4th can be alpha)
    type: float(f)
    0.0 is 0
    1.0 is 255 (ie full value)
    """
    glColor3f(1.0, 1.0, 1.0) # White
    # glBegin(PRIMITIVE) - say you are making a PRIMITIVE with the next vertices
    """
    OpenGL Primitives: 
    - GL_POINTS
    - GL_LINES
    - GL_LINE_LOOP
    - GL_LINE_STRIP
    # note: all triangles default to being filled in
    - GL_TRIANGLES
    - GL_TRIANGLE_STRIP
    - GL_TRIANGLE_FAN
    """
    glBegin(GL_TRIANGLES)
    # vertices of PRIMITIVE
    """
    Vertex Naming Scheme
    glVertex(Dimension)(Type)
    Dimensions: 2 or 3
    Types: Integer(i), Float(f), Double(d)
    """
    glVertex3f(10.0, 10.0, 0.0)
    glVertex3f(60.0, 10.0, 0.0)
    glVertex3f(60.0, 60.0, 0.0)
    # glEnd() - finish the PRIMITIVE
    glEnd()

    glColor3f(0.79, 0.19, 0.99)   # Purple
    glBegin(GL_TRIANGLES)
    glVertex3f(45.0, 10.0, 0.0)
    glVertex3f(85.0, 10.0, 0.0)
    glVertex3f(85.0, 85.0, 0.0)
    glEnd()

    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)   # Red
    glVertex3f(8.0, 8.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)    # Green
    glVertex3f(62.0, 8.0, 0.0)
    glColor3f(0.0, 0.0, 1.0)    # Blue
    glVertex3f(62.0, 62.0, 0.0)
    glColor3f(1.0, 1.0, 0.0)    # Yellow
    glVertex3f(8.0, 62.0, 0.0)
    glEnd()

    # create a circle:
    # centered at (X,Y) with radius R:
    glColor3f(0.5, 0.0, 0.7)
    drawCircle(100.0,100.0, 25.0)    

    # you can create any curve with GL_LINE_STRIP if you can find points along it


pyglet.app.run()
