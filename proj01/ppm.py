# George Prielipp (265112)
# writes a ViewPlane into a ppm file
from graphics import ViewPlane
def PPM(view: ViewPlane, fn: str):
    file = open(fn, 'w')

    try:
        # writing in PPM style:
        file.write('P3\n')

        width, height = view.get_resolution()
        
        # shows the size of the image
        file.write(f'{width} {height}\n')
        # max color value
        file.write('255\n')
        
        # ViewPlane 0,0 is Lower Left
        # PPM 0,0 is Top Left
        # i.e. left->right is good, top->bottom is inverted
        for row in range(height-1, -1, -1):
            for col in range(0, width):
                r,g,b = [int(x * 255) for x in view.get_color(row, col)]
                file.write(f'{r} {g} {b}' + (' ' if col != width-1 else '\n'))
                

    except Exception as e:
        print(f'PPM Error: {e}')
        file.close()
    finally:
        file.close()

if __name__ == '__main__':
    import graphics as g

    myViewPlane = g.ViewPlane(g.Point3D(0,0,0), g.Normal(0,0,1), 3, 4, 1)
    myViewPlane.set_color(0,0,g.ColorRGB(1,1,1))
    myViewPlane.set_color(0,2,g.ColorRGB(1,0,0))
    myViewPlane.set_color(1,1,g.ColorRGB(1,0,1))
    myViewPlane.set_color(1,2,g.ColorRGB(1,1,0))
    myViewPlane.set_color(3,0,g.ColorRGB(0,1,0))
    myViewPlane.set_color(3,2,g.ColorRGB(0,0,1))

    PPM(myViewPlane, 'part3-testing.ppm')
