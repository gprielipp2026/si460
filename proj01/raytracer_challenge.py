#!/usr/bin/env python3

from graphics import Sphere, Plane, Point3D, Normal, ColorRGB, Hit, ViewPlane, Ray
from ppm import PPM

# Build the Spheres that will be in our world
S1 = Sphere(Point3D(300,200,200), 100, ColorRGB(1.0,0.2,0.4))
S2 = Sphere(Point3D(-200,-100,50), 35, ColorRGB(0.3,0.8,0.2))
S3 = Sphere(Point3D(50,20,100), 25, ColorRGB(0.4,0.1,0.4))
S4 = Sphere(Point3D(300,-200,600), 250, ColorRGB(0.6,0.6,0.4))
S5 = Sphere(Point3D(400,400,900), 400, ColorRGB(0.0,0.2,1.0))

# Build the Planes that will be in our world
P1 = Plane(Point3D(50,50,999), Normal(0,0,1), ColorRGB(0.8,0.8,0.8))
P2 = Plane(Point3D(50,50,900), Normal(1,1,1), ColorRGB(1.0,1.0,1.0))

# It would make sense to put all of your objects into an array
# so that you can iterate through them.  Here is our observable world:
obs = [S1,S2,S3,S4,S5,P1,P2]

def getMinTHit(hits: list[Hit]):
    # sort ascending based on t values
    hits.sort()
    # find first positive t 
    for hit in hits:
        if hit.t >= 0:
            return hit
    # no hit in front of the viewplane was good:
    return Hit(False, None, None, ColorRGB(0,0,0))

def rayTrace(view: ViewPlane, objs, camera):
    width, height = view.get_resolution()

    # iterate through and cast a ray for each pixel
    for row in range(height-1, -1, -1):
        for col in range(0, width):
            ray = view.perspective_ray(row, col, camera.getOrigin())
            hits = []
            for obj in objs:
                hit = obj.hit(ray)
                if isinstance(hit, list):
                    hits.extend(hit)
                else:
                    hits.append(hit)

            closestHit = getMinTHit(hits)
            view.set_color(row, col, closestHit.color)


view = ViewPlane(Point3D(0,0,0), Normal(0,0,1), 640, 480, 1.0)

cameras = [\
           Ray(Point3D(0,0,-100), Normal(0,0,1)),\
           Ray(Point3D(0,0,-1000), Normal(0,0,1)),\
           Ray(Point3D(-100,-100,-30), Normal(0,0,1))]

# going to just bruteforce it because why not (ie no multi-threading/processing)

for i,camera in enumerate(cameras):
    rayTrace(view, obs, camera)
    PPM(view, f'part6-{i+1}.ppm')


