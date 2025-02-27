#!/usr/bin/python3

# Important Libraries

from tile import Tile

# A floating island
class Island(Tile):
    def __init__(self, length=1, x=200, y=140):
        # define the possible states for the Player
        base = 'mylevel/tiles'
        sequence = ['hl'] + ['hm']*length + ['hr']
        files = [f'{base}/{item}.png' for item in sequence]
        # I wan't one row 
        super().__init__([files], x, y)

