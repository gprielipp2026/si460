#!/usr/bin/python3

# G. W. Prielipp (m265112)
import numpy

import math

scalars = [int, float, numpy.float64]

# The beginnings of a Vector3D
class Vector3D:
    def __init__(self, val, *args):
        if type(val) is numpy.ndarray:
            self.v = val
        elif args and len(args) == 2:
            self.v = numpy.array([val,args[0],args[1]], dtype='float64')
        else:
            raise Exception("Invalid Arguments to Vector3D")
    
    def __repr__(self):
        return str(self.v)

    def __str__(self):
        return str(self.v)
   
    # add two vectors together
    def __add__(self, other):
        return Vector3D(self.v + other.v)
    
    # subtract two vectors
    def __sub__(self, other):
        return Vector3D(self.v - other.v)
    
    # take the dot product of two vectors
    def dot(self, other):
        return self.v.dot(other.v) 
    
    # return the dot product from an angle and vector 
    def dotangle(self, other, angle):
        # angle is in radians
        return self.magnitude() * other.magnitude() * math.cos(angle) 
    
    # scale a vector
    def scalar(self, a):
        return Vector3D(self.v * a) 
    
    # Allows the notation of v * a and v * u (vector * scalar or vector *
    # vector)
    def __mul__(self, other):
        if type(other) in scalars:
            return self.scalar(other)
        elif isinstance(other, Vector3D) or isinstance(other, Normal):
            return self.dot(other)
        else:
            raise Exception(f'Error: Vector3D * {type(other)}')
    
    # divide a vector by a scalar
    def __truediv__(self, a):
        if type(a) not in scalars:
            raise Exception(f'Error: Vector3D / {type(other)}')
        return Vector3D(self.v / a) 
    
    # return a new vector that has the same values
    def copy(self):
        return Vector3D(self.v.copy()) 
    
    # take the magnitude
    def magnitude(self):
        return numpy.sqrt(self.square()) 

    # x^2 + y^2 + z^2
    def square(self):
        return (self.v * self.v).sum() 

    # return the cross product
    def cross(self, other):
        return Vector3D(numpy.cross(self.v, other.v)) 

# represents a point in 3D space
class Point3D:
    def __init__(self, v, *args):
        if isinstance(v, numpy.ndarray):
            self.v = v
        elif len(args) == 2:
            self.v = numpy.array([v, args[0], args[1]], dtype='float64')
        else:
            raise Exception('invalid arguments passed to Point3D')
    def __repr__(self):
        return str(self.v)

    def __str__(self):
        return str(self.v)
    
    # add a vector and point
    def __add__(self, other):
        if isinstance(other, Vector3D):
            return Point3D(self.v + other.v)
        else:
            raise Exception(f'cannot add a {type(other)} to a Point3D')
    
    # allows notation of p1 - p2 = vector or point - vector = point
    def __sub__(self, other):
        if isinstance(other, Vector3D):
            return Point3D(self.v - other.v)
        elif isinstance(other, Point3D):
            return Vector3D(self.v - other.v)
    
    # the distance squared to a given point
    def distancesquared(self, point):
        vector = self - point
        return vector.square()
    
    # the distance between this point and a given point
    def distance(self, point):
        vector = self - point
        return vector.magnitude()
    
    # get a Point with the same x,y,z
    def copy(self):
        return Point3D(self.v.copy())

    def __mul__(self, constant):
        if type(constant) in scalars:
            return Point3D(self.v * constant)
        else:
            raise Exception(f'cannot multiply a Point3D by a {type(constant)}')

# A Normal for defining surfaces
class Normal:
    def __init__(self, v, *args):
        if isinstance(v, numpy.ndarray):
            self.v = v
        elif len(args) == 2:
            self.v = numpy.array([v, args[0], args[1]], dtype='float64')
            #mag = numpy.sqrt((self.v * self.v).sum())
            #self.v = self.v / mag
        else:
            raise Exception('invalid arguments passed to Normal')
    def __repr__(self):
        return str(self.v)

    def __str__(self):
        return str(self.v)
    
    # returns Normal(-x,-y,-z)
    def __neg__(self):
        return Normal(-self.v)
    
    # performs vector addition
    def __add__(self, other):
        if isinstance(other, Vector3D):
            return Vector3D(self.v + other.v)
        elif isinstance(other, Normal):
            return Normal(self.v + other.v)

    # takes the dot product of two normals or a normal and a vector
    def dot(self, other):
        if type(other) in [Vector3D, Normal]:
            return self.v.dot(other.v)
        else:
            raise Exception(f'Normal.dot({type(other)}) is not defined')

    # scalar multiply a Normal
    def scalar(self, other):
        if type(other) in scalars:
            return Normal(self.v * other)
        else:
            raise Exception(f'Cannot scalar multiply a Normal with a {type(other)}')
    
    # convenient notation to allow the scalar and dot product to piggyback on
    # the '*' operator
    def __mul__(self, other):
        if type(other) in [Vector3D, Normal]:
            return self.dot(other)
        else:
            return self.scalar(other)

    # copy the values of the normal and pass them on to a new normal
    def copy(self):
        return Normal(self.v.copy())

