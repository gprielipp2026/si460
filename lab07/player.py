#!/usr/bin/python3

# Important Libraries
import pyglet
from pyglet.window import key

from entity import Entity

# Our Hero Class
class Player(Entity):
    def __init__(self, speed=0.05, scale=0.15, loop=True, x=380, y=250):
        # define the possible states for the Player
        super().__init__('mylevel/sprites/hero', speed, scale, loop, x, y)
       
        self.updateState('Idle')
        
        self.direction = 'Right'
        self.actions = []

        self.keyMappings = {\
                key.RIGHT: 'right',\
                key.LEFT: 'left',\
                key.SPACE: 'jump',\
                key.LSHIFT: 'run',\
                key.LCTRL: 'shoot',\
                key.LALT: 'attack',\
                key.UP: 'up',\
                key.DOWN: 'down'\
                }

    def on_key_press(self, symbol, modifiers):
        self.info(symbol, modifiers)
       
        if symbol in self.keyMappings:
            self.actions.append(self.keyMappings[symbol])
            self.log(self.actions)

        self.interpretActions()
         
    def on_key_release(self, symbol, modifiers):
        self.info(symbol, modifiers)

        if symbol in self.keyMappings:
            self.actions.remove(self.keyMappings[symbol])
            self.log(self.actions)

        self.interpretActions()

    # interact with a physics engine here
    def isInAir(self):
        return False

    def isDead(self):
        return False

    def interpretActions(self):
        state, direction = None, None

        if 'right' in self.actions:
            direction = 'Right'
            state = 'Run' if not self.isInAir() else 'Glide'
        elif 'left' in self.actions:
            direction = 'Left'
            state = 'Run' if not self.isInAir() else 'Glide'

        if len(self.actions) == 0:
            state = 'Idle'
        elif 'jump' in self.actions:
            if 'shoot' in self.actions:
                state = 'Jump-Throw'
            elif 'attack' in self.actions:
                state = 'Jump-Attack'
            else:
                state = 'Jump'
        elif 'run' in self.actions:
            state = 'Run'
            if 'down' in self.actions:
                state = 'Slide'
        elif 'shoot' in self.actions:
            if 'up' in self.actions:
                # aim upwards somehow
                pass
            elif 'down' in self.actions:
                # aim downwards
                pass
            state = 'Throw'
        elif 'up' in self.actions:
            state = 'Climb'
        elif 'down' in self.actions:
            state = 'Climb'
        elif 'attack' in self.actions:
            state = 'Attack'
        
        if self.isDead():
            state = 'Dead'
        
        if state is not None:
            self.updateState(state)
        if direction is not None:
            self.updateDir(direction)

        self.log(f'{self.state} facing {self.direction}')

objects = [Player()]
