#!/usr/bin/env python3

from graphics import *

def getDir(point, origin):
    d = point - origin
    d = d / d.magnitude()
    return d

def findSol(point, origin, plane2):
    ray = Ray(origin, getDir(point, origin))
    
    return (ray.getDirection(), plane2.hit(ray))

plane2 = Plane(Point3D(0,0,20), Normal(0,0,1))
origin = Point3D(0,0,0)
testPoints = [Point3D(1,1,5), Point3D(1,2,5), Point3D(2,1,5), Point3D(2,2,5)]

for point in testPoints:
    print(findSol(point, origin, plane2))
