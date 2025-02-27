#!/usr/bin/python3 -B

# Important Libraries
import pyglet
from pyglet.window import key
import time, sys, importlib, os, glob, re

from player import Player
from enemy import Enemy
from landmass import Landmass

# Our world that we will draw via pyglet
class Game(pyglet.window.Window):

    # Update the world time based on time elapsed in the real world
    # since we started the Game Class.
    def updateClock(self, dt):
        self.worldTime = time.time() - self.startTime
        # A temporary background mover as a demo...
        #print(self.background_x + self.background.width, self.width)
        # I want this to loop appropriately
        if self.background.width + self.background_x <= 0.0:
            self.background_x += self.background.width

        self.background_x -= 1.0
       #self.background_x -= 0.2
        
    # Initialize and run our environment
    def __init__(self, width=800, height=600, caption="Would you like to play a game?", entities: list=[], tiles=[], resizable=False):
        # background music
        self.backgroundMusic = pyglet.media.Player()
        self.backgroundMusic.queue(pyglet.media.load('mylevel/music/1.wav', streaming=True))
        self.backgroundMusic.eos_action = 'loop'
        self.backgroundMusic.loop = True
        self.backgroundMusic.play()

        # Count screenshots
        self.screenshot = 0

        # Build the OpenGL / Pyglet Window
        super().__init__(width=width, height=height, resizable=resizable, caption=caption)

        self.width = width
        self.height = height
        self.entities = entities
        self.tiles = tiles

        # Fix transparent issue...
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

        # Lets set a global clock
        self.worldTime = 0.0
        self.startTime = time.time()

        # Create the Background, this is one method of creating images,
        # we will work with multiple methods.
        # Take a look at how this is drawn in the on_draw function
        # and the self.background.blit method.
        # eventually background could be passed in
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

        for entity in self.entities:
            if 'on_key_press' in dir(entity):
                entity.on_key_press(symbol, modifiers)

        if symbol == key.END:
            self.screenshot = self.screenshot + 1
            pyglet.image.get_buffer_manager().get_color_buffer().save(sys.argv[-1]+'.'+str(self.screenshot)+'.png')

    def on_key_release(self, symbol, modifiers):
        for entity in self.entities:
            if 'on_key_release' in dir(entity):
                entity.on_key_release(symbol, modifiers)

    # Event Handler for drawing the screen
    #@window.event
    def on_draw(self):

        # Clear the window (a good way to start things)
        self.clear()

        # Draw the game background
        self.background.blit(self.background_x,self.background_y,height=self.height)
        count = 0
        while self.background_x + self.background.width + count * self.background.width <= self.width:
            x = self.background_x + self.background.width + count * self.background.width - 0.1 # small factor to remove gap
            self.background.blit(x, self.background_y, height=self.height)
            count += 1

        for tile in self.tiles:
            tile.draw()

        # Lets draw all of the individual objects, these objects
        # need to have a draw function that takes in worldTime as
        # a variable.
        for entity in self.entities:
            entity.draw(self.worldTime)

def loadAllImages(filepath='mylevel/sprites'):
    dirs = os.listdir(filepath)
    images = {}
    load = lambda loc,flip_x: pyglet.resource.image(loc, flip_x=flip_x)
    for name in dirs:
        images[name] = dict() 
        minMaxes = dict()
        for file in glob.glob(f'{filepath}/{name}/*.png'):
            matches = re.search(r'([a-zA-Z]+)\ (\(\d+\))\.png', file)
            if matches is None:
                continue

            animation = matches.group(1)
            seq = int(matches.group(2)[1:-1])
            if animation not in minMaxes:
                minMaxes[animation] = (seq, seq)
            else:
                pmin, pmax = minMaxes[animation]
                minMaxes[animation] = (min(pmin, seq), max(pmax, seq))
        for animation, startEnd in minMaxes.items():
            start,end = startEnd
            end += 1
            images[name][animation] = {\
                'Left': [load(f'{filepath}/{name}/{animation} ({i}).png', True) for i in range(start, end)],\
                'Right': [load(f'{filepath}/{name}/{animation} ({i}).png', False) for i in range(start, end)],\
            }
    return images

# Load in any requested objects from the command then, then start the game.
if __name__ == '__main__':
    #print(loadAllImages('mylevel/sprites') | loadAllImages('mylevel/objects') | loadAllImages('mylevel/tiles'))
    
    entities = [Player(), Enemy(), Enemy()]
    tiles = [Landmass([[1,1,0,0,0,0,0,0],[1,1,1,1,1,1,0,0],[1,1,1,1,1,1,0,0]], 0, 216)]

    myGame = Game(800, 600, "SI460 Game", entities, tiles)
    pyglet.app.run()
