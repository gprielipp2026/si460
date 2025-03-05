#!/usr/bin/python3

# Important Libraries
import pyglet, config, random
from pyglet.window import key

# Our Hero Class
class Player:
    def __init__(self, sprites={},
                       buildSprite=None,
                       playerClass="hero",
                       mode="Run",
                       facing="Right",
                       speed=0.05,
                       scale=0.15,
                       loop=True,
                       x=380,
                       y=250):

        # Store the sprites, and the sprite building function
        self.sprites      = sprites
        self.buildSprite  = buildSprite
        self.playerSprite = None

        # Some basic settings
        self.animationSpeed = speed
        self.animationScale = scale
        self.animationLoop  = loop
        self.animationX     = x
        self.animationY     = y
        self.playerClass    = playerClass
        self.mode           = mode
        self.facing         = facing

        # Build the starting character sprite
        self.changeSprite()

        # keep track of the time locally
        self.t = 0
        self.dt = 0

        # save the sounds
        load = lambda x: pyglet.media.load(f'mylevel/music/{x}.wav', streaming=False)
        self.sounds = {
            'attack': [load('attack')],
            'jump': [load('jump'), load('jump2')],
            'throw': [load('throw')],
            'win': [load('win')],
            'lose': [load('hero_death')]
        }

    # Build the initial character
    def changeSprite(self, mode=None, facing=None):
        if mode is not None:
            self.mode = mode
        if facing is not None:
            self.facing = facing
        if self.playerSprite is not None:
            self.animationX = self.playerSprite.x
            self.animationY = self.playerSprite.y
        self.playerSprite = self.buildSprite(self.sprites,
                                             self.playerClass,
                                             self.mode,
                                             self.facing,
                                             self.animationSpeed,
                                             self.animationScale,
                                             self.animationLoop,
                                             self.animationX,
                                             self.animationY)

    # figure out which animation should be showing
    def interpretAnimation(self, keyTracking={}):
        self.facing = 'Left' if key.LEFT in keyTracking else 'Right' if key.RIGHT in keyTracking else self.facing
        isJumping = key.SPACE in keyTracking
        isAttacking = key.LCTRL in keyTracking or key.RCTRL in keyTracking

    # Move the character
    def movement(self, t=0, keyTracking={}): 
        self.interpretAnimation(keyTracking)

        isMoving  = key.LEFT in keyTracking or key.RIGHT in keyTracking
        isJumping = key.SPACE in keyTracking 
        isRunning = (key.LSHIFT in keyTracking or key.RSHIFT in keyTracking) and isMoving
        direction = -1 if self.facing == 'Left' else 1 # multiplier

        lrconstant = 15 # the movement was a little too sluggish
        jumpconstant = 20 # too sluggish
        self.playerSprite.x += direction * (9 if isRunning else 3 if isMoving else 0) * self.dt * lrconstant
        self.playerSprite.y += (3 if isJumping else 0) * self.dt * jumpconstant

        mode = 'Idle'
        if isJumping:
            mode = 'Jump'
        elif isRunning or isMoving:
            mode = 'Run'

        self.changeSprite(mode=mode)
        
    # Draw our character
    def draw(self, t=0, keyTracking={}, *other):
        self.dt = t - self.t
        self.t = t

        self.movement(t, keyTracking)
        self.playerSprite.draw()
