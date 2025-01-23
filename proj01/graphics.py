#!/usr/bin/python3

# G. W. Prielipp (m265112)
import numpy

import math

from dataclasses import dataclass

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

    # returns a normal (aka a Vector3D with magnitude = 1)
    def normalize(self):
        return Normal(self.v.copy())

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
            # I'm pretty certain a Normal should always have a magnitude of 1
            mag = numpy.sqrt((self.v * self.v).sum())
            self.v = self.v / mag
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

    # cross product of a normal (like a Vector3D)
    def cross(self, other: 'Normal'):
        if not type(other) in [Vector3D, Normal]:
            raise Exception(f'Cannot take the cross product of a Normal and a {str(type(other))}')
        return Normal(numpy.cross(self.v, other.v))

    # scalar multiply a Normal
    def scalar(self, other):
        if type(other) in scalars:
            return Vector3D(self.v * other)
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
    def isPerpendicularTo(self, vec: Vector3D):
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
   
    # allow a ColorRGB to be unpacked into it's R,G,B components
    # notation would be: r,g,b = ColorRGB(...)
    def __iter__(self):
        return iter((self.v))

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
    def __add__(self, color: 'ColorRGB'):
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
    def __truediv__(self, scalar: scalars):
        if not type(scalar) in scalars:
            raise Exception(f'Cannot divide a ColorRGB by a {type(other)}')
        elif scalar == 0:
            raise Exception('Cannot divide by zero')
        return ColorRGB(self.v / scalar)
       
    # raise the individual color values to the value of the float
    def __pow__(self, val: scalars):
        # I know that it says has to be by a float in the definition ... (why can't I have an int here?)
        if not type(val) in scalars:
            raise Exception(f'Cannot raise a ColorRGB to the power of {type(other)}')
        return ColorRGB(self.v ** val)

# simple object to define what a Hit looks like
# the other option would be a namedtuple from collections
# or just making a super simple class
@dataclass
class Hit:
    isHit: bool
    t: numpy.float64 or float
    point: Point3D
    color: ColorRGB
    
    # define string representation of this object
    def __repr__(self):
        if self.isHit:
            return f'Hit: {str(self.t)} -> {str(self.point)}\tcolor = {str(self.color)}'
        else:
            return 'No Hit'
    def __str__(self):
        return repr(self)

    # allows a list of Hit's to be sorted
    # compare all Hits based on t value
    def __lt__(self, other: 'Hit'):
        ret = None
        
        if self.t != None and other.t != None:
            ret = self.t < other.t
        else:
            ret = self.t != None and other.t == None
        
        return ret

# a 2D Plane from a given origin and Normal
class Plane:
    def __init__(self, point: Point3D, normal: Normal, color: ColorRGB=ColorRGB(1,1,1)):
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

    # this should return a Hit object to follow OOP standards
    # returns: (BOOLEAN, FLOAT, Point3D, ColorRGB)
    #           is hit,   t   ,intersect, pane color
    def hit(self, ray: Ray, epsilon=0.000001, shadeRec=False):
        if ray.isPerpendicularTo(self.normal):
            return Hit(False, None, None, None)

        t = ((self.point - ray.getOrigin()) * self.normal) / (ray.getDirection() * self.normal)
        
        t = t if t > epsilon else 0.0

        return Hit(True, t, ray.pointAlong(t), self.color.copy())

# 3D sphere
class Sphere:
    def __init__(self, center: Point3D, radius: float, color: ColorRGB=ColorRGB(1,1,1)):
        self.center = center
        self.radius = radius
        self.color = color

    # create a new Sphere with the same properties
    def copy(self):
        return Sphere(self.center.copy(), self.radius, self.color.copy())

    # create the string representation of a sphere in format: [center, radius]
    def __repr__(self):
        return f'[{str(self.center)}, {self.radius}]'
    def __str__(self):
        return repr(self)

    # calculate the spots hit by a ray (if it does hit)
    def hit(self, ray: Ray, epsilon: float=0.000001, shadeRec: bool = False):
        rayd = ray.getDirection()
        orig = ray.getOrigin()
        cent = self.center
        radi = self.radius

        # calc at**2 + bt + c = 0
        a = rayd * rayd
        b = 2.0 * ((orig - cent) * rayd)
        c = (orig - cent) * (orig - cent) - radi**2

        # discriminant:
        d = b**2 - 4.0*a*c
        
        # d is negative => sqrt(d) = constant * i
        if d < 0:
            return [Hit(False, None, None, None)]
        # d = 0
        elif d == 0: 
            t = (-b) / (2.0 * a)
            
            # removed t == -0.0 # having weird issue
            if abs(t) <= epsilon:
                t = 0.0

            return [Hit(True, t, ray.pointAlong(t), self.color.copy())] 
        # d > 0
        else: 
            d = numpy.sqrt(d)
            t1 = (-b + d) / (2.0 * a)
            t2 = (-b - d) / (2.0 * a)
            
            t1 = t1 if abs(t1) > epsilon else 0.0
            t2 = t2 if abs(t2) > epsilon else 0.0
            
            return [Hit(True, t1, ray.pointAlong(t1), self.color.copy()), Hit(True, t2, ray.pointAlong(t2), self.color.copy())]

# ViewPlane is a non-orthographic (ray tracing) projection of the environment
class ViewPlane:
    def __init__(self, center: Point3D, normal: Normal, hres: int, vres: int, pixelsize: scalars):
        self.center = center
        self.normal = normal
        self.hres = hres
        self.vres = vres
        self.scale =  pixelsize
        
        # what is "displayed" to the physical screen 
        self.screen = [[ColorRGB(0,0,0) for col in range(self.hres)] for row in range(self.vres)]

        # compute unit vectors and lower left corner
        self.__initVectors()

    # compute the 3D unit vectors and the lower left corner
    def __initVectors(self):
        Vup = Vector3D(0,-1,0)
        # x-axis unit vector
        self.u = Vup.cross(-self.normal)
        
        # y-axis unit vector (should be unit vector from cross product already)
        self.v = self.u.cross(-self.normal)

        # normal = z-axis unit vector
        
        # calculate the lower left cell (lower left corner of that cell specifically)
        self.lowerLeft = self.center - self.u * self.hres * self.scale / 2.0 - self.v * self.vres * self.scale / 2.0
        # offset the lower left point to be the center of the cell
        #self.lowerLeft = self.lowerLeft + self.u * 0.5 + self.v * 0.5 

        # print the axis' for debugging
        #print(f'x: {str(self.u)}   y: {str(self.v)}   z: {str(self.normal)}')

    # returns the current color at a given pixel(row, col)
    def get_color(self, row: int, col: int):
        return self.screen[row][col]
    
    # set a pixel's color
    def set_color(self, row: int, col: int, color: ColorRGB):
        self.screen[row][col] = color

    # get the center point for given pixel
    def get_point(self, row: int, col: int):
        # because lowerLeft is at the center of the cell, all further offsets in relation to that will be the center of the cell
        return self.lowerLeft + self.u * col * self.scale + self.v * row * self.scale
    
    # returns the resulotion (width, height)
    def get_resolution(self):
        return (self.hres, self.vres)

    # get a Ray from a specific point with the same direction as the normal
    def orthographic_ray(self, row: int, col: int):
        origin = self.get_point(row, col)
        return Ray(origin, self.normal)

    # get a ray with a specific perspective from a camera
    def perspective_ray(self, row: int, col: int, cameraOrigin: Point3D):
        origin = self.get_point(row, col)
        return Ray(origin, (origin - cameraOrigin).normalize())

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


