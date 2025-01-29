#!/usr/bin/python3 -B

from graphics import Vector3D, Point3D, Normal, Ray, Plane, Sphere, ViewPlane

##### Problem Set 1 #####

# Create a viewplane with center 0,0,0 and normal 0.2, 0.4, 0.6, width 1920, 
# height 1080, scaling factor 1
myViewingPlane = ViewPlane(Point3D(0,0,0), Normal(0.2, 0.4, 0.6), 1920, 1080, 1) 

# What is the value for u, v, and the lower left coordinates?
print('u:  ', myViewingPlane.u)
print('v:  ', myViewingPlane.v)
print('LL: ', myViewingPlane.lowerLeft)

# What is the value for the ray origin point at row 5, column 10
myRayOrigin = myViewingPlane.get_point(5, 10)
print('location of the origin of the ray based on the row and col', myRayOrigin)

# By the way what is the direction vector of the ray that you will create?  
# Based off of the viewing plane?
myRayDirection = ...  # Fill in the blank

# How would you create a Ray object from these?

##### Problem Set 2 ######

# Create a ray with origin at 0,0,0 and going in the direction of 1,0,0
r1 = Ray(Point3D(0,0,0), Vector3D(1,0,0))

# create a sphere with center 20,5,0 and radius 10
s1 = Sphere(Point3D(20,5,0), 10)

# create a plane with point 50,50,0 and normal 0.2, 0.2, 0.2
p1 = Plane(Point3D(50,50,0), Normal(0.2, 0.2, 0.2))

# Draw the ray (r1), the sphere (s1), and the plane (p2) on paper or the board

# Solve for the hitpoint between the ray and the sphere
hitcheck, t, poi, color = s1.hit(r1, 0.000001)
print('Sphere, We found an intersection?', hitcheck)
print('The value for t at the intersection: ', t)
print('The point of intersection: ', poi)

# Solve for the hitpoint between the ray and the plane
hitcheck, t, poi, color = p1.hit(r1, 0.000001)
print('Plane, We found an intersection?', hitcheck)
print('The value for t at the intersection: ', t)
print('The point of intersection: ', poi)


