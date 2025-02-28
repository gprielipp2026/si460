#!/usr/bin/python3

# Important Libraries
import pyglet
from pyglet.gl import *
import glob
import re
import inspect
import random

from physics import *

# this loads and handles Movable Sprites on the Screen
class Entity:
    def __init__(self, type, imageLocation, speed, scale, loop, x, y, width, height, sounds={}):
        if imageLocation[-1] == '/':
            imageLocation = imageLocation[:-1] # remove the /

        self.sounds = sounds

        # define the possible states for the Entity 
        # locate these from the given directory
        animationTypes = set() 
        files = glob.glob(f'{imageLocation}/*.png')
        self.name = imageLocation[ imageLocation.rfind('/')+1 : ].capitalize()
        minMaxes = dict() 

        for file in files:
            # naming convention is 'Action (#).png'
            matches = re.search(r'([a-zA-Z\-]+)\ (\(\d+\))\.png', file)
            
            # could happen if some weird file is in the directory
            if matches is None:
                continue
            
            # pull out the Action and number (#)
            animation = matches.group(1)
            seq = int(matches.group(2)[1:-1])
            
            # check if the Action is in the type of animations yet
            if animation not in animationTypes:
                animationTypes.add(animation)
                minMaxes[animation] = (seq, seq)
            else:
                pmin, pmax = minMaxes[animation]
                minMaxes[animation] = (min(pmin, seq), max(pmax, seq))
        
        # all of the available "Action"'s that can be taken
        self.availableStates = list(animationTypes)

        self.collided = False

        # load the sequences
        self.imageSequences = {}
        load = lambda fn,flip_x: pyglet.resource.image(fn, flip_x=flip_x)
        # Retrieve the appropriate sequence of images from the sprite dictionary
        for animation in animationTypes:
            start, end = minMaxes[animation]
            end += 1
            self.imageSequences[animation] = {\
                'Left':[load(f'{imageLocation}/{animation} ({i}).png', True) for i in range(start, end)],\
                'Right':[load(f'{imageLocation}/{animation} ({i}).png', False) for i in range(start, end)]\
            }

        # Some basic settings
        self.animationSpeed = speed
        self.animationScale = scale
        self.animationLoop = loop
        self.x = x
        self.y = y
        self.body = RigidBody(self.x - width/2, self.y, width, height, type)

        self.state = list(animationTypes)[0]
        self.direction = 'Right'

        self.hp = 100
        self.levelOver = False

    # interact with the engine here somehow (rigid bodies?)
    def isInAir(self):
        return self.collided

    def update(self, dt):
        self.body.update(dt)
        self.x = (self.body.left()+self.body.right())/2
        self.y = self.body.bottom()
        self.animation = self.__getSprite()

    def isColliding(self, other):
        if type(other) is not RigidBody:
            return self.body.isColliding(other.body)
        else:
            return self.body.isColliding(other)

    def checkCollisions(self, objects):
        # objects is a [Entity...]
        self.collided = False
        for object in objects:
            if object is self:
                continue

            collision = object.isColliding(self.body)
            if collision[0]:
                self.collided = True    
                # I was trying really hard to avoid having hard coded values like these to make the game more expandable
                if self.body.getType() == 'player' and collision[1] == 'enemy':
                    self.log(f'player hit by {object}')
                    self.hp -= 20 # again, hard coding - not my favorite #TODO - refactor this code
                elif self.body.getType() == 'enemy' and collision[1] == 'weapon':
                    self.hp -= 50 
                elif collision[1] == 'tile':
                    self.body.velocity = Vector(0,0)

    def checkTileCollisions(self, tiles):
        for tile in tiles:
            for bodies in tile.rows:
                self.checkCollisions(bodies)


    # convert the given state and direction into a Sprite for display
    def __getSprite(self):
        # get the sequence
        sequence = self.imageSequences[self.state][self.direction]
        # Build the pyglet animation sequence
        playerAnimation = pyglet.image.Animation.from_image_sequence(sequence, self.animationSpeed, self.animationLoop)
        # center the sprite's anchor
        correctionX = (1 if self.direction == 'Left' else -1) * sequence[0].width * self.animationScale / 2.0
        # Create the sprite from the animation sequence
        sprite = pyglet.sprite.Sprite(playerAnimation, x=self.x + correctionX, y=self.y)
        # Set the player's scale
        sprite.scale = self.animationScale
        return sprite
    
    def isDead(self):
        return self.hp <= 0
    
    def hasWon(self):
        return self.levelOver

    # change the internal movement states
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def info(self, *args):
        func = inspect.stack()[1].function
        print(f'[{self.name}] {func}{str(tuple(args))}')
    
    def log(self, string):
        print(f'[{self.name}] {string}')

    def updateState(self, newState):
        self.state = newState
        self.animation = self.__getSprite()

    def updateDir(self, Dir):
        self.direction = Dir
        self.animation = self.__getSprite()

    def draw(self, t=0, *other):
        # display the animation of the current state 
        self.animation.draw()

        # draw the body for debugging
        glColor3f(0,1,0)
        glBegin(GL_LINE_LOOP)
        body = self.body
        # do the four sides of a box
        glVertex3f(body.left(), body.top(), 0.0)
        glVertex3f(body.right(), body.top(), 0.0)
        glVertex3f(body.right(), body.bottom(), 0.0)
        glVertex3f(body.left(), body.bottom(), 0.0)

        glEnd()
        glColor3f(1,1,1)

        # check to see what sound to play
        # right now it allows a user to hold down a button and it will spam the sound
        # TODO - fix this issue and only allow a sound to play once per animation sequence
        if self.state.lower() in self.sounds:
            random.choice(self.sounds[self.state.lower()]).play()
        elif self.isDead():
            self.sounds['lose'][0].play()
        elif self.hasWon():
            self.sounds['win'][0].play()
