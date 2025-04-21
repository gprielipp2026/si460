#!/usr/bin/python3

# Important Libraries
import pyglet

# Our own Game Libraries
import sprites, config

# SI460 Level Definition
class Level:
    def __init__(self, sprites, hero, enemies=[]):

        # Create the Background, this is one method of creating images,
        # we will work with multiple methods.
        # Take a look at how this is drawn in the on_draw function
        # and the self.background.blit method.
        self.background   = pyglet.resource.image(config.background)
        self.background_x = 0
        self.background_y = 0

        # Store the loaded sprites and hero
        self.sprites = sprites
        self.hero    = hero
        self.weapons = []
        self.hero.set_level(config.level, config.height, config.width)
        self.hero.set_weapon_factory(self.weapon_spawner)
        
        self.enemies = enemies
        for enemy in self.enemies:
            enemy.set_level(config.level, config.height, config.width)

        # Music in the Background
        self.backgroundMusic = pyglet.media.Player()
        self.backgroundMusic.queue(pyglet.media.load('mylevel/music/background-music.wav', streaming=True))
        self.backgroundMusic.eos_action = 'loop'
        self.backgroundMusic.loop = True
        self.backgroundMusic.play()

    # Here is a complete drawBoard function which will draw the terrain.
    # Lab Part 1 - Draw the board here
    def drawBoard(self, level, delta_x=0, delta_y=0, height=50, width=50):
        # level = dict(str:dict(str:str)), level[row][col] = filename
        for row, val in level.items():
            for col, img in val.items():
                x = int(col) * width  + delta_x
                y = int(row) * height + delta_y
                img.blit(x,y,width=width, height=height)

    def draw(self, t=0, width=800, height=600, keyTracking={}, mouseTracking=[], *other):

        # Draw the game background
        if self.background.width < width:
            self.background.blit(self.background_x,self.background_y,height=height,width=width)
        else:
            self.background.blit(self.background_x,self.background_y,height=height)

        # Draw the gameboard
        self.drawBoard(config.level, 0, 0, config.height, config.width)

        # Draw the weapons
        for weapon in self.weapons:
            weapon.draw()

        # Draw the enemies
        for enemy in self.enemies:
            enemy.collide(self.weapons)
            enemy.draw(t)

        # Draw the hero.
        self.hero.collide(self.enemies)
        self.hero.draw(t, keyTracking)

    def weapon_spawner(self, direction, x, y):
        global gameSprites
        print(f'Spawned weapon facing {direction} at ({x},{y})')

        weapon = Player(gameSprites,
                        sprites.buildSprite,
                        'weapon', 'Kunai', direction,
                        config.playerSpriteSpeed,
                        config.playerSpriteScale,
                        False,
                        x,
                        y
                        )

        self.weapons.append(weapon)

# Load all game sprites
print('Loading Sprites...')
gameSprites = sprites.loadAllImages(config.spritespath)

# Load in the hero
print('Loading the Hero...')
from player import Player

load = lambda x: pyglet.media.load(f'mylevel/music/{x}.wav', streaming=False)
heroSounds = {
    'attack': [load('attack')],
    'jump': [load('jump'), load('jump2')],
    'throw': [load('throw')],
    'win': [load('win')],
    'lose': [load('hero_death')]
}

hero = Player(gameSprites,
              sprites.buildSprite,
              "hero", "Idle", "Right",
              config.playerSpriteSpeed,
              config.playerSpriteScale,
              True,
              config.playerStartCol * config.width,
              config.playerStartRow * config.height,
              sounds=heroSounds)

# Load in the Enemies
print('Loading the Enemies...')

enemySounds = {
    'attack': [load('attack')],
    'lose': [load('enemy_death')],
}
enemyConfigs = ()

enemies = [Player(gameSprites,
              sprites.buildSprite,
              f"enemy-{e[1]}", "Run", "Right",
              config.playerSpriteSpeed,
              config.playerSpriteScale,
              True,
              x * config.width,
              y * config.height, 
              sounds=enemySounds) for x,y,e in config.enemies]

# provide the level to the game engine
print('Starting level:', config.levelName)
level = Level(gameSprites, hero, enemies)
