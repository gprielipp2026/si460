#!/usr/bin/python3
from tile import Tile

# allows a user to define a landmass
class Landmass(Tile):
    def __init__(self, matrix, left, top):
        """
        EXAMPLE:
        [
        [1,1,0,0,0,0]
        [1,1,1,1,1,0]
        [1,1,1,1,1,0]
        ]
        """
        base = lambda x: f'mylevel/tiles/{x}.png' if x is not None else ''
        
        # apply the filters and get back which images belong at what "pixel" in the matrix
        images = self.classify(matrix)
       

        # apply the base to figure out the exact filepath
        for row in range(len(images)):
            for col in range(len(images[row])):
                images[row][col] = base(images[row][col])
        
        for row in images:
            while '' in row:
                row.remove('')
        
        super().__init__(images, left, top)
    
    # turns ['u1', 'm2'] into 'um'
    def fix(self, items):
        if len(items) == 0:
            # must be an air block
            return None

        if 'cr' in items:
            return 'cr'
        elif 'cl' in items:
            return 'cl'
        elif 'wr' in items:
            return 'wr'
        elif 'wl' in items:
            return 'wl'

        result = list(items[0])
        for item in items:
            if '1' in item:
                result[0] = item[0]
            elif '2' in item:
                result[1] = item[0]
        return ''.join(result)
    
    # applies all of the filters and returns all of those that work
    def apply(self, filters, matrix, row, col):
        result = []

        for name, func in filters.items():
            isGood = True
            for dy in range(-1,2):
                for dx in range(-1,2):
                    #       col    +   row    * height
                    idx = (1 + dx) + (1 + dy) * 3
                    # don't care about this
                    if func[idx] == 'x':
                        continue
                    else:
                        isGood = isGood and str(matrix[row+dy][col+dx]) == func[idx]
            if isGood:
                result.append(name)
        return result

    # expand the left, right, top, and bottom of a matrix
    def expand(self, matrix):
        # items on the left/right bound get copied
        # items on the top/bottom bound get padded by '0'
        for row in range(len(matrix)):
            matrix[row].insert(0, matrix[row][0])
            matrix[row].append(matrix[row][-1])
        matrix.insert(0, [0 for _ in range(len(matrix[0]))])
        matrix.append(matrix[-1])
        return matrix

    # classifies each pixel
    def classify(self, matrix):
        """
        str '123456789'
        is matrix:
        1 2 3
        4 5 6
        7 8 9
        """
        
        # the different filters
        up = '000x1xxxx' 
        m1 = 'x1xx1xx1x' 
        m2 = 'xxx111xxx'
        le = 'xxx01xxxx'
        ri = 'xxxx10xxx'
        lo = 'xxxx1x000'
        cr = '110111xxx'
        cl = '011111xxx'
        wl = '100111xxx'
        wr = '001111xxx'
        filters = {'u1': up, 'm1': m1, 'm2': m2, 'l2': le, 'l1': lo,\
                'r2': ri, 'cl': cl, 'cr': cr, 'wl': wl, 'wr': wr}
       
        result = [ [None] * len(matrix[i]) for i in range(len(matrix))]

        # provide buffer space
        # now indices are 1 -> len(matrix)-2
        matrix = self.expand(matrix)
       
        # apply the filters
        for row in range(1, len(matrix)-1):
            for col in range(1, len(matrix[row])-1):
                # would return ['u1', 'm2'] for an um pixel
                pixel = self.apply(filters, matrix, row, col)
                # takes ['u1', 'm2'] => 'um'
                result[row-1][col-1] = self.fix(pixel)
        return result

if __name__ == '__main__':
    body = [
            [1,1,0,0,0,0,0,0],
            [1,1,1,1,1,1,0,0],
            [1,1,1,1,1,1,0,0],
            ] 
    tiles = Landmass(body, 0, 0) 

objects = [Landmass([[1,1,0,0,0,0,0,0],[1,1,1,1,1,1,0,0],[1,1,1,1,1,1,0,0]], 0, 216)]
