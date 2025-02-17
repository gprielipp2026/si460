#!/usr/bin/python3 -B

# Important Libraries
import pyglet
from pyglet.window import key
import time, sys, importlib

from enemy import Enemy

# Our world that we will draw via pyglet
class Game(pyglet.window.Window):

    # Update the world time based on time elapsed in the real world
    # since we started the Game Class.
    def updateClock(self, dt):
        self.worldTime = time.time() - self.startTime
        # A temporary background mover as a demo...
        self.background_x -= 0.2

    # Initialize and run our environment
    def __init__(self, width=800, height=600, caption="Would you like to play a game?", players=[], resizable=False):

        # Count screenshots
        self.screenshot = 0

        # Build the OpenGL / Pyglet Window
        super().__init__(width=width, height=height, resizable=resizable, caption=caption)

        self.width = width
        self.height = height
        self.players = players

        # Fix transparent issue...
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

        # Array of players that I would like to draw over time
        # make sure they have: .draw(timeT) function
        self.players = players

        # Lets set a global clock
        self.worldTime = 0.0
        self.startTime = time.time()

        # Create the Background, this is one method of creating images,
        # we will work with multiple methods.
        # Take a look at how this is drawn in the on_draw function
        # and the self.background.blit method.
        self.background = pyglet.resource.image("mylevel/backgrounds/level1.png")
        self.background_x = 0
        self.background_y = 0

        # Schedule a Clock to update the time
        pyglet.clock.schedule_interval(self.updateClock, 1.0/30.0)

    # Handle Key Presses in our World
    #@window.event
    def on_key_press(self, symbol, modifiers):
        if modifiers == key.MOD_CTRL and symbol == key.C:
            print('[Game] exiting...')
            sys.exit(0)

        for player in self.players:
            if 'on_key_press' in dir(player):
                player.on_key_press(symbol, modifiers)

        if symbol == key.END:
            self.screenshot = self.screenshot + 1
            pyglet.image.get_buffer_manager().get_color_buffer().save(sys.argv[-1]+'.'+str(self.screenshot)+'.png')

    # Event Handler for drawing the screen
    #@window.event
    def on_draw(self):

        # Clear the window (a good way to start things)
        self.clear()

        # Draw the game background
        self.background.blit(self.background_x,self.background_y,height=self.height)

        # Lets draw all of the individual objects, these objects
        # need to have a draw function that takes in worldTime as
        # a variable.
        for player in self.players:
            player.draw(self.worldTime)

# Load in any requested objects from the command then, then start the game.
if __name__ == '__main__':
    worldPlayers = []
    for objectFile in sys.argv[1:]:
        print('Loading', objectFile)
        if objectFile.find('.py') != -1:
            objectFile = objectFile.split('.py')[0]
        objects = getattr(importlib.import_module(objectFile), 'objects')
        if len(objects) > 0:
            print(' Adding', len(objects), 'to worldObjects')
            for i in range(len(objects)):
                worldPlayers.append(objects[i])
   
    worldPlayers.extend([Enemy(), Enemy()])

    myGame = Game(800, 600, "SI460 Game", worldPlayers)
    pyglet.app.run()
