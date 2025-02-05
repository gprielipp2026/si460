#!/usr/bin/env python3

from graphics import *
from ppm import PPM
from world_objects import getObjects
from raytracer import orthoRayTrace
from math import sin, cos, pi

world = getObjects()

# the circle to spin the view plane about
center = Point3D(0,60,400)
radius = 600

# return the view plane shifted counter-clockwise by angle on the z-axis
def update(view, angle):
    global center, radius
    x, y, z = radius * cos(angle), 0.0, radius * sin(angle)
    pointOnCircle = Vector3D(x,y,z)
    pointInSpace = center + pointOnCircle 
    
    view.center = pointInSpace
    
    planeToCenter = pointInSpace - center

    view.normal = planeToCenter.normalize()


# rotate the plane around the scene and generate images
angle = 0.0
view = ViewPlane(Point3D(0,0,0), Normal(0,0,1), 400, 400, 1.0)

# how many times to run
numFrames = 60
deltaAngle = 2.0 * pi / float(numFrames)

for i in range(numFrames):
    print(f'Making frame-{str(i+1) if i + 1 >= 10 else '0'+str(i+1)}.ppm', end='\r')
    # figure out where the frame should be
    update(view, angle) 
    # capture the image
    orthoRayTrace(view, world)
    # record the image
    PPM(view, f'frames/frame-{str(i+1) if i + 1 >= 10 else '0'+str(i+1)}.ppm')
    # update the angle
    angle += deltaAngle
print()
print('All Done!')

