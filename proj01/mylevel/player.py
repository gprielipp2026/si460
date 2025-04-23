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
                       sounds={}):

        # Store the sprites, and the sprite building function
        self.sprites      = sprites
        self.buildSprite  = buildSprite
        self.playerSprite = None
        self.attackBlock  = False
        self.attackUnblock = 0.0
        self.weapon_factory = lambda *args: print(f'null_func({args})')

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

        # save the sounds
        self.sounds = sounds

        # Build the starting character sprite
        self.changeSprite()

        # keep track of the time locally
        self.t = 0
        self.dt = 0
      
        self.updatelabel()

    def set_weapon_factory(self, factory):
        self.weapon_factory = factory

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
        if self.hp <= 0:
            return

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
        else:
            # if you're outside the box, fall
            self.isFalling = True

        # check collisions of the enemies

        for enemy in enemies:
            ex,ey = enemy.getX(), enemy.getY()
            x, y  = self.playerSprite.x, self.playerSprite.y
            w1, h1 = enemy.playerSprite.width, enemy.playerSprite.height
            w2, h2 = self.playerSprite.width, self.playerSprite.height
            # (left, right, bottom, top)
            r1 = ( ex - w1/2.0, ex + w1/2.0, ey,  ey+h1 )
            r2 = ( x - w2/2.0, x + w2/2.0, y,  y+h2)

            # player can sustain 2 hits
            if self.overlapping(r1, r2):
                #print(f'[colliding] {self.playerClass} collided with {enemy.playerClass}')
                if self.isAttacking:
                    enemy.hit(100)
                    #print('Enemy took damage: dead')
                elif not enemy.hp <= 0: # cannot take damage from a dead enemy
                    self.hit(50)
                    #print(f'Hero took damage: {self.hp=} at {r1}\t{r2}')
           
    # check if two rectangles are overlapping
    # defined each as: (left, right, bottom, top
    def overlapping(self, rect1, rect2):
        l1, r1, b1, t1 = rect1
        l2, r2, b2, t2 = rect2

        left   = l2 <= l1 <= r2
        right  = l2 <= r1 <= r2
        bottom = b2 <= b1 <= t2
        top    = b2 <= t1 <= t2

        return (left or right) and (bottom or top)

    def manageDeath(self):
        if self.mode == 'Dead':
            return
        print(f'{self.playerClass} died')
        self.mode = 'Dead'
        self.changeSprite(self.mode, self.facing)

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
                                             self.animationLoop if mode != 'Dead' else False,
                                             self.animationX,
                                             self.animationY)
        
        if mode in self.sounds:
            # play the sound
            self.sounds[mode].play()

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
        self.isAttacking = key.LCTRL in keyTracking or key.RCTRL in keyTracking
        self.isThrowing  = key.LALT in keyTracking or key.RALT in keyTracking
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
            if (not isMoving or self.isAttacking or self.isThrowing) and self.step > 15 and self.fallingSpeed < 180:
                self.fallingSpeed *= 1.3
            elif isMoving and self.fallingSpeed > 45 and not self.isAttacking and not self.isThrowing:
                self.fallingSpeed = 45

            if self.step <= 15 and self.isJumping:
                # y speed is 160
                mode = 'Jump'
                self.playerSprite.y += math.sin(math.radians(90.0/15.0*self.step)) * 15 
            else:
                self.playerSprite.y -= self.fallingSpeed * self.dt
                self.isJumping = False

            self.step += 1.0
        if not self.attackBlock:
            if self.isAttacking:
                mode = 'Jump-Attack' if isJumping else 'Attack'
            elif self.isThrowing:
                mode = 'Jump-Throw' if isJumping else 'Throw'
                # spawn a throwable kunai
                if not self.attackBlock:
                    #print('Spawning weapon') 
                    x = self.playerSprite.x + self.playerSprite.width/2.0 
                    y = self.playerSprite.y + self.playerSprite.height/2.0 
                    self.weapon_factory(self.facing, x, y)
                    self.attackBlock = True
                    self.attackUnblock = 1.5 + self.t

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
            
    # move the weapon along
    def moveWeapon(self):
        speed = 50 
        self.playerSprite.x += (-1 if self.facing == 'Left' else 1) * speed * self.dt
        #print(f'[moveWeapon] at pos {self.playerSprite.x}')

    # Draw our character
    def draw(self, t=0, keyTracking={}, *other):
        self.dt = t - self.t
        self.t = t
        
        #print(f'[draw] can{"not" if self.attackBlock else ""} attack')

        if self.t >= self.attackUnblock:
            self.attackBlock = False

        if not self.mode == 'Dead':
            if self.playerClass == 'hero':
                self.movement(t, keyTracking)
            elif 'enemy' in self.playerClass:
                self.ai(t)
            elif 'weapon' in self.playerClass:
                self.moveWeapon()

        self.playerSprite.draw()
        
        if self.position is not None:
            self.position.draw()

