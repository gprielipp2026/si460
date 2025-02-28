#!/usr/bin/python3

# Important Libraries
import pyglet
from pyglet.window import key
import random

from entity import Entity

# Our Hero Class
class Player(Entity):
    def __init__(self, speed=0.05, scale=0.15, loop=True, x=380, y=250):
        load = lambda x: pyglet.media.load(f'mylevel/music/{x}.wav', streaming=False)

        sounds = {
            'attack': [load('attack')],
            'jump': [load('jump'), load('jump2')],
            'shoot': [load('throw')],
            'lose': [load('hero_death')],
            'win': [load('win')],
        }
        
        # define the possible states for the Player
        super().__init__('player', 'mylevel/sprites/hero', speed, scale, loop, x, y, 200*scale, 400*scale, sounds=sounds)
       
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

        if symbol in self.keyMappings and len(self.actions) > 0:
            if self.keyMappings[symbol] in self.actions:
                self.actions.remove(self.keyMappings[symbol])
            self.log(self.actions)

        self.interpretActions()

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
        
        # update the direction and state
        if state is not None:
            self.updateState(state)
        if direction is not None:
            self.updateDir(direction)

        self.log(f'{self.state} facing {self.direction}')
