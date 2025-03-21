#!/usr/bin/python3

import pyglet, sys, math
from pyglet.window import mouse, key, Window
from pyglet.gl import *
from math import sin, cos, acos
import numpy as np

# from google searches
from pyglet.math import Mat4, Vec3
import ctypes

class Scene(Window):
    # Initialize and run our environment
    def __init__(self, width=800, height=600, caption="Would you like to play a game?", resizable=False):
        # Build the OpenGL / Pyglet Window
        super().__init__(width=width, height=height, resizable=resizable, caption=caption)
        
        self.width = width
        self.height = height
        
        self.stepTheta = 5
        self.stepPhi = 5

        # make the window update every "frame"
        #pyglet.clock.schedule_interval(self.on_draw, 1/10.0)

        # Fix transparent issue...
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.angle = 0.0
        #self.phi = 0.0
        self.u = np.array([0,1,0], dtype='float64')
        self.p1 = np.array([0,0,0], dtype='float64')
         
        #self.rotations = [(self.angle, self.u)]
        self.rotations = Mat4.from_rotation(self.angle, Vec3(*self.u))

    # increment the cases
    def on_key_press(self, symbol, modifier):
        if symbol == key.C and modifier == key.MOD_CTRL:
            print('exiting...')
            sys.exit(0)
        elif symbol == key.LEFT:
            self.angle -= 1.0
            print(f'angle: {self.angle}')
            self.rotations = self.rotations.rotate( -math.pi/180, Vec3(0,1,0) )
        elif symbol == key.RIGHT:
            self.angle += 1.0
            print(f'angle: {self.angle}')
            self.rotations = self.rotations.rotate( math.pi/180, Vec3(0,1,0) )
        elif symbol == key.PAGEUP:
            self.stepPhi += 1
            self.stepTheta += 1
            print(f'stepTheta: {self.stepTheta}')
            print(f'stepPhi: {self.stepPhi}')
        elif symbol == key.PAGEDOWN:
            self.stepPhi -= 1
            self.stepTheta -= 1
            if self.stepPhi == 0 or self.stepTheta == 0:
                self.stepPhi = 1
                self.stepTheta = 1
            print(f'stepTheta: {self.stepTheta}')
            print(f'stepPhi: {self.stepPhi}')
        elif symbol == key.END:
                #fn = f'image{self.caseID}.png'
                #pyglet.image.get_buffer_manager().get_color_buffer().save(fn)
                #print('saved:',fn)
            pass 
        if self.angle < 0:
            self.angle += 360.0
        elif self.angle >= 360.0:
            self.angle -= 360.0
      
    def z(self,x,y):
        condition = pow(x-self.width/2.0, 2) + pow(y-self.height/2.0, 2)
        check = pow(self.height/2.0, 2)
        if condition < check:
            return np.sqrt(check - condition)
        else:
            return 0.1

    def on_mouse_press(self, x, y, button, modifiers):
        self.p1 = self.addRotate(x,y)

    def addRotate(self, x,y):
        newx = self.width / 2.0 - x
        newy = y - self.height / 2.0
        return np.array([-newx,newy, self.z(x,y)], dtype='float64')

    # calculate the angle offset based on the x value of the mouse
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        #if button != mouse.RIGHT:
            #return

        # x,y is from the bottom left, shift it to the center
        lerp = lambda x, l1,r1, l2,r2: ((x - l1) / (r1 - l1)) * (r2 - l2) + l2
        
        #theta = lerp(x, 0, self.width, -180, 180)
        #self.phi = lerp(y, 0, self.height, 180, -180)
        #self.angle = theta
        
        # arcball algorithm goes here
        p1 = self.p1
        p2 = self.addRotate(x, y)
        
        #print(f'{p1=}\n{p2=}')
        val = p1.dot(p2)
        denom = np.linalg.norm(p1) * np.linalg.norm(p2)
        #print('-'*100)
        #print(f'{denom=}')
        self.angle = acos( val / denom )
        self.u = np.cross(p1,p2) / denom
        #print(f'{self.u=}') 
        #print(f'{np.linalg.norm(self.u)=}')
        norm = np.linalg.norm(self.u)
        self.u /= norm if norm != 0 else 1
        #print(self.u)
        #print(np.sum(pow(self.u, 2)))
        #self.rotations.append((self.angle, self.u))
        # convert angle to radians
        self.rotations = self.rotations.rotate( self.angle, Vec3(*self.u) )
        self.p1 = p2

    # Event Handler for drawing the screen
    def on_draw(self, dt=0):
        self.clear()
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #glOrtho(0, width, 0, height, -1, 1)
        glFrustum(-5.0, 5.0, -5.0, 5.0, 5.0, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glColor3f(1.0, 1.0, 1.0)        # Set the point color to white
        # put the wirecube in
        glLoadIdentity()
        glPushMatrix()
        glTranslatef(0.0, 0.0, -60.0)   # Move the Cube into the Frustum
        #glRotatef(self.angle,0,1,0)
        #glRotatef(self.phi,1,0,0)
        # from arcball
        #glRotatef(self.angle, *self.u)
        
        # old way of rotating by storing all rotations
        #for theta, u in self.rotations:
            #glRotatef(theta, *u)
        
        # just use the saved rotations from quaternion
        floats = []
        #print('matrix')
        #print(self.rotations)
        for i in range(4):
            row = list(self.rotations.row(i))
            #print([f'{float(x):.3f}' for x in row])
            floats.extend(row)
        carray = (ctypes.c_float * len(floats))(*floats)
        #glMultMatrixf( ctypes.cast(floats, ctypes.POINTER(ctypes.c_float)) )
        glMultMatrixf(carray)

        self.WireCube(20)                     # Draw a 5x5x5 wire cube
        self.pointSphere(30)
        glPopMatrix()

    def gen(self, start, stop, step):
        while start < stop:
            yield start
            start += step

    def pointSphere(self, r):
        r = float(r)
       
        glBegin(GL_POINTS)
        for theta in self.gen(0, 360, self.stepTheta):
            for phi in self.gen(0, 180, self.stepPhi):
                x = r * cos(theta)*sin(phi)
                y = r * sin(theta)*sin(phi)
                z = r * cos(phi)
                glVertex3f(x,y,z)
        glEnd()

    def Rectangle(self, x_min, y_min, x_max, y_max):
        z_min = 0.0
        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(x_min, y_max, z_min)
        glVertex3f(x_min, y_min, z_min)
        glVertex3f(x_max, y_max, z_min)
        glVertex3f(x_max, y_min, z_min)
        glEnd()

    def Cube(self, dim):
        x_min, y_min, z_min = -0.5*dim, -0.5*dim, -0.5*dim
        x_max, y_max, z_max =  0.5*dim,  0.5*dim,  0.5*dim
        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(x_min, y_max, z_min)
        glVertex3f(x_min, y_min, z_min)
        glVertex3f(x_max, y_max, z_min)
        glVertex3f(x_max, y_min, z_min)
        glEnd()
        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(x_min, y_max, z_max)
        glVertex3f(x_min, y_min, z_max)
        glVertex3f(x_max, y_max, z_max)
        glVertex3f(x_max, y_min, z_max)
        glEnd()
        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(x_min, y_min, z_max)
        glVertex3f(x_min, y_min, z_min)
        glVertex3f(x_max, y_min, z_max)
        glVertex3f(x_max, y_min, z_min)
        glEnd()
        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(x_min, y_max, z_max)
        glVertex3f(x_min, y_max, z_min)
        glVertex3f(x_max, y_max, z_max)
        glVertex3f(x_max, y_max, z_min)
        glEnd()
        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(x_min, y_min, z_max)
        glVertex3f(x_min, y_min, z_min)
        glVertex3f(x_min, y_max, z_max)
        glVertex3f(x_min, y_max, z_min)
        glEnd()
        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(x_max, y_min, z_max)
        glVertex3f(x_max, y_min, z_min)
        glVertex3f(x_max, y_max, z_max)
        glVertex3f(x_max, y_max, z_min)
        glEnd()

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

# Run the following code if this script was run directly from the command line
if __name__ == '__main__':
    myGame = Scene(600, 500, "Transformations")
    pyglet.app.run()

