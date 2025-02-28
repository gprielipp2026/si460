#!/usr/bin/python3

# Important Libraries
#import pyglet
#from pyglet.window import key
import random, glob, re
from entity import Entity

# an enemy
# chooses one at random
class Enemy(Entity):
    def __init__(self, speed=0.05, scale=0.15, loop=True, x=380, y=250):
        # define the possible states for the Player
        left, right = None, None

        files = glob.glob('mylevel/sprites/*')
        for file in files:
            matches = re.search(r'enemy-(\d+)', file)
            if matches is None:
                continue
            num = int(matches.group(1))
            if left is None:
                left, right = num, num
            left = min(num, left)
            right = max(num, right)

        ID = random.randint(left, right) 
        
        super().__init__('enemy', f'mylevel/sprites/enemy-{ID}', speed, scale, loop, x, y, 200*scale, 400*scale)
       
        self.stateID = self.availableStates.index('Idle') 
        self.updateState(self.availableStates[self.stateID])

    

