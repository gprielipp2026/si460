#!/usr/bin/env python3

from graphics import *

def pointRayIntersectPlane(ray, plane):
    t = ((plane.point - ray.origin) * plane.normal) / (ray.direction * plane.normal)
    # t = 1.8 
    print(f'{t=}')
    # p = o + d * t; because the builtin type for t (float/int) does not define multiplication with a Vector3D
    return ray.origin + ray.direction * t


print('Point:',pointRayIntersectPlane( Ray(Point3D(1,1,-10), Vector3D(2,2,4)), Plane(Point3D(2,4,2), Normal(-3,-3,-2)) ))


