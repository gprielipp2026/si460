def test(name, val, exp):
    print(f'Testing {name}...',end='\t')
    if val != exp:
        print(f'\033[0;31mFailed\033[0m\texpected: {exp}\treceived: {val}')
    else:
        print('\033[0;32mPassed\033[0m')

class TestVector:
    def __init__(self):
        from graphics import Vector3D
        self.u = Vector3D(1,2,3)
        self.v = Vector3D(4,5,6)
        self.c = 2.0

    def run(self):
        print("Testing Vector3D:")
        u = self.u
        v = self.v
        c = self.c

        test('Printing', str(u), '[1. 2. 3.]')
        test('Addition', str(u + v), '[5. 7. 9.]')
        test('Subtraction', str(u - v), '[-3. -3. -3.]')
        test('Scalar Multiplication', str(u * c), '[2. 4. 6.]')
        test('Magnitude', str(round(u.magnitude(), 4)), '3.7417')
        test('Square', str(int(u.square())), '14')
        test('Cross', str(u.cross(v)), '[-3.  6. -3.]')
        print()

class TestPoint:
    def __init__(self):
        from graphics import Point3D, Vector3D
        self.a = Point3D(3,4,5)
        self.b = Point3D(0,0,1)
        self.u = Vector3D(3,6,9)
        self.c = 5.0

    def run(self):
        print("Testing Point3D:")
        a = self.a
        b = self.b
        u = self.u
        c = self.c

        test('Printing', str(a), '[3. 4. 5.]')
        test('Addition', str(a + u), '[ 6. 10. 14.]')
        test('Point-Vector Subtraction', str(a - u), '[ 0. -2. -4.]')
        test('Point-Point Subtraction', str(a - b), '[3. 4. 4.]')
        test('Distance Squared', str(a.distancesquared(b)), '41.0')
        test('Distance', str(round(a.distance(b), 4)), '6.4031')
        test('Copy', str(a.copy()), '[3. 4. 5.]')
        test('Scalar Multiplication', str(a * c), '[15. 20. 25.]')
        print()

class TestNormal:
    def __init__(self):
        from graphics import Normal, Vector3D, Point3D
        self.v = Vector3D(1,2,3)
        self.u = Vector3D(4,5,6)
        self.a = Point3D(1,3,5)
        self.b = Point3D(2,5,6)
        self.n = Normal(5,3,1)
        self.m = Normal(6,4,2)
        self.c = 2.0

    def roundNDArray(self, arr):
        import numpy
        return numpy.array([x for x in map(lambda y: round(y, 4), arr)])
    
    def run(self):
        print('Testing Normal')
        v, u, a, b, n, m, c = self.v, self.u, self.a, self.b, self.n, self.m, self.c

        test('Printing', str(self.roundNDArray(n.v)), '[5. 3. 1.]')
        test('Normal + Normal', str(self.roundNDArray((n + m).v)), '[11.  7.  3.]')
        test('Normal.dot(Vector3D)', str(round(n.dot(u), 4)), '41.0')
        test('Scalar Multiplication', str(self.roundNDArray((n*c).v)), '[10.  6.  2.]')
        test('Normal + Vector3D', str( self.roundNDArray((n + u).v) ), '[9. 8. 7.]')
        test('Vector3D + Normal', str( self.roundNDArray((u + n).v) ), '[9. 8. 7.]')

        print()


class TestSphere:
    def __init__(self):
        pass

    def run(self):
        from graphics import Sphere, Point3D, Vector3D, Ray, Hit, ColorRGB 

        print('Testing Sphere')

        s = Sphere(Point3D(0,0,20), 10.0)
        d = Vector3D(0,0,1)
        
        os = [Point3D(0,0,0), Point3D(0,10,0), Point3D(0,20,0), Point3D(0,0,20), Point3D(0,10,20), Point3D(0,0,40)]
        c = ColorRGB(1,1,1)
        exps = [[Hit(True, 10.0, Point3D(0,0,10), c), Hit(True, 30.0, Point3D(0,0,30), c)], \
                [Hit(True, 20.0, Point3D(0,10,20), c)], \
                [Hit(False, None, None, None)], \
                [Hit(True, -10.0, Point3D(0,0,10), c), Hit(True, 10.0, Point3D(0,0,30), c)], \
                [Hit(True, 0.0, Point3D(0,10, 20), c)], \
                [Hit(True, -30.0, Point3D(0,0,10), c), Hit(True, -10.0, Point3D(0,0,30), c)]]

        for o, exp in zip(os, exps):
            r = Ray(o, d)
            res = s.hit(r)
            res.sort()
            test(f'Ray: {str(r)} -> Sphere: {str(s)}', str(res), str(exp)) 
        
        print()


class TestViewPlane:
    def __init__(self):
        pass

    def run(self):
        from graphics import ViewPlane, Point3D, Normal
        
        print('Testing ViewPlane')

        vp = ViewPlane(Point3D(0,0,0), Normal(0,0,1), 640, 480, 1.0)
        print(str(['debug 1',0,0,vp.get_point(0,0)]))
        print(str(['debug 2',479,639,vp.get_point(479,639)]))
        
        print()

