import numpy as np
import random
import pyglet
from pyglet.gl import *
from math import sin, cos, pi

class Particle:
    def __init__(self, origin=np.array([0.0,0.0,0.0], dtype='float64'), 
                       velocity=np.array([0.0,0.0,0.0], dtype='float64'), 
                       acceleration=np.array([0.0,-9.8,0.0], dtype='float64')):
        self.origin = origin
        self.velocity = velocity
        self.acceleration = acceleration
        self.onBottom = False

    def reflect(self, N, V):
        projVonN = (np.dot(V,N) / np.dot(N, N)) * N
        return V - 2.0 * projVonN

    def inbox(self, sidelen):
        # has the side effect of reflecting the velocity based on which wall it hits
        sidelen /= 2.0
        x, y, z = self.origin
        retval = True

        ## left plane
        ## right plane
        if x <= -sidelen or x >= sidelen:
            #print(f'{x:.2f}, {y:.2f}, {z:.2f}', sidelen)
            self.velocity = self.reflect(np.array([x/abs(x),0,0],dtype='float64'), self.velocity)
            retval = False

        ## top plane
        ## bottom plane
        if y <= -sidelen or y >= sidelen:
            #print(f'{x:.2f}, {y:.2f}, {z:.2f}', sidelen)
            self.velocity = self.reflect(np.array([0,y/abs(y),0],dtype='float64'), self.velocity)
            if y <= -sidelen:
                self.onBottom = True
                x,y,z = self.velocity
                self.velocity = np.array([x,0,z], dtype='float64')
                self.acceleration = np.array([0,0,0], dtype='float64')
                x,y,z = self.origin
                self.origin = np.array([x,-sidelen+0.01,z], dtype='float64')
            retval = False

        ## front plane
        ## back plane
        if z <= -sidelen or z >= sidelen:
            #print(f'{x:.2f}, {y:.2f}, {z:.2f}', sidelen)
            self.velocity = self.reflect(np.array([0,0,z/abs(z)],dtype='float64'), self.velocity)
            retval = False

        return retval 

    def update(self, dt, sidelen):
        # P_i = P_0 + V_0*t + a * t^2 / 2
        if self.onBottom:
            if abs(np.linalg.norm(self.velocity)) <= 0.1:
                return
            # apply friction
            self.acceleration = -0.3 * self.velocity
        
        newpos = self.origin + self.velocity * dt + self.acceleration * pow(dt, 2) * 0.5
        newvel = self.velocity + self.acceleration * dt 
        
        if self.inbox(sidelen):
            self.origin = newpos
            self.velocity = newvel
        else:
            self.origin = self.origin + self.velocity * dt + self.acceleration * pow(dt, 2) * 0.5
            

    def getPos(self):
        return self.origin
    
    @staticmethod
    def rand():
        maxTheta = 60 * pi / 180.0
        maxPhi = 2.0 * pi
    
        speed = 90.0
        randArr = lambda: np.array([0,0,0])#np.array([random.uniform(-100,100) for _ in range(3)], dtype='float64')
        randVel = lambda theta, phi: np.array([sin(theta)*sin(phi), cos(theta), sin(theta)*cos(phi)], dtype='float64')*speed*(1-pow(theta/maxTheta, 2))
        randAngle = lambda lb,ub: random.uniform(lb, ub)
        randParticle = lambda: Particle(origin=randArr(), velocity=randVel(randAngle(0,maxTheta), randAngle(0,maxPhi)))
        
        return randParticle()

    def draw(self, dt):
        glBegin(GL_TRIANGLE_FAN)
   
        # make a coord system
        vup = np.array([0,1,0], dtype='float64')
        if abs(np.linalg.norm(self.velocity)) > 0.0:
            norm = self.velocity / np.linalg.norm(self.velocity)
        else:
            norm = np.array([0,0.99999,0], dtype='float64')
        
        tmp = np.cross(vup, -norm)
        u = tmp / np.linalg.norm(tmp)
        tmp = np.cross(u, -norm)
        v = tmp / np.linalg.norm(tmp)

        # norm = "up"
        # u = "x axis"
        # v = "y axis"

        pointAt = lambda x,y,z: self.getPos() + u * x + v * y + norm * z
        scale = 10
        scaleSQRD = pow(scale, 2)
        h = np.sqrt(scaleSQRD + scaleSQRD/4.0)

        # 0
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glVertex3f(*pointAt(0,0,0))
        
        # 1
        glColor4f(1.0, 0.0, 0.0, 1.0)
        glVertex3f(*pointAt(-scale,-scale, -h))
        
        # 2
        glColor4f(0.0, 1.0, 0.0, 1.0)
        glVertex3f(*pointAt(-scale,scale, -h))
        
        # 3
        glColor4f(0.0, 0.0, 1.0, 1.0)
        glVertex3f(*pointAt(scale,0,-h))
        
        # 1
        glColor4f(1.0, 0.0, 0.0, 1.0)
        glVertex3f(*pointAt(-scale,-scale, -h))

        glEnd()


class ParticleArray:
    def __init__(self, numParticles=10, tlag=random.uniform(0,60)):
        self.numParticles = numParticles
        self.particles = []
        tlag = 1
        pyglet.clock.schedule_interval(self.addParticle, tlag)
    
    def addParticle(self, *args):
        #if len(self.particles) >= self.numParticles:
            #self.particles.pop(0)
        self.particles.append(Particle.rand())



    def draw(self, dt, sidelen):
        for particle in self.particles:
            particle.update(dt,sidelen)
            particle.draw(dt)
        
