#!/usr/bin/python3

import pyglet
from pyglet.window import mouse, key
from pyglet.gl import *
import math
import sys
import json

# Our OpenGL Graphical Environment!
class Scene:

    # Initialize and run our environment
    def __init__(self, width=800, height=600, caption="Would you like to play a game?", resizable=False, saveFN = None, loadFN = None):

        # Build the OpenGL / Pyglet Window
        self.window = pyglet.window.Window(width=width, height=height, resizable=resizable, caption=caption)
        self.width = width
        self.height = height

        self.caption = caption
        
        self.save = saveFN

        # Fix transparency issue...
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # determine if the app needs to display any points
        self.drawing = False
        self.loadPointsAndLines(loadFN)

        def inside(x, y, bounds):
            return x >= bounds[0] and x <= bounds[2] and y >= bounds[1] and y <= bounds[3]
    
        # c key = clear
        # q key = quit program
        @self.window.event
        def on_key_press(symbol, modifiers):
            print(['key', symbol, modifiers])
            if symbol == key.END:
                pyglet.image.get_buffer_manager().get_color_buffer().save('house.png')
            if modifiers == 0:
                if symbol == key.C:
                    self.drawing = False
                    self.points = []
                    self.lines = []
                elif symbol == key.Q:
                    self.quit()

        # handler for when the mouse is pressed in 
        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            self.drawing = True
            print(['mouse',x, y, button, modifiers])
            if inside(x, y, self.screen):
                self.points.append( (x,y) )
                self.lines.append( ((x,y), (x,y)) )
        
        # handler for when the mouse is released
        @self.window.event
        def on_mouse_release(x, y, button, modifiers):
            self.drawing = False
            print(['mouse', x, y, button, modifiers])


        # handler for when the mouse moves
        # need to add points if the mouse is pressed
        @self.window.event
        def on_mouse_drag(x, y, dx, dy, button, modifiers):
            print(['motion', x, y, dx, dy])
            if self.drawing and inside(x, y, self.screen):
                if len(self.lines) > 0:
                    self.lines.append( (self.lines[-1][1], (x, y)) )
                elif len(self.points) > 0:
                    self.lines.append( (self.points[-1], (x, y)) )

        # Resize our world based on the size of the window, in many cases
        # it's not in your best interest to allow resizing.
        @self.window.event
        def on_resize(width, height):
            self.width = width
            self.height = height
            glViewport(0, 0, width, height)
            glMatrixMode(gl.GL_PROJECTION)
            glLoadIdentity()
            glOrtho(0, width, 0, height, -1, 1)
            glMatrixMode(gl.GL_MODELVIEW)
        
        # Event Handler for drawing the screen
        @self.window.event
        def on_draw():
            self.window.clear()

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            
            # the box
            glColor3f(1.0, 1.0, 1.0)
            bottom = self.height * 0.2
            left = self.width / 6.0
            self.screen = [bottom, left, bottom + self.width * 2 / 3, left + self.height * 0.7]
            #bottom = 100 
            #left = 100
            Scene.rect(bottom, left, self.width * 2 / 3, self.height * 0.7)

            # the "knobs"
            glColor3f(1.0, 1.0, 1.0)
            Scene.circle(50.0, 50.0, 40.0)
            Scene.circle(self.width - 50.0, 50.0, 40.0)
        
            # the text "Etch A Sketch"
            glColor3f(1.0, 1.0, 1.0)
            label = pyglet.text.Label(self.caption, font_name='Times New Roman', font_size=24, x=self.width//2, y = self.height - 30, anchor_x='center', anchor_y='center') 
            label.draw()
            
            # draw the lines
            glColor3f(1.0, 1.0, 1.0)
            glLineWidth(1.0)
            for p0, p1 in self.lines:#range(1, len(self.lines)):
                glBegin(GL_LINES)
                glVertex3f(p0[0], p0[1], 0)
                glVertex3f(p1[0], p1[1], 0)
                glEnd()

            # draw the points
            glColor3f(1.0, 1.0, 1.0)
            glPointSize(1.0)
            glBegin(GL_POINTS)
            for x, y in self.points:
                glVertex3f(x, y, 0.0)
            glEnd()

    # draw the drawing grid area
    @staticmethod
    def rect(x, y, width, height):
        glBegin(GL_LINE_LOOP)
        
        glVertex3f(x        , y         , 0.0)
        glVertex3f(x + width, y         , 0.0)
        glVertex3f(x + width, y + height, 0.0)
        glVertex3f(x        , y + height, 0.0)
        glVertex3f(x        , y         , 0.0)

        glEnd()
    

    # draw a filled in circle at X,Y with radius R
    @staticmethod
    def circle(X, Y, R):
        glBegin(GL_TRIANGLE_FAN)

        # center vertex

        # go for number of vertices
        theta = 0.0
        dTheta = math.pi * 2.0 / 50.0
        while theta < math.pi * 2.0:
            x, y = R * math.cos(theta) + X, R * math.sin(theta) + Y
            # place vertices on the edge
            glVertex3f(x, y, 0.0)
            theta += dTheta

        glEnd()

    # gracefully exit the program and save points and lines if needed
    def quit(self):
        if self.save != None:
            data = {'points': self.points, 'lines': self.lines}
            with open(self.save, 'w') as fd:
                fd.write(json.dumps(data))
        sys.exit(0)
    
    # load points from a file
    def loadPointsAndLines(self, file):
        if file != None:
            with open(file, 'r') as fd:
                obj = json.load(fd)
                self.points = obj['points']
                self.lines = obj['lines']
        else:
            self.points = []
            self.lines = []

# Run the following code if this script was run directly from the command line
if __name__ == '__main__':
    saveFN = None
    loadFN = None

    for i in range(len(sys.argv)):
        if '-s' == sys.argv[i]:
            saveFN = sys.argv[i+1]
        elif '-l' == sys.argv[i]:
            loadFN = sys.argv[i+1]
    

    myGame = Scene(600, 500, "Etch a Sketch", True, saveFN=saveFN, loadFN=loadFN)
    debugging = pyglet.window.event.WindowEventLogger()
    myGame.window.push_handlers(debugging)
    pyglet.app.run()

