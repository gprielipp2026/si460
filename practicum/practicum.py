#!/usr/bin/env python3

import pyglet, sys
from pyglet.gl import *
from pyglet.window import Window, key, mouse
import numpy as np
from random import uniform
from pyglet.math import Mat4, Vec3
import ctypes

# https://docs.python.org/3/library/dataclasses.html
# for a quick and dirty c-like struct
from dataclasses import dataclass

@dataclass
class Pos:
    x: float
    y: float 
    orientation: int = 1
    w: float = 30   
    h: float = 30 * np.sin(np.pi/3.0)

    def __add__(self, other):
        if isinstance(other, Pos):
            self.x += other.x
            self.y += other.y
            return self
    
    def __mul__(self, other):
        if type(other) in [int, float]:
            self.x *= other
            self.y *= other
            return self

    def vertices(self) -> tuple:
        """
            a
           b c
         -- or --
           b c
            a
        """
        # the points of the triangles above
        b = self.x - self.w / 2.0
        c = self.x + self.w / 2.0
        a = self.y + self.h * self.orientation
        
        return ( (b, self.y, 0.0), (c, self.y, 0.0), (self.x, a, 0.0) )

    # just treat overlapping like two rects
    def overlap(self, other):
        # areas to check for me

        # this is going to be used as enemy.overlap(player)

        # enemy
        l1 = self.x - self.w / 2.0
        r1 = self.x + self.w / 2.0
        t1 = self.y
        b1 = self.y - self.h
        
        # areas to check for them
        #player
        l2 = other.x - other.w / 2.0
        r2 = other.x + other.w / 2.0
        t2 = other.y + other.h
        b2 = other.y

        # check overlaps
        left = l1 <= l2 <= r1
        right = l1 <= r2 <= r1
        top = b1 <= t2 <= t1
        bottom = b1 <= b2 <= t1

        return (left or right) and (top or bottom)


@dataclass
class Missile:
    x: float
    y: float 
    w: float = 10   
    h: float = 30 

    def __add__(self, other):
        if isinstance(other, Pos):
            self.x += other.x
            self.y += other.y
            return self
    
    def __mul__(self, other):
        if type(other) in [int, float]:
            self.x *= other
            self.y *= other
            return self
   
    def overlap(self, other):
        # areas to check for me
        l1 = self.x - self.w / 2.0
        r1 = self.x + self.w / 2.0
        t1 = self.y + self.h
        b1 = self.y
        
        # areas to check for them
        # this is going to be an enemy
        l2 = other.x - other.w / 2.0
        r2 = other.x + other.w / 2.0
        t2 = other.y
        b2 = other.y - other.h

        # check overlaps
        left = l1 <= l2 <= r1
        right = l1 <= r2 <= r1
        top = b1 <= t2 <= t1
        bottom = b1 <= b2 <= t1

        return (left or right) and (top or bottom)

    def vertices(self) -> tuple:
        """
         a b

         c d
        """
        # the points of the shape above
        left = self.x - self.w / 2.0
        right = self.x + self.w / 2.0
        top = self.y + self.h
        bottom = self.y

        a = (left, top, 0.0)
        b = (right, top, 0.0)
        c = (left, bottom, 0.0)
        d = (right, bottom, 0.0)

        return (a, c, b, d) # defined as a TRIANGLE_STRIP

