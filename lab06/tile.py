#!/usr/bin/python3

# Important Libraries
import pyglet

# a tile class that loads in the images and displays them
class Tile:
    def __init__(self, files, x, y):
        # what will actually display the images
        # is supposed to allow me to make rendering faster (less calls), but it wasn't working
        #self.batch = pyglet.graphics.Batch()

        # get the images
        load = lambda fn: pyglet.image.load(fn)
        images = [load(file) for file in files] 
        
        # make the sprites
        makeSprite = lambda img, ix, iy: pyglet.sprite.Sprite(img=img, x=ix, y=iy)#, batch=self.batch)
        self.sprites = []
        totalWidth = 0
        for img in images:
            sprite = makeSprite(img, x + totalWidth, y) 
            totalWidth += img.width
            self.sprites.append(sprite)

    def draw(self, t=0, *other):
        #self.batch.draw() 
        for sprite in self.sprites:
            sprite.draw()

