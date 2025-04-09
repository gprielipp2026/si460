#!/usr/bin/python3

import pyglet
from pyglet.window import mouse, key
from pyglet.gl import *

class Scene:

    # Move objects between keyboard input
    def movement(self, dt):
        print('%f seconds since last callback' %dt)
        self.box_position = self.box_position - 0.2

    # Initialize and run our environment
    def __init__(self, width=800, height=600, caption="Would you like to play a game?", resizable=False):

        # Build the OpenGL / Pyglet Window
        self.window = pyglet.window.Window(width=width, height=height, resizable=resizable, caption=caption)

        # Fix transparent issue...
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Schedule the event
        pyglet.clock.schedule_interval(self.movement, 1.0/60.0)

        # Lets move the box
        self.box_position = 0

        # Event Handler for drawing the screen
        @self.window.event
        def on_draw():
            self.window.clear()

            glViewport(0, 0, width, height)
            glMatrixMode(gl.GL_PROJECTION)
            glLoadIdentity()
            #glOrtho(0, width, 0, height, -1, 1)
            glFrustum(-5.0, 5.0, -5.0, 5.0, 5.0, 100.0)
            glMatrixMode(gl.GL_MODELVIEW)

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()

            glColor3f(1.0, 1.0, 1.0)

            glTranslatef(0.0, 0.0, -15.0+self.box_position)
            WireCube(5)

        def Rectangle(x_min, y_min, x_max, y_max):
            z_min = 0.0
            glBegin(GL_TRIANGLE_STRIP)
            glVertex3f(x_min, y_max, z_min)
            glVertex3f(x_min, y_min, z_min)
            glVertex3f(x_max, y_max, z_min)
            glVertex3f(x_max, y_min, z_min)
            glEnd()

        def Cube(dim):
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

        def WireCube(dim):
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
    myGame = Scene(600, 500, "Example")
    debugging = pyglet.window.event.WindowEventLogger()
    myGame.window.push_handlers(debugging)
    pyglet.app.run()