# Ray class
class Ray:
    def __init__(self, origin: Point3D, direction: Vector3D):
        self.origin = origin
        self.direction = direction
   
    # constructs the representation as: [origin, direction]
    def __repr__(self):
        return f'[{str(self.origin)}, {str(self.direction)}]'
    
    # str gets called more
    def __str__(self):
        return repr(self)

    # copy the values of the ray and pass them on to a new ray
    def copy(self):
        return Ray(self.origin.copy(), self.direction.copy())

    # calculates the point along a given ray
    def pointAlong(self, scale):
        return self.origin + self.direction * scale

    # calculate if a Vector3D is perpendicular to the Ray's Direction
    def isPerpendicularTo(self, vec):
        return self.direction * vec == 0

    # Semi-decent OOP practices:
    def getOrigin(self):
        return self.origin
    def getDirection(self):
        return self.direction

# Represents an RGB color from (0,0,0) - (1,1,1)
class ColorRGB:
    def __init__(self, val, *args):
        if type(val) is numpy.ndarray:
            self.v = val
        elif len(args) == 2:
            self.v = numpy.array([val, args[0], args[1]], dtype='float64')
        else:
            raise Exception('ColorRGB constructor expects 1 ndarray(3) or 3 floats')
    
    # create a new color with the same value
    def copy(self):
        return ColorRGB(self.v.copy()) 

    # create the representation as [r g b]
    def __repr__(self):
        return str(self.v)

    # str gets called more
    def __str__(self):
        return repr(self)
    
    # get the individual R, G, B values and return it individually
    def get(self, field):
        fields = {'r': 0, 'g': 1, 'b': 2}
        return self.v[fields[field]]

    # add two colors and return the resulting Color
    def __add__(self, color):
        if not isinstance(color, ColorRGB):
            raise Exception(f'Cannot add a ColorRGB and a {type(color)}')
        # I want to make sure the result is between 0 and 1, but I don't know if that's the definition of this function
        return ColorRGB(self.v + color.v)

    # multiply a color by a scalar or another ColorRGB object
    # I'm not sure how ColorRGB * ColorRGB = ColorRGB is supposed to work
    def __mul__(self, other):
        # I know that it says has to be by a float in the definition ... (why can't I have an int here?)
        if type(other) in scalars:
            return ColorRGB(self.v * other)
        elif type(other) is ColorRGB:
            return ColorRGB(self.v * other.v)
        else:
            raise Exception(f'Cannot multiply a ColorRGB and a {type(other)}')

    # divide the color by a scalar value
    def __truediv__(self, scalar):
        if not type(other) is float:
            raise Exception(f'Cannot divide a ColorRGB by a {type(other)}')
        elif scalar == 0:
            raise Exception('Cannot divide by zero')
        return ColorRGB(self.v / scalar)
       
    # raise the individual color values to the value of the float
    def __pow__(self, val):
        # I know that it says has to be by a float in the definition ... (why can't I have an int here?)
        if not type(val) in scalars:
            raise Exception(f'Cannot raise a ColorRGB to the power of {type(other)}')
        return ColorRGB(self.v ** val)

# a 2D Plane from a given origin and Normal
class Plane:
    def __init__(self, point, normal, color=ColorRGB(1,1,1)):
        self.point = point
        self.normal = normal
        self.color = color

    # return a new Plane with the same parameters
    def copy(self):
        return Plane(self.point.copy(), self.normal.copy(), self.color.copy())

    # the string representation of a plane: [point, normal]
    def __repr__(self):
        return f'[{str(self.point)}, {str(self.normal)}]'
    
    # str gets called more
    def __str__(self):
        return repr(self)

    # returns: (BOOLEAN, FLOAT, Point3D, ColorRGB)
    #           is hit,   t   ,intersect, pane color
    def hit(self, ray, shadeRec=False):
        if ray.isPerpendicularTo(self.normal):
            return (False, None, None, None)

        t = ((self.point - ray.getOrigin()) * self.normal) / (ray.getDirection() * self.normal)
        
        return (True, t, ray.pointAlong(t), self.color.copy())


# We should always have debugging in our libraries
# that run if the file is called from the command line
# vice from an import statement!
if __name__ == '__main__':
    from inspect import isclass
    import testing
    
    # highly vulnerable code here :)
    tests = [eval('testing.'+x+'()') for x in dir(testing) if isclass(getattr(testing, x))]
    for test in tests:
        test.run()


