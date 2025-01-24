#!/usr/bin/env python3

from graphics import Sphere, Plane, Point3D, Normal, ColorRGB, Hit, ViewPlane, Ray
from ppm import PPM

# Build the Spheres that will be in our world
S1 = Sphere(Point3D(0,40,500), 40.0, ColorRGB(0.8, 0.0, 0.0))
S2 = Sphere(Point3D(0,100,500), 20.0, ColorRGB(0.0, 0.8, 0.0))
S3 = Sphere(Point3D(0,40,200), 60.0, ColorRGB(0.0, 0.0, 0.6))

# Build the Planes that will be in our world
P1 = Plane(Point3D(0,0,0), Normal(0,1,0), ColorRGB(0,0.9,0.4)) # "floor" x-z plane
P2 = Plane(Point3D(0,0,1000), Normal(0,0,-1), ColorRGB(0.8,0.8,0.8)) # back wall

# It would make sense to put all of your objects into an array
# so that you can iterate through them.  Here is our observable world:
obs = [S1,S2,S3,P1,P2]

def getMinTHit(hits: list[Hit]):
    # sort ascending based on t values
    hits.sort()
    # find first positive t 
    for hit in hits:
        if hit.isHit and hit.t >= 0:
            return hit
    # no hit in front of the viewplane was good:
    return Hit(False, None, None, ColorRGB(0,0,0))

# somehow this is faster ??
def rayTrace(view: ViewPlane, objs):
    width, height = view.get_resolution()
    
    # simulate "orthographic" view
    # produced the same images and the othrographic_ray
    #camera = Ray(view.getCenter() - view.getNormal()*100000.0, view.getNormal())

    # iterate through and cast a ray for each pixel
    for row in range(0, height):
        for col in range(0, width):
            ray = view.orthographic_ray(row, col)
            #ray = view.perspective_ray(row, col, camera.getOrigin())
            hits = []
            for obj in objs:
                hit = obj.hit(ray)
                if isinstance(hit, list):
                    hits.extend(hit)
                else:
                    hits.append(hit)

            closestHit = getMinTHit(hits)
            view.set_color(row, col, closestHit.color)


views = [\
        ViewPlane(Point3D(0,0,0), Normal(0,0,1), 640, 480, 1.0),\
        ViewPlane(Point3D(0,400,0), Normal(0,-0.5,1), 640, 480, 1.0),\
        ViewPlane(Point3D(0,0,400), Normal(0,0,1), 640, 480, 1.0),\
        ViewPlane(Point3D(0,100,500), Normal(0,-1,0), 640, 480, 1.0),
        ViewPlane(Point3D(0,200,200), Normal(0,-1,1), 640, 480, 1.0),\
        ViewPlane(Point3D(200,200,200), Normal(1,1,1), 640, 480, 1.0),\
        ViewPlane(Point3D(0,0,600), Normal(0,0,-1), 640, 480, 1.0)\
        ]

# going to just bruteforce it because why not (ie no multi-threading/processing)

for i,view in enumerate(views):
    rayTrace(view, obs)
    PPM(view, f'testing/part5-test-{i+1}.ppm')
    print(f'Done with: part5-test-{i+1}.ppm')

