#!/usr/bin/python3

# Important Libraries
import pyglet

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

        # this assumes that all of the images are the same width and height
        totalHeight = 0
        for row in files:
            # get the images
            images = [load(file) for file in row] 
            
            totalWidth = 0
            for img in images:
                sprite = makeSprite(img, x + totalWidth, y - totalHeight) 
                totalWidth += img.width
                self.sprites.append(sprite)

            # move the "cursor" to the next line
            totalHeight += images[0].height

    def draw(self, t=0, *other):
        #self.batch.draw() 
        for sprite in self.sprites:
            sprite.draw()

