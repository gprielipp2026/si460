#!/usr/bin/env python3

"""
George Prielipp 265112
Vector.py
implementation of basic mathmatical vector operations
"""

import math

from typing import Union

numeric = Union[int, float]

class Vector3D:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'

    def __add__(self, other: 'Vector3D') -> 'Vector3D':
        newx = self.x + other.x
        newy = self.y + other.y
        newz = self.z + other.z

        return Vector3D(newx, newy, newz)

    def __sub__(self, other: 'Vector3D') -> 'Vector3D':
        newx = self.x - other.x
        newy = self.y - other.y
        newz = self.z - other.z

        return Vector3D(newx, newy, newz)

    def dot(self, other: 'Vector3D') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z 

    """
    assumes the angle is already in radians
    """
    def dotangle(self, other: 'Vector3D', angle: numeric, mode='RADIANS') -> float:
        if mode == 'DEGREES':
            angle = math.pi * angle / 180.0
        return self.magnitude() * other.magnitude() * math.cos(angle)

    def scalar(self, a: numeric) -> 'Vector3D':
        newx = self.x * a
        newy = self.y * a
        newz = self.z * a

        return Vector3D(newx, newy, newz)

    def __mul__(self, other: Union[numeric, 'Vector3D']) -> Union[float, 'Vector3D']:
        if isinstance(other, Vector3D):
            return self.dot(other)
        elif isinstance(other, numeric):
            return self.scalar(other)
        else:
            raise Exception("Somehow other is not numeric or a Vector3D")

    def __div__(self, a: numeric) -> 'Vector3D':
        newx = self.x / a
        newy = self.y / a
        newz = self.z / a

        return Vector3D(newx, newy, newz)

    def copy(self) -> 'Vector3D':
        return Vector3D(self.x, self.y, self.z)

    def magnitude(self) -> float:
        return math.sqrt(self.square())

    def square(self) -> float:
        return self.x * self.x + self.y * self.y + self.z * self.z
    
    def cross(self, other: 'Vector3D') -> 'Vector3D':
        ux,uy,uz = self.x, self.y, self.z
        vx,vy,vz = other.x, other.y, other.z

        newx = uy*vz - uz*vy
        newy = uz*vx - ux*vz
        newz = ux*vy - uy*vx

        return Vector3D(newx, newy, newz)


    def __setattr__(self, name, value):
        if not isinstance(value, numeric) and name in ['x','y','z']:
            raise Exception(f'Error: Wrong type - Cannot assign {name} to {value}')
        else:
            self.__dict__[name] = value



if __name__ == '__main__':
    u = Vector3D(0,0,0)
    v = Vector3D(1,0,1)

    print(u * v)
    print(v * 10)

    u.x = 3
    print(u)

    try:
        u.z = 'hi'
        print(u)
    except Exception as e:
        print(e)


