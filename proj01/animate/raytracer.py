#!/usr/bin/env python3

from graphics import *

def getMinTHit(hits: list[Hit]):
    # sort ascending based on t values
    hits.sort()
    # find first positive t 
    for hit in hits:
        if hit.isHit and hit.t >= 0:
            return hit
    # no hit in front of the viewplane was good:
    return Hit(False, None, None, ColorRGB(0,0,0))

def orthoRayTrace(view: ViewPlane, objs):
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

def perspectiveRayTrace(view: ViewPlane, objs, camera: Ray):
    width, height = view.get_resolution()
    
    # iterate through and cast a ray for each pixel
    for row in range(0, height):
        for col in range(0, width):
            ray = view.perspective_ray(row, col, camera)
            
            hits = []
            for obj in objs:
                hit = obj.hit(ray)
                if isinstance(hit, list):
                    hits.extend(hit)
                else:
                    hits.append(hit)

            closestHit = getMinTHit(hits)
            view.set_color(row, col, closestHit.color)

