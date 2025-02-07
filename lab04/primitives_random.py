#!/usr/bin/env python3

# load in pyglet libraries
import pyglet
from pyglet.gl import *
import math
import sys
import random
# the window
window = pyglet.window.Window(400,400,resizable=False, caption='ex1.py')



if len(sys.argv) == 1:
    print('usage: python3 primitives.py <...vertices> <primitive>')
    exit(0)

PRIMITIVES = {'GL_POINTS': 1,\
              'GL_LINES': 2,\
              'GL_LINE_STRIP': 2,\
              'GL_LINE_LOOP': 2,\
              'GL_TRIANGLES': 3,\
              'GL_TRIANGLE_STRIP': 3,\
              'GL_TRIANGLE_FAN': 3}

# do some error checking:
primitive = sys.argv[-1]
if primitive not in PRIMITIVES:
    print('need to give a primitive')
    exit(0)
#if any([x in primitive for x in ['LOOP', 'STRIP', 'FAN']]):
    # ensure there are at least that amount of vertices
    #if (len(sys.argv) - 2) / 2 < PRIMITIVES[primitive]:
        #print(f'{primitive} requires at least {PRIMITIVES[primitive]} points')
        #exit(0)
#elif ((len(sys.argv) - 2) / 2) % PRIMITIVES[primitive] != 0:
    # need exactly that many points to define the primitive
    #print(f'{primitive} requires exactly {PRIMITIVES[primitive]} points per {primitive}')
    #exit(0)

vertices = [(int(x), int(y)) for x,y in zip(sys.argv[1:-1:2],sys.argv[2:-1:2])]
print(vertices)

# thought about just evaling a string instead of this lookup table
STR2PRIM =   {'GL_POINTS': GL_POINTS,\
              'GL_LINES': GL_LINES,\
              'GL_LINE_STRIP': GL_LINE_STRIP,\
              'GL_LINE_LOOP': GL_LINE_LOOP,\
              'GL_TRIANGLES': GL_TRIANGLES,\
              'GL_TRIANGLE_STRIP': GL_TRIANGLE_STRIP,\
              'GL_TRIANGLE_FAN': GL_TRIANGLE_FAN}

saved = False

def save(fn):
    saved = True
    pyglet.gl.glClearColor(0,0,0,1)
    pyglet.image.get_buffer_manager().get_color_buffer().save(fn)
    

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
    
    # start the primitive
    glBegin(STR2PRIM[primitive])
    for x,y in vertices:
        color = [random.uniform(0,1) for _ in range(3)]
        glColor3f(*color)
        glVertex3f(x, y, 0.0)
    glEnd()
    
    if not saved:
        save(f'{primitive}_random.png')


pyglet.app.run()

