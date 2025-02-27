class RigidBody:
    def __init__(self, x, y, width, height):
        self.pos = Vector(x,y)
        self.width = width
        self.height = height
        self.velocity = Vector(0,0)

    def isColliding(self, other):
        # check to see if any edge of my box is inside their box
        top = self.top() <= other.top() and self.top() >= other.bottom()
        bottom = self.bottom() <= other.top() and self.bottom() >= other.bottom()
        left = self.left() <= other.right() and self.left() >= other.left()
        right = self.right() <= other.right() and self.right() >= other.left()
        return any([top, bottom, left, right])

    def applyForce(self, force):
        # assume m (mass) = 1
        # F = m*a
        # F = a (simplified for assumption)
        self.velocity += force

    def applyVelocity(self, vel):
        self.position += vel

    def update(self, dt):
        self.applyForce(Vector(0,-1)*dt) # gravity
        self.applyVelocity(self.velocity*dt)

    def top(self):
        return self.getY() + self.height
    
    def bottom(self):
        return self.getY()
    
    def left(self):
        return self.getX()
    
    def right(self):
        return self.getX() + self.width()

    def getX(self):
        return self.pos.x

    def getY(self):
        return self.pos.y
    

# simple class to represent forces, positions, and velocities
import numpy
class Vector:
    def __init__(self, *args):
        if type(args) == numpy.ndarray:
            self.v = args
        else:
            self.v = numpy.array([*args], dtype='float64')
    
    def __add__(self, other):
        return Vector(self.v + other.v)
    
    def __sub__(self, other):
        return Vector(self.v - other.v)
    
    def __mul__(self, other):
        if type(other) in [float, int]:
            return Vector(self.v * other)
        else:
            raise Exception(f'Vector does not support multiplication with {type(other)}')