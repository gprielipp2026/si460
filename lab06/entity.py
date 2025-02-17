#!/usr/bin/python3

# Important Libraries
import pyglet
import glob
import re

# Our Hero Class
class Entity:
    def __init__(self, imageLocation, speed, scale, loop, x, y):
        if imageLocation[-1] == '/':
            imageLocation = imageLocation[:-1] # remove the /

        # define the possible states for the Entity 
        # locate these from the given directory
        animationTypes = set() 
        files = glob.glob(f'{imageLocation}/*.png')
        minMaxes = dict() 
        for file in files:
            # naming convention is 'Action (#).png'
            matches = re.search(r'([a-zA-Z]+)\ (\(\d+\))\.png', file)
            
            # could happen if some weird file is in the directory
            if matches is None:
                continue

            animation = matches.group(1)
            seq = int(matches.group(2)[1:-1])
            # check if the Action is in the type of animations yet
            if animation not in animationTypes:
                animationTypes.add(animation)
                minMaxes[animation] = (seq, seq)
            else:
                pmin, pmax = minMaxes[animation]
                minMaxes[animation] = (min(pmin, seq), max(pmax, seq))
        
        self.availableStates = list(animationTypes)

        # load the sequences
        self.animations = {}
        load = lambda fn,flip_x: pyglet.resource.image(fn, flip_x=flip_x)
        # Retrieve the appropriate sequence of images from the sprite dictionary
        for animation in animationTypes:
            start, end = minMaxes[animation]
            end += 1
            self.animations[animation] = {\
                'Left':[load(f'{imageLocation}/{animation} ({i}).png', True) for i in range(start, end)],\
                'Right':[load(f'{imageLocation}/{animation} ({i}).png', False) for i in range(start, end)]\
            }
        
        # Some basic settings
        self.animationSpeed = speed
        self.animationScale = scale
        self.animationLoop = loop
        self.animationX = x
        self.animationY = y

        self.state = list(animationTypes)[0]
        self.direction = 'Right'
        # convert all of the animation sequences into a sprite
        for animation, val in self.animations.items():
            self.animations[animation] = {}
            for direction, sequence in val.items():
                # Build the pyglet animation sequence
                playerAnimation = pyglet.image.Animation.from_image_sequence(sequence, self.animationSpeed, self.animationLoop)
                # center the sprite's anchor
                correctionX = (1 if direction == 'Left' else -1) * sequence[0].width * self.animationScale / 2.0
                # Create the sprite from the animation sequence
                sprite = pyglet.sprite.Sprite(playerAnimation, x=self.animationX+correctionX, y=self.animationY)
                # Set the player's scale
                sprite.scale = self.animationScale
                # save the sprite
                self.animations[animation][direction] = sprite

    def draw(self, t=0, *other):
        # display the animation of the current state 
        self.animations[self.state][self.direction].draw()

