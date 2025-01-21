#!/usr/bin/python3

# G. W. Prielipp (m265112)
import numpy

import math
# The beginnings of a Vector3D
class Vector3D:
    def __init__(self, val, *args):
        if type(val) is numpy.ndarray:
            self.v = val
        elif args and len(args) == 2:
            self.v = numpy.array([val,args[0],args[1]], dtype='float64')
        else:
            raise Exception("Invalid Arguments to Vector3D")
    
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
        if type(other) in [int, float]:
            return self.scalar(other)
        elif isinstance(other, Vector3D) or isinstance(other, Normal):
            return self.dot(other)
        else:
            raise Exception(f'Error: {other} does not work for multiplication')
    
    # divide a vector by a scalar
    def __div__(self, a):
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
        if type(constant) in [int, float]:
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
        if type(other) in [int, float]:
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

    # copy the values of the ray and pass them on to a new ray
    def copy(self):
        return Ray(self.origin.copy(), self.direction.copy())

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
        pass

    # create the representation as [r g b]
    def __repr__(self):
        return str(self.v)

    # get the individual R, G, B values and return it individually
    def get(self, field):
        fields = {'r': 0, 'g': 1, 'b': 2}
        return self.v[fields[field]]

    # add two colors and return the resulting Color
    def __add__(self, color):
        if not isinstance(color, ColorRGB):
            raise Exception(f'Cannot add a ColorRGB and a {type(color)}')
        return ColorRGB(self.v + color.v)


        

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


