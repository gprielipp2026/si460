class RigidBody:
    def __init__(self, x, y, width, height, type):
        self.pos = Vector(x,y)
        self.width = width
        self.height = height
        self.velocity = Vector(0,0)
        self.type = type

    def isColliding(self, other):
        # check to see if any edge of my box is inside their box
        top = self.top() <= other.top() and self.top() >= other.bottom()
        bottom = self.bottom() <= other.top() and self.bottom() >= other.bottom()
        left = self.left() <= other.right() and self.left() >= other.left()
        right = self.right() <= other.right() and self.right() >= other.left()
        result = (top and left or top and right) or (bottom and left or bottom and right)
        return ( result , self.type)

    def applyForce(self, force):
        # assume m (mass) = 1
        # F = m*a
        # F = a (simplified for assumption)
        self.velocity += force

    def getType(self):
        return self.type

    def applyVelocity(self, vel):
        self.pos += vel

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
        return self.getX() + self.width

    def getX(self):
        return self.pos.x

    def getY(self):
        return self.pos.y
    

# simple class to represent forces, positions, and velocities
import numpy
class Vector:
    def __init__(self, *args):
        if isinstance(args[0], numpy.ndarray):
            self.v = args[0]
        else:
            self.v = numpy.array([x for x in args], dtype='float64')
    
    def __getattribute__(self, name):
        v = object.__getattribute__(self, 'v')
        if name == 'x':
            return v[0]
        elif name == 'y':
            return v[1]
        elif name == 'v':
            return v
        else:
            raise Exception(f'Vector object has no atrribute "{name}"')

    def __add__(self, other):
        return Vector(self.v + other.v)
    
    def __sub__(self, other):
        return Vector(self.v - other.v)
    
    def __mul__(self, other):
        if type(other) in [float, int]:
            return Vector(self.v * other)
        else:
            raise Exception(f'Vector does not support multiplication with {type(other)}')