class Scene(Window):
    def __init__(self, width, height, ):
        super().__init__(width=width, height=height, resizable=True,
                         caption='Practicum') 
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # get draw to be called many repeatedly 
        pyglet.clock.schedule_interval(self.on_draw, 1/24.0) # 24 frames per second

        self.sliding = False
        self.rotating = False

        self.p1 = self.p2 = np.array([0,0])
        self.translate = np.array([-self.width / 2.0, -self.height/2.0])
        self.scale = np.array([0,0,1,1])
        self.arcball = Mat4.from_rotation(0.0, Vec3(0,0,0))

        # position of the spaceship
        self.pos = Pos(self.width / 2.0, 10) # just need to define x & y
        self.hp  = 100
            
        # for determing how the spaceship will move
        self.keyTracker = []

        # position of the enemies
        self.enemies = [ Pos(x, self.height - 40, orientation=-1) for x in self.gen(0,
                                                                    self.width,self.width
                                                                    / 10) ]
        
        # the missiles
        self.missiles = []

    # simple generator
    def gen(self, start, stop, step):
        while start < stop:
            yield start
            start += step

    def on_key_press(self, symbol, modifiers):
        if symbol == key.C and modifiers & key.MOD_CTRL:
            print('exiting...')
            sys.exit(0)
        
        # can only shoot one at a time
        if symbol == key.SPACE:       
            # shoot a lazer
            print('pew pew')
            self.missiles.append(Missile(self.pos.x, self.pos.y))

        # add the key to the list if it moves the player
        if symbol in [key.LEFT, key.RIGHT, key.UP, key.DOWN]:
            self.keyTracker.append(symbol)

    def on_key_release(self, symbol, modifiers):
        if symbol in self.keyTracker:
            self.keyTracker.remove(symbol)
    

    def on_mouse_press(self, x, y, symbol, modifiers):
        if symbol == mouse.LEFT:
            self.p1 = self.p2 = np.array([x,y])
            self.sliding = True

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.sliding:
            self.p2 = np.array([x,y])
           

    def on_mouse_release(self, x, y, symbol, modifiers):
        if self.sliding: 
            self.translate += self.p2 - self.p1
            self.p1 = self.p2 = np.array([0,0])
            self.sliding = False
    
    def on_mouse_scroll(self, x, y, scrollx, scrolly):
        factor = 1.1 if scrolly > 0 else 0.9
        self.scale = factor * self.scale
        self.scale[0:2] = [x, y]

    def update_pos(self, dt):
        # take the key tracker and build a vector to move the player
        speed = 15
        moves = {65361:  Pos(-1,0), #left 
                 65363: Pos(1,0),   #right
                 65362:    Pos(0,1),#up
                 65364:  Pos(0,-1)} #down
        
        for key in self.keyTracker:
            self.pos += moves[key] * speed * dt
    
    def update_missiles(self, dt):
        speed = 30

        for missile in self.missiles:
            missile += Pos(0, 1) * speed * dt  

            # handle outside world
            if missile.y > self.height:
                self.missiles.remove(missile)

            # check collisions with all enemies
            for enemy in self.enemies:
                if missile.overlap(enemy):
                    self.missiles.remove(missile)
                    self.enemies.remove(enemy)
                    print('Enemy hit!')


    def update_enemies(self, dt):
        speed = 10

        for enemy in self.enemies:
            # move enemy
            enemy += Pos(0, -1) * speed * dt

            # check collision with player
            if enemy.overlap(self.pos):
                self.hp -= 25
                self.enemies.remove(enemy)

                if self.hp <= 0:
                    self.exit('Player died')

    def exit(self, msg):
        print(msg)
        sys.exit(0)

    def on_draw(self, dt=0):            

        # clear the screen
        self.clear()

        # set viewport and frustum
        glViewport(0,0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        scale = 10.0
        glFrustum(-scale, scale, -scale, scale, 5.0, 10000.0)
        glMatrixMode(GL_MODELVIEW)

        # set environment to handle depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # draw the stuff
        glLoadIdentity()
        
        # translate the world into view
        glTranslatef(-self.width/2.0, -self.height/2.0, -200.0)

        # translate the matrix based on the left mouse click
        #tx,ty = (self.translate + ((self.p2 - self.p1) if self.sliding else np.array([0,0])))
        #glTranslatef(tx, ty, -100.0)
        
        # scale the world around the cursor based on the scroll wheel
        #tsx, tsy, sx, sy = self.scale
        
        #glScalef(sx, sy, sy)
            
        # update the scene (player and enemies)
        if dt == 0: dt = 0.1
        self.update_pos(dt) # this handles the player movement


        # draw the hp bar
        # left, right, y = coordinates for the health bar to sit
        left, right, y = self.pos.x - self.pos.w / 2.0, self.pos.x + self.pos.w / 2.0, self.pos.y - 10
            
        # put the red one as a background 
        glColor4f(1.0,0.0,0.0,1.0)
        glLineWidth(5.0)
        glBegin(GL_LINES)
        glVertex3f(left, y, 0.0) 
        glVertex3f(right, y, 0.0) 

        # put the green "health" bar in 
        glColor4f(0.0,1.0,0.0,1.0)
        glVertex3f(left, y, 0.0) 
        glVertex3f(left + (self.hp / 100.0)*(self.pos.w), y, 0.0) # some percentage along the width 

        glEnd()

        # reset the line width
        glLineWidth(1.0)

        # draw the player
        glColor4f(0.0,1.0,0.0,1.0)
        glBegin(GL_TRIANGLES)
        for vertex in self.pos.vertices():
            glVertex3f(*vertex)
        glEnd()
        
        # update the missiles
        self.update_missiles(dt)

        # draw any missile
        glColor4f(1.0,1.0,1.0,1.0)
        for missile in self.missiles:
            glBegin(GL_TRIANGLE_STRIP)

            for vertex in missile.vertices():
                glVertex3f(*vertex)
            
            glEnd()
        
        # update the enemies
        self.update_enemies(dt)

        # draw the enemies
        glColor4f(1.0, 0.0, 0.0, 1.0)
        for enemy in self.enemies:
            glBegin(GL_TRIANGLES)
            
            for vertex in enemy.vertices():
                glVertex3f(*vertex)

            glEnd()
            
            # check game over
            if enemy.y <= 0:
                self.exit('Enemies made it to your base!, you lose')

        
if __name__ == '__main__':

    scene = Scene(500, 500)
    pyglet.app.run()



