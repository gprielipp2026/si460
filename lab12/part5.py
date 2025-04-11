#!/usr/bin/env python3

import pyglet, sys
from pyglet.gl import *
from pyglet.window import Window, key, mouse
import numpy as np

from pyglet.math import Mat4, Vec3
import ctypes

import makeTopoMap

class Scene(Window):
    def __init__(self, M, width, height, threshold=6.5, thresholds=(0.5,19.5,1.0)):
        super().__init__(width=width, height=height, resizable=True, caption='Marching squares') 
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.M = M
        self.M_height, self.M_width = M.shape
        self.upperX = -self.M_width  / 2.0
        self.upperY =  self.M_height / 2.0

        # doing the hemisphere
        self.thresholds = thresholds

        print(f'Matrix is: {self.M_width}x{self.M_height}')
        
        self.sliding = False
        self.rotating = False

        self.p1 = self.p2 = np.array([0,0])
        self.translate = np.array([0,0])
        self.scale = np.array([0,0,1,1])
        self.arcball = Mat4.from_rotation(0.0, Vec3(0,0,0))

    def z(self,x,y,radius=None):
        if radius is None:
            r1 = self.height / 2.0
            r2 = self.width / 2.0
        else:
            r1 = r2 = radius

        condition = pow(x-r1, 2) + pow(y-r2, 2)
        check = pow(r2, 2)
        if condition < check:
            return np.sqrt(check - condition)
        else:
            return 0.1

    def gen(self, start, stop, step):
        while start < stop:
            yield start
            start += step

    def on_key_press(self, symbol, modifiers):
        if symbol == key.C and modifiers == key.MOD_CTRL:
            print('exiting...')
            sys.exit(0)

    def on_mouse_press(self, x, y, symbol, modifiers):
        if symbol == mouse.LEFT:
            self.p1 = self.p2 = np.array([x,y])
            self.sliding = True
        elif symbol == mouse.RIGHT:
            self.p1 = self.p2 = np.array([x,y,self.z(x,y)])
            self.rotating = True

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.sliding:
            self.p2 = np.array([x,y])
        elif self.rotating:
            self.p2 = np.array([x,y,self.z(x,y)])
            
            det = np.linalg.norm(self.p1) * np.linalg.norm(self.p2)
            
            # was having floating point precision errors that led to the value growing greater than 1
            theta = np.arccos( round(np.dot(self.p1, self.p2) / det, 5) ) 

            u = np.cross(self.p1, self.p2) / det
            norm = np.linalg.norm(u)
            u /= norm if norm != 0 else 1 

            self.arcball = self.arcball.rotate(theta, Vec3(*u)) 
            
            self.p1 = self.p2
            

    def on_mouse_release(self, x, y, symbol, modifiers):
        if self.sliding: 
            self.translate += self.p2 - self.p1
            self.p1 = self.p2 = np.array([0,0])
            self.sliding = False
        elif self.rotating:
            self.p1 = self.p2 = np.array([0,0])
            self.rotating = False

    def on_mouse_scroll(self, x, y, scrollx, scrolly):
        factor = 1.1 if scrolly > 0 else 0.9
        self.scale = factor * self.scale
        self.scale[0:2] = [x, y]

    def matrix2world(self, x, y):
        sclX = self.M_width / 2.0
        sclY = self.M_height / 2.0
    
        lerp = lambda x, lx, rx, nl, nr: ( (float(x) - lx) / (rx - lx) ) * ( nr - nl ) + nl 
        
        x = lerp(x, -sclX, sclX, -self.width/2.0, self.width/2.0)
        y = lerp(y, -sclY, sclY, -self.height/2.0, self.height/2.0)
        
        return (x,y)

    def square(self, row, col):
        a = M[row  ][col  ] # value of a
        b = M[row  ][col+1] # value of b
        c = M[row+1][col+1] # value of c
        d = M[row+1][col  ] # value of d
        ax = self.upperX + col # x coordinate of a, Hint: use upperX and col to calculate this
        ay = self.upperY - row # y coordinate of a, Hint: use upperY and row to calculate this
        
        return ((ax,ay, a), (ax+1,ay, b), (ax+1,ay-1, c), (ax,ay-1, d))

    def hemisphere(self, x, y, radius, step):
        return ((x,y, self.z(x,y,radius)), (x+step, y, self.z(x+step,y,radius)), (x+step, y-step, self.z(x+step,y-step,radius)), (x,y-step,self.z(x,y-step,radius)))

    def sombrero(self, x, y, radius, step,zscale=1):
        z = lambda r: zscale*(np.sin(r) / float(r)) if abs(r) > 0 else zscale
        r = lambda x,y: np.sqrt(pow(x,2) + pow(y,2))
        """
        clockwise function
        a b
        d c
        """
        a = (x, y, z(r(x,y)))
        b = (x+step, y, z(r(x+step, y)))
        c = (x+step, y-step, z(r(x+step, y-step)))
        d = (x, y-step, z(r(x,y-step)))
        
        return (a, b, c, d)

    def on_draw(self, dt=0):            

        # clear the screen
        self.clear()

        # set viewport and frustum
        glViewport(0,0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        scale = 10.0
        glFrustum(-scale, scale, -scale, scale, 5.0, 10000.0)
        glMatrixMode(GL_MODELVIEW)

        # set environment to handle depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # draw the stuff
        glLoadIdentity()

        # translate the matrix based on the left mouse click
        tx,ty = (self.translate + ((self.p2 - self.p1) if self.sliding else np.array([0,0])))
        glTranslatef(tx, ty, -100.0)
        
        # scale the world around the cursor based on the scroll wheel
        tsx, tsy, sx, sy = self.scale
        
        glScalef(sx, sy, sy)
        # rotate the world based on Arcball and the right mouse click
        floats = []
        for i in range(4):
            row = list(self.arcball.row(i))
            floats.extend(row)
        carray = (ctypes.c_float * len(floats))(*floats)
        glMultMatrixf(carray)
 
        # cube to help visualize rotation
        #glColor4f(0.0,1.0,0.0,1.0)
        #self.WireCube(30)
        
        # make the toroid
        R = 20
        r = 10

        rsqd = r*r 
        Rsqd = R*R 

        step = 0.5
        zscale = 5

        sidelen = int(np.floor(2 * R / step))
        M = np.zeros((sidelen,sidelen,3), dtype=np.float64)

        maxval = 0.0
        minval = 10000.0
        for row in range(sidelen):
            for col in range(sidelen):
                x = col - sidelen / 2.0
                y = sidelen / 2.0 - row
                z = 0.0

                checkval = x*x + y*y
                 
                # check x,y inside torus
                if checkval >= rsqd and checkval <= Rsqd:
                    # find z value
                    percent = (checkval - rsqd) / (Rsqd - rsqd)
                    px = percent - 0.5
                    z = zscale * np.sqrt( 1 - px*px )

                maxval = max(z,maxval)
                minval = min(z,minval)
                M[row][col] = np.array([x,y,z])
        self.thresholds = (minval, maxval, step)

        # draw the half toroid
        glBegin(GL_TRIANGLES)
        for row in range(sidelen-1):
            for col in range(sidelen-1):
                """
                a b
                c d
                """
                
                a = M[row  ][col  ]
                b = M[row  ][col+1]
                c = M[row+1][col  ]
                d = M[row+1][col+1]

                ca = self.get_color(a[2])
                cb = self.get_color(b[2])
                cc = self.get_color(c[2])
                cd = self.get_color(d[2])

                glColor4f(*ca)
                glVertex3f(*a)
                glColor4f(*cb)
                glVertex3f(*b)
                glColor4f(*cc)
                glVertex3f(*c)

                glColor4f(*cb)
                glVertex3f(*b)
                glColor4f(*cc)
                glVertex3f(*c)
                glColor4f(*cd)
                glVertex3f(*d)

        glEnd()


    def get_color(self, val):
        # stop - start + 1
        rangewidth = self.thresholds[1] - self.thresholds[0] + 1
        percent = val / rangewidth
        if percent <= 0.01:
            percent = 0.1
        return (percent, percent, percent, 1.0)


    def WireCube(self, dim):
        x_min, y_min, z_min = -0.5*dim, -0.5*dim, -0.5*dim
        x_max, y_max, z_max =  0.5*dim,  0.5*dim,  0.5*dim
        glBegin(GL_LINE_STRIP)
        glVertex3f(x_min, y_min, z_min)
        glVertex3f(x_max, y_min, z_min)
        glVertex3f(x_max, y_max, z_min)
        glVertex3f(x_min, y_max, z_min)
        glVertex3f(x_min, y_min, z_min)
        glVertex3f(x_min, y_min, z_max)
        glVertex3f(x_max, y_min, z_max)
        glVertex3f(x_max, y_max, z_max)
        glVertex3f(x_min, y_max, z_max)
        glVertex3f(x_min, y_min, z_max)
        glVertex3f(x_min, y_max, z_max)
        glVertex3f(x_min, y_max, z_min)
        glVertex3f(x_max, y_max, z_min)
        glVertex3f(x_max, y_max, z_max)
        glVertex3f(x_max, y_min, z_max)
        glVertex3f(x_max, y_min, z_min)
        glEnd()

    
if __name__ == '__main__':

    #M = [[ 0,  1,  2,  4,  4,  6,  7,  4,  5,  2 ],
         #[ 3,  2,  4,  2,  2,  5,  7,  7,  7,  4 ],
         #[ 1,  1,  4,  1,  0,  2,  4,  6,  4,  7 ],
         #[ 2,  3,  5,  4,  2,  5,  5,  6,  7,  7 ],
         #[ 1,  2,  2,  1,  1,  3,  3,  5,  7, 10 ],
         #[ 2,  3,  4,  4,  3,  4,  5,  5,  8,  8 ],
         #[ 2,  5,  2,  3,  4,  6,  8,  6,  7,  9 ],
         #[ 4,  6,  3,  5,  7,  5,  7,  6,  4,  6 ],
         #[ 4,  6,  3,  4,  4,  5,  5,  3,  3,  6 ],
         #[ 7,  7,  4,  1,  1,  3,  6,  5,  6,  5 ]]

    M = makeTopoMap.get_matrix(seed=3, rows=10, cols=10, delta=3, maxval=20)
    #M = makeTopoMap.get_matrix(seed=3, rows=100, cols=60, delta=3, maxval=20)

    #M = [[6,6,6,6,6,6],
         #[6,6,7,7,7,6],
         #[6,7,6,7,7,6],
         #[6,7,7,7,6,6],
         #[6,7,7,6,7,6],
         #[6,6,6,6,6,6]]

    start, stop, step = 0.5, 19.5, 1.0 
    scene = Scene(np.array(M), 500, 500, thresholds=(start,stop,step))
    pyglet.app.run()



