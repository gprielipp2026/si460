#!/usr/bin/python3

# G. W. Prielipp (m265112)
import numpy

import math

# The beginnings of a Vector3D - For you to edit
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
    
    def __add__(self, other):
        return Vector3D(self.v + other.v)

    def __sub__(self, other):
        return Vector3D(self.v - other.v)

    def dot(self, other):
        return self.v.dot(other.v) 

    def dotangle(self, other, angle):
        # angle is in radians
        return self.magnitude() * other.magnitude() * math.cos(angle) 

    def scalar(self, a):
        return Vector3D(self.v * a) 

    def __mul__(self, other):
        if type(other) in [int, float]:
            return self.scalar(other)
        elif isinstance(other, Vector3D) or isinstance(other, Normal):
            return self.dot(other)
        else:
            raise Exception(f'Error: {other} does not work for multiplication')

    def __div__(self, a):
        return Vector3D(self.v / a) 

    def copy(self):
        return Vector3D(self.v.copy()) 

    def magnitude(self):
        return numpy.sqrt(self.square()) 

    def square(self):
        return (self.v * self.v).sum() 

    def cross(self, other):
        return Vector3D(numpy.cross(self.v, other.v)) 


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
    
    def __add__(self, other):
        return Point3D(self.v + other.v)

    def __sub__(self, other):
        if isinstance(other, Vector3D):
            return Point3D(self.v - other.v)
        elif isinstance(other, Point3D):
            return Vector3D(self.v - other.v)

    def distancesquared(self, point):
        vector = self - point
        return vector.square()

    def distance(self, point):
        vector = self - point
        return vector.magnitude()
    
    def copy(self):
        return Point3D(self.v.copy())

    def __mul__(self, constant):
        return Point3D(self.v * constant)

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
        
    def __neg__(self):
        return Normal(-self.v)

    def __add__(self, other):
        if isinstance(other, Vector3D):
            return Vector3D(self.v + other.v)
        elif isinstance(other, Normal):
            return Normal(self.v + other.v)
   
    def dot(self, other):
        return self.v.dot(other.v)

    def scalar(self, other):
        return Normal(self.v * other)

    def __mul__(self, other):
        if type(other) in [Vector3D, Normal]:
            return self.dot(other)
        else:
            return self.scalar(other)

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


