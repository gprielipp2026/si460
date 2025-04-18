#!/usr/bin/python3

# Important Libraries
import pyglet, config, random, math
from pyglet.window import key

# Our Hero Class
class Player:
    def __init__(self, sprites={},
                       buildSprite=None,
                       playerClass="hero",
                       mode="Run",
                       facing="Right",
                       speed=0.05,
                       scale=0.15,
                       loop=True,
                       x=380,
                       y=250,
                       sounds=None):

        # Store the sprites, and the sprite building function
        self.sprites      = sprites
        self.buildSprite  = buildSprite
        self.playerSprite = None

        # number of hits the hero can take
        self.hp = 100

        # Some basic settings
        self.animationSpeed = speed
        self.animationScale = scale
        self.animationLoop  = loop
        self.animationX     = x
        self.animationY     = y
        self.playerClass    = playerClass
        self.mode           = mode
        self.facing         = facing
        self.fallingSpeed   = 0.0
        self.step           = 0
        self.isFalling      = False
        self.isJumping      = False
        self.isMoving       = False
        self.position       = None
        self.isAttacking    = None

        # Build the starting character sprite
        self.changeSprite()

        # keep track of the time locally
        self.t = 0
        self.dt = 0

        # save the sounds
        self.sounds =  sounds

        self.updatelabel()

    def set_level(self, level, width, height):
        self.level = level
        self.width = width
        self.height = height

    def updatelabel(self):
        if self.playerClass == "hero":
            x,y=self.playerSprite.x, self.playerSprite.y
            self.position = pyglet.text.Label(f'({x:.2f}, {y:.2f}) => ({x//50},{y//50})',x=100,y=580) # hard coded numbers

    # for collision detection
    def collide(self, enemies=[]):
        level, width, height = self.level, self.width, self.height
        testY = self.playerSprite.y
        testX = self.playerSprite.x 

        modifier = 1 if self.facing == 'Right' else -1

        coordY = testY // height
        coordX = testX // width
        
        minX, maxX = width * coordX, width * (coordX + 1)
        if coordY in level:
            if coordX not in level[coordY]:
                self.isFalling = True
            else:
                self.isFalling = False
            # horizontal edge detection and correction
            if coordY + 1 in level:
                if coordX in level[coordY+1]:
                    if testX >= minX and testX <= maxX:
                        dl, dr = testX - minX, maxX - testX
                        if dr > dl:
                            self.playerSprite.x = minX
                            coordX = minX // width 
                        else:
                            self.playerSprite.x = maxX 
                            coordX = maxX // width
            if testY <= (coordY+1) * height and coordY + 1 in level and coordX in level[coordY + 1]:
                self.playerSprite.y = (coordY + 1)* height

        # check collisions of the enemies

        for enemy in enemies:
            ex,ey = enemy.getX(), enemy.getY()
            gridEX = ex // width
            gridEY = ey // height
            coordX = getX() // width
            coordY = getY() // height

            # player can sustain 2 hits
            

    def manageDeath(self):
        pass

    def hit(self, points):
        self.hp -= points
        if self.hp <= 0:
            self.manageDeath()

    def getX(self):
        return self.playerSprite.x
    def getY(self):
        return self.playerSprite.y

    # Build the initial character
    def changeSprite(self, mode=None, facing=None):
        # if self.mode == mode and mode != 'Glide':
        #     return

        if mode is not None:
            self.mode = mode
        if facing is not None:
            self.facing = facing
        if self.playerSprite is not None:
            self.animationX = self.playerSprite.x
            self.animationY = self.playerSprite.y

        self.playerSprite = self.buildSprite(self.sprites,
                                             self.playerClass,
                                             self.mode,
                                             self.facing,
                                             self.animationSpeed,
                                             self.animationScale,
                                             self.animationLoop,
                                             self.animationX,
                                             self.animationY)

    # figure out which animation should be showing
    def interpretAnimation(self, keyTracking={}):
        facing = self.facing
        
        if key.LEFT in keyTracking and key.RIGHT in keyTracking:
            pass
        elif key.LEFT in keyTracking:
            facing = 'Left'
        elif key.RIGHT in keyTracking:
            facing = 'Right'

        if facing != self.facing:
            self.changeSprite(mode=self.mode, facing=facing)
        self.facing = facing
        
        

    # Move the character
    def movement(self, t=0, keyTracking={}): 
        self.interpretAnimation(keyTracking)

        isMoving  = key.LEFT in keyTracking or key.RIGHT in keyTracking
        isJumping = key.SPACE in keyTracking 
        isRunning = (key.LSHIFT in keyTracking or key.RSHIFT in keyTracking) and isMoving
        isAttacking = key.LCTRL in keyTracking or key.RCTRL in keyTracking
        isThrowing  = key.LALT in keyTracking or key.RALT in keyTracking
        direction = -1 if self.facing == 'Left' else 1 # multiplier

        mode = 'Idle'
        if isJumping and not self.isFalling and not self.isJumping:           
            self.isJumping = True
            self.fallingSpeed = 0.0
            self.step = 0
        elif self.isFalling and not self.isJumping and isMoving:
            mode = 'Glide'
        elif isRunning or isMoving:
            mode = 'Run'


        if self.isFalling or self.isJumping:
            if self.step == 0:
                self.fallingSpeed = 1.0

            if self.step > 15 and self.fallingSpeed < 45:
                self.fallingSpeed *= 1.1
            if (not isMoving or isAttacking or isThrowing) and self.step > 15 and self.fallingSpeed < 180:
                self.fallingSpeed *= 1.3
            elif isMoving and self.fallingSpeed > 45 and not isAttacking and not isThrowing:
                self.fallingSpeed = 45

            if self.step <= 15 and self.isJumping:
                # y speed is 160
                mode = 'Jump'
                self.playerSprite.y += math.sin(math.radians(90.0/15.0*self.step)) * 15 
            else:
                self.playerSprite.y -= self.fallingSpeed * self.dt
                self.isJumping = False

            self.step += 1.0

        if isAttacking:
            mode = 'Jump-Attack' if isJumping else 'Attack'
        elif isThrowing:
            mode = 'Jump-Throw' if isJumping else 'Throw'
            # spawn a throwable kunai

        self.playerSprite.x += direction * 100 * (1.5 if isRunning else 1) * (1 if isMoving else 0) * self.dt

        if mode != self.mode:
            self.changeSprite(mode=mode, facing=self.facing)
        self.updatelabel()

    # movement for enemies
    def ai(self, t):
        level, width, height = self.level, self.width, self.height
        # try walking forwards:
        direction = -1 if self.facing == 'Left' else 1
        enemySpeed = 75
        testX = self.playerSprite.x + enemySpeed * direction * self.dt

        # if edge, turn around
        coordX = testX // width # get this number from somewhere else
        coordY = self.playerSprite.y // height

        # check for a wall
        if coordY + 1 in level:
            if coordX in level[coordY + 1]:
                self.facing = 'Left' if self.facing == 'Right' else 'Right'
                self.changeSprite(mode='Run', facing=self.facing)
        # check for a floor
        if coordY - 1 in level:
            if coordX not in level[coordY - 1]:
                self.facing = 'Left' if self.facing == 'Right' else 'Right'
                self.changeSprite(mode='Run', facing=self.facing)
        
        direction = -1 if self.facing == 'Left' else 1
        self.playerSprite.x += enemySpeed * direction * self.dt
            
    # Draw our character
    def draw(self, t=0, keyTracking={}, *other):
        self.dt = t - self.t
        self.t = t

        if self.playerClass == 'hero':
            self.movement(t, keyTracking)
        elif 'enemy' in self.playerClass:
            self.ai(t)
        self.playerSprite.draw()
        
        if self.position is not None:
            self.position.draw()

