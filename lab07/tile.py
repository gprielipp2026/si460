#!/usr/bin/python3

# Important Libraries
import pyglet
from pyglet.gl import *

from physics import *

# a tile class that loads in the images and displays them
class Tile:
    def __init__(self, files, x, y):
        # what will actually display the images
        # is supposed to allow me to make rendering faster (less calls), but it wasn't working
        #self.batch = pyglet.graphics.Batch()

        load = lambda fn: pyglet.image.load(fn)
        
        # make the sprites
        makeSprite = lambda img, ix, iy: pyglet.sprite.Sprite(img=img, x=ix, y=iy)#, batch=self.batch)
        self.sprites = []

        # make the physics body
        # it is rather easy road to just store a rigid body for each image
        self.rows = []
        # this assumes that all of the images are the same width and height
        totalHeight = 0
        for row in files:
            # get the images
            images = [load(file) for file in row] 
            bodies = []
            totalWidth = 0
            for img in images:
                sprite = makeSprite(img, x + totalWidth, y - totalHeight) 
                bodies.append(RigidBody(x + totalWidth, y - totalHeight, img.width, img.height, 'tile'))
                totalWidth += img.width
                self.sprites.append(sprite)
            self.rows.append(bodies)
            # move the "cursor" to the next line
            totalHeight += images[0].height

    def draw(self, t=0, *other):
        #self.batch.draw() 
        for sprite in self.sprites:
            sprite.draw()

        for bodies in self.rows:
            for body in bodies:
                glColor3f(1,0,0)
                glBegin(GL_LINE_LOOP)
                
                # do the four sides of a box
                glVertex3f(body.left(), body.top(), 0.0)
                glVertex3f(body.right(), body.top(), 0.0)
                glVertex3f(body.right(), body.bottom(), 0.0)
                glVertex3f(body.left(), body.bottom(), 0.0)

                glEnd()
                glColor3f(1,1,1)
