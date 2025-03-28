#!/usr/bin/python3 -B

# Important Libraries
import pyglet
from pyglet.window import mouse, key, Window
from pyglet.gl import *
import time, sys, numpy, importlib
from particle import ParticleArray

# Our world that we will draw via pyglet
class Scene(Window):

    # Update the world time based on time elapsed in the real world
    # since we started the Scene Class.
    def updateClock(self, dt):
        self.worldTime = time.time() - self.startTime
        self.dt = dt

    # Initialize and run our environment
    def __init__(self, saveFile, width=800, height=600, caption="Would you like to play a game?", resizable=False):
        # Build the OpenGL / Pyglet Window
        super().__init__(width=width, height=height, resizable=resizable, caption=caption)
        
        # where to save the screenshots
        self.saveFile = saveFile

        # Define current world rotations (arcball)
        self.width = width
        self.height = height
        self.P1 = numpy.array([0,0,0])
        self.P2 = numpy.array([0,0,0])
        self.theta = 0.0
        self.u = numpy.array([0,0,0])
        self.wr = []
        self.particles = ParticleArray()

        # Lets allow some zooming, used in conjunction with the
        # portion of code in draw that scales the world into a 100x100 area
        self.zoom = 1.0

        # Fix transparent issue...
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Lets set a global clock
        self.worldTime = 0.0
        self.dt = 0.0
        self.startTime = time.time()

        # Schedule a Clock to update the time
        pyglet.clock.schedule_interval(self.updateClock, 1.0/120.0)

    # Handle Mouse Press (arcball)
    def on_mouse_press(self, x, y, button, modifiers):
        z = self.zxy(x,y,self.width, self.height)
        x = -1.0 * (self.width/2.0 - x)
        y = y - self.height/2.0
        self.wr.append([0.0, numpy.array([0,0,0])])
        self.P1 = numpy.array([x,y,z])

    # Handle Mouse Drag (arcball)
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        z = self.zxy(x,y,self.width, self.height)
        x = -1.0 * (self.width/2.0 - x)
        y = y - self.height/2.0
        self.P2 = numpy.array([x,y,z])
        theta, u = self.vector_angle(self.P1, self.P2)
        self.wr[-1] = [theta, u]

    # Allow for basic zooming in our 100x100 world.
    def on_key_press(self, symbol, modifiers):
        if symbol == key.PAGEUP:
            self.zoom = self.zoom + 0.2
            self.zoom = max(0.1, self.zoom)
        elif symbol == key.PAGEDOWN:
            self.zoom = self.zoom - 0.2
            self.zoom = max(0.1, self.zoom)
        elif symbol == key.END:
            print('saving image:',self.saveFile)
            pyglet.image.get_buffer_manager().get_color_buffer().save(self.saveFile)

    # Event Handler for drawing the screen
    def on_draw(self, dt=0):
        # Clear the window (a good way to start things)
        self.clear()

        # Set the ViewPort and Frustum
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-5.0, 5.0, -5.0, 5.0, 5.0, 10000.0)
        glMatrixMode(GL_MODELVIEW)

        # Setup the environment to handle depth
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # Set the Modelview matrix to the identity matrix
        glLoadIdentity()

        # Translate the world to give us more space, the more
        # we push things back the smaller they start out as...
        glTranslatef(0.0,0.0,-450.0)

        # Rotate the world based on the arcball algorithm
        for r in self.wr:
            glRotatef(numpy.degrees(r[0]), r[1][0], r[1][1], r[1][2])

        # Basic World Scaling, easier than the version needed for
        # the world based on M
        glScalef(self.zoom, self.zoom, self.zoom)

        # Lets draw all of the individual objects.
        self.particles.draw(self.dt)

    # Determine the z value based on x,y (mouse) w,h (screen) for arcball
    def zxy(self,x,y,w,h):
      if ((x - (w/2.0))**2 + (y - (h/2.0))**2) < ((h/2.0)**2):
          return numpy.sqrt((h/2.0)**2 - (x - (w/2.0))**2 - (y - (h/2.0))**2)
      return 0.01

    # Determine the appropriate vectors and angles for the arcball algorithm
    def vector_angle(self, p1, p2):
      theta = numpy.arccos((p1.dot(p2))/(numpy.linalg.norm(p2) * numpy.linalg.norm(p1)))
      u = (numpy.cross(p1, p2) / (numpy.linalg.norm(p2) * numpy.linalg.norm(p1)))
      return theta, u

# Run the following code if this script was run directly from the command line
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'usage: {sys.argv[0]} <screenshot filename>')
        sys.exit()
    myGame = Scene(sys.argv[1], 600, 600, "Particle Simulation")
    pyglet.app.run()
