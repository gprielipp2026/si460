#!/usr/bin/env python3

from abc import ABC, abstractmethod

class Entity(ABC):

    @abstractmethod
    def save(self, file, tabs=0):
        pass

class KML:
    def __init__(self, fn):
        self.filename = fn
        self.entities = []

    def addEntity(self, entity: Entity):
        self.entities.append(entity)

    def saveKML(self):
        file = open(self.filename, 'w')
        
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        file.write('<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">\n')
        file.write('<Document>') 
       
        for entity in self.entities:
            entity.save(file, 1)
        
        file.write('</Document>') 
        file.write('</kml>')

        file.close()


class Placemark(Entity):
    def __init__(self, ID=0, *attrs):
        self.id = ID
        self.attrs = [*attrs]

    def save(self, file, tabs=0):
        indent = '\t'*tabs
        file.write(f'{indent}<Placemark id="{self.id}">\n')

        for attr in self.attrs:
            attr.save(file, tabs+1)

        file.write(f'{indent}</Placemark>\n')

class SimpleAttr(Entity):
    def __init__(self, key, value):
        self.key = key
        self.val = value

    def save(self, file, tabs=0):
        indent = '\t'*tabs
        line = f'{indent}<{self.key}>{self.val}</{self.key}>\n'
        file.write(line)

class Point(Entity):
    def __init__(self, coords):
        coords = [coord[1:] if '+' in coord else coord for coord in coords]
        self.lat = coords[0]
        self.lon = coords[1]

    def save(self, file, tabs=0):
        indent = '\t'*tabs
        indent1more = '\t'*(tabs+1)

        coordline = f'{indent1more}<coordinates>{self.lon},{self.lat},0</coordinates>\n'
        
        file.write(indent+'<Point>\n')
        file.write(coordline)
        file.write(indent+'</Point>\n')

