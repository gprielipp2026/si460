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
        if hit.isHit and hit.t >= 0:
            return hit
    # no hit in front of the viewplane was good:
    return Hit(False, None, None, ColorRGB(0,0,0))

# somehow this is faster ??
def rayTrace(view: ViewPlane, objs):
    width, height = view.get_resolution()
    
    # iterate through and cast a ray for each pixel
    for row in range(0, height):
        for col in range(0, width):
            ray = view.orthographic_ray(row, col)
            
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
        ViewPlane(Point3D(0,0,0), Normal(0,0,1), 200, 100, 1.0),\
        ViewPlane(Point3D(50,50,-50), Normal(0,0,1), 200, 100, 1.0),\
<<<<<<< HEAD
        ViewPlane(Point3D(50,50,-50), Normal(1,1,1), 200, 100, 1.0),\
=======
        ViewPlane(Point3D(50,50,-50), Normal(1,1,1), 200, 100, 1.00),\
>>>>>>> 435e5bdee0222e66d209bdafb22f3e5cd25e1c9e
        ViewPlane(Point3D(0,0,0), Normal(0,0,1), 640, 480, 1.0),\
        ViewPlane(Point3D(50,50,-50), Normal(-0.2,0,1), 200, 100, 1.0)\
        ]


for i,view in enumerate(views):
    rayTrace(view, obs)
    PPM(view, f'old_images/part5-{i+1}.ppm')
    print(f'Done with: part5-{i+1}.ppm')

