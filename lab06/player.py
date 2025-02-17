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
       
        self.stateID = self.availableStates.index('Idle') 
        self.state = self.availableStates[self.stateID]

    def on_key_press(self, symbol, modifiers):
        self.info(symbol, modifiers)

        if modifiers == key.MOD_SHIFT:
            if symbol == key.PLUS:
                self.stateID += 1
                self.state = self.availableStates[self.stateID % len(self.availableStates)]
        elif modifiers == 0:
            if symbol == key.A:
                self.direction = 'Left'
            elif symbol == key.D:
                self.direction = 'Right'
            elif symbol == key.W:
                self.stateID += 1
                self.state = self.availableStates[self.stateID % len(self.availableStates)]
            elif symbol == key.S:
                self.stateID -= 1
                self.state = self.availableStates[self.stateID % len(self.availableStates)]
            elif symbol == key.MINUS:
                self.stateID -= 1
                self.state = self.availableStates[self.stateID % len(self.availableStates)]
        
        self.log(f'{self.state} facing {self.direction}')

objects = [Player()]
