#!/usr/bin/python3 -B

# SI460 - Game Level Configuration file - A default level configuration
#         file for the SI460 Graphics Course.  This file defines the layout
#         of the game, where the players and enemies exists and where the goal
#         is located.  Typically reaching the goal advances the user to
#         the next level.

# We are assuming a 800x600 world, which is allowed to go beyond that in
# both the x and y, and is divided up into 50x50 chunks in a grid-like
# fashion.

# Lets define the size of our grid in terms of width and height for
# EACH cell in the grid.
height = 50
width  = 50

# Define the board
levelDefinition = '''
11
10                                     hl hr
09
08
07                   hl hm hm hm hm hm hm hm hr
06
05          hl hr
04
03 um ur
02 mm mr
01 mm cr wl um um um um um um um um ur
00 mm mm mm mm mm mm mm mm mm mm mm mr
00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16
'''

# Define the objects
goalDefinition = '''
11                                        sm
10
09
08
07
06
05
04
03
02
01
00
00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16
'''

# Define the enemies
enemyDefinition = '''
11
10
09
08                               e1
07
06
05
04
03
02             e2
01
00
00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16
'''

# Define where the player will start on the board
playerStartRow = 2
playerStartCol = 9

# Define the scaling for the player, and speed of the shifts between
# the various sprites that make up the players.
playerSpriteSpeed = 0.05
playerSpriteScale = 0.15

# Retrieve the level name from the directory name, don't change this...
import os
levelName = os.path.realpath(__file__).split('/')[-2]

# Define where the background image is
background = levelName + "/backgrounds/level1.png"

# Define what music to play
background_music = levelName + '/music/1.wav'

# Sound Effects, when a player changes it state to one of the
# following modes, play the following sounds.
sounds = {'hero':{'Jump':        levelName + '/music/jump.wav',
                  'Attack':      levelName + '/music/attack.wav',
                  'Jump-Attack': levelName + '/music/jump.wav',
                  'Jump-Throw':  levelName + '/music/throw.wav',
                  'Throw':       levelName + '/music/throw.wav',
                  'Dead':        levelName + '/music/hero_death.wav'  },
          'enemy-1': {'Dead':    levelName + '/music/enemy_death.wav' },
          'enemy-2': {'Dead':    levelName + '/music/enemy_death.wav' } }

# When our hero wins the game, play the following music
heroSoundWin = levelName + '/music/win.wav'

# Where are the sprites, tiles, and goals located?
tilepath     = levelName + '/tiles'
goalpath     = levelName + '/objects'
spritespath  = levelName + "/sprites"

# Define the Keyboard mappings
from pyglet.window import key
keyMappings = {key.LSHIFT: 'run',    key.RSHIFT: 'run',
               key.LALT:   'attack', key.RALT:   'attack',
               key.LCTRL:  'shoot',  key.RCTRL:  'shoot',
               key.SPACE:  'jump',
               key.RIGHT:  'right',
               key.LEFT:   'left',
               key.UP:     'up',
               key.DOWN:   'down'}

# Determine some very useful information needed in our game.
from layout import positionEnemies, board2grid
enemies = positionEnemies(enemyDefinition)
level, rows, cols = board2grid(levelDefinition, tilepath, returnSize=True)
goals = board2grid(goalDefinition, goalpath)
