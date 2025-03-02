#!/usr/bin/python3 -B

# Important Libraries
import pyglet
import time, sys, importlib

# Our world that we will draw via pyglet
class Game:

    # Update the world time based on time elapsed in the real world
    # since we started the Game Class.
    def updateClock(self, dt):
        self.worldTime = time.time() - self.startTime

    # Initialize and run our environment
    def __init__(self, width=800, height=600, caption="Would you like to play a game?", level=None, resizable=True):

        # Store the dimensions of the world
        self.width  = width
        self.height = height

        # Lets track what keys are being pressed
        self.keyTracking   = {}
        self.mouseTracking = []

        # Count screenshots
        self.screenshot = 0

        # Build the OpenGL / Pyglet Window
        self.window = pyglet.window.Window(width=self.width, height=self.height, resizable=resizable, caption=caption)

        # Fix transparent issue...
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

        # Store the current level of the game
        self.level = level

        # Lets set a global clock
        self.worldTime = 0.0
        self.startTime = time.time()

        # Schedule a Clock to update the time
        pyglet.clock.schedule_interval(self.updateClock, 1.0/60.0)

        # Handle Key Presses in our World
        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol == pyglet.window.key.END:
                self.screenshot = self.screenshot + 1
                pyglet.image.get_buffer_manager().get_color_buffer().save(sys.argv[-1]+'.'+str(self.screenshot)+'.png')
            self.keyTracking[symbol] = modifiers

        # Handle Key Releases in our World
        @self.window.event
        def on_key_release(symbol, modifiers):
            if symbol in self.keyTracking:
                del(self.keyTracking[symbol])

        # Allow for resizing the game window
        @self.window.event
        def on_resize(width, height):
            self.width = width
            self.height = height

        # Event Handler for drawing the screen
        @self.window.event
        def on_draw():

            # Clear the window (a good way to start things)
            self.window.clear()

            # Lets draw all of the individual objects, these objects
            # need to have a draw function that takes in worldTime as
            # a variable.
            if self.level is not None:
                self.level.draw(self.worldTime, self.width, self.height, self.keyTracking, self.mouseTracking)

# Load in any requested objects from the command then, then start the game.
if __name__ == '__main__':

    # Retrieve the levelname from the command line, default to mylevel
    levelName = sys.argv[-1]
    if len(sys.argv) < 2:
        levelName = 'mylevel'
    if levelName[-1] == '/':
        levelName = levelName[:-1]

    # Update path for python libraries so we can import python files in the
    # level directory (such as player, enemies, etc.)
    sys.path.append("./"+levelName)

    print('Loading Level...')
    level =  getattr(importlib.import_module(levelName), 'level')

    print('Starting Game...')
    myGame = Game(800, 600, "SI460 Game", level)
    pyglet.app.run()
