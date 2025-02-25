#!/usr/bin/python3

# Important Libraries
import pyglet
import glob
import re
import inspect

# this loads and handles Movable Sprites on the Screen
class Entity:
    def __init__(self, imageLocation, speed, scale, loop, x, y):
        if imageLocation[-1] == '/':
            imageLocation = imageLocation[:-1] # remove the /

        # define the possible states for the Entity 
        # locate these from the given directory
        animationTypes = set() 
        files = glob.glob(f'{imageLocation}/*.png')
        self.name = imageLocation[ imageLocation.rfind('/')+1 : ].capitalize()
        minMaxes = dict() 
        for file in files:
            # naming convention is 'Action (#).png'
            matches = re.search(r'([a-zA-Z]+)\ (\(\d+\))\.png', file)
            
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

        self.state = list(animationTypes)[0]
        self.direction = 'Right'

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
