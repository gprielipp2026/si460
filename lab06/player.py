#!/usr/bin/python3

# Important Libraries
import pyglet

# Our Hero Class
class Player:
    def __init__(self, speed=0.05, scale=0.15, loop=True, x=380, y=250):
        # Example sprite building...
        # --- What a horrible way of loading in images ---
        # --- There must be a better way ---
        # --- Possibly a good Lab problem, hmmm.... ---
        a = pyglet.resource.image('mylevel/sprites/hero/Run (1).png', flip_x=False)
        b = pyglet.resource.image('mylevel/sprites/hero/Run (2).png', flip_x=False)
        c = pyglet.resource.image('mylevel/sprites/hero/Run (3).png', flip_x=False)
        d = pyglet.resource.image('mylevel/sprites/hero/Run (4).png', flip_x=False)
        e = pyglet.resource.image('mylevel/sprites/hero/Run (5).png', flip_x=False)
        f = pyglet.resource.image('mylevel/sprites/hero/Run (6).png', flip_x=False)
        g = pyglet.resource.image('mylevel/sprites/hero/Run (7).png', flip_x=False)
        h = pyglet.resource.image('mylevel/sprites/hero/Run (8).png', flip_x=False)
        i = pyglet.resource.image('mylevel/sprites/hero/Run (9).png', flip_x=False)
        j = pyglet.resource.image('mylevel/sprites/hero/Run (10).png',flip_x=False)

        # We can change the anchor point of an image, by setting it's x and y
        # anchor values, example:
        # a.anchor_x = a.width / 2.0

        # Retrieve the appropriate sequence of images from the sprite dictionary
        self.playerSequence = [a,b,c,d,e,f,g,h,i,j]

        # Some basic settings
        self.animationSpeed = speed
        self.animationScale = scale
        self.animationLoop = loop
        self.animationX = x
        self.animationY = y

        # Build the pyglet animation sequence
        self.playerAnimation = pyglet.image.Animation.from_image_sequence(self.playerSequence,
                                                                          self.animationSpeed,
                                                                          self.animationLoop)
        # Create the sprite from the animation sequence
        self.playerSprite = pyglet.sprite.Sprite(self.playerAnimation,
                                                 x=self.animationX,
                                                 y=self.animationY)
        # Set the player's scale
        self.playerSprite.scale = self.animationScale

    def draw(self, t=0, *other):
        self.playerSprite.draw()

objects = [Player()]
