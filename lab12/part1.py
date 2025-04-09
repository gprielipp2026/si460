#!/usr/bin/python3 -B

import makeTopoMap
M = makeTopoMap.get_matrix(rows=100, cols=60, seed=3)

def march(M, threshold):
  rows, cols = M.shape
  upperX = -cols / 2.0    # X coordinate of the first item in the matrix
  upperY =  rows / 2.0    # Y coordinate of the first item in the matrix
  results = []

  lerp = lambda x, lx, rx, nl, nr: ( (float(x) - lx) / (rx - lx) ) * ( nr - nl ) + nl 

  percent = lambda a, b, t: ( t - a ) / ( b - a ) if abs(b - a) > 0 else -1.0

  A = 0b1000
  B = 0b0100
  C = 0b0010
  D = 0b0001

  for row in range(rows-1):
    for col in range(cols-1):
      a = M[row  ][col  ] # value of a
      b = M[row  ][col+1] # value of b
      c = M[row+1][col+1] # value of c
      d = M[row+1][col  ] # value of d
      ax = upperX + col # x coordinate of a, Hint: use upperX and col to calculate this
      ay = upperY - row # y coordinate of a, Hint: use upperY and row to calculate this
      
      pcase  = 0
      points = []
      #if a >= threshold and b <= threshold:  #( the threshold is between a, b):
      if 1.0 > percent(a, b, threshold) > 0.0:
        px = lerp(threshold, a, b, ax, ax + 1) # x coordinate of the interpolated position between a and b
        py = ay                                # y coordinate of the interpolated position between a and b
        pcase |= (A if a > b else B if b > a else (A | B))
        points.append((px,py))
      #if b >= threshold and c <= threshold: # ( the threshold is between b, c):
      if 1.0 > percent(b, c, threshold) > 0.0:
        px = ax + 1                            # x coordinate of the interpolated position between b and c
        py = lerp(threshold, b, c, ay, ay - 1) # y coordinate of the interpolated position between b and c
        pcase |= (B if b > c else C if c > b else (B | C))
        points.append((px,py))
      #if c >= threshold and d <= threshold: # ( the threshold is between c, d):
      if 1.0 > percent(c, d, threshold) > 0.0:
        px = lerp(threshold, c, d, ax + 1, ax) # x coordinate of the interpolated position between c and d
        py = ay - 1                            # y coordinate of the interpolated position between c and d
        pcase |= (C if c > d else D if d > c else (C | D))
        points.append((px,py))
      #if d >= threshold and a <= threshold: # ( the threshold is between d, a):
      if 1.0 > percent(d, a, threshold) > 0.0:
        px = ax                                # x coordinate of the interpolated position between d and a
        py = lerp(threshold, d, a, ay - 1, ay) # y coordinate of the interpolated position between d and a
        pcase |= (D if d > a else A if a > d else (D | A))
        points.append((px,py))
      if points != []:
        # somehow pcase == 5 without 4 points ?
        if pcase == 5 and len(points) == 4: # want the lines to separate A from C
          # right now the points define lines separating B from D
          points[1], points[3] = points[3], points[1]
        # case 10 seems to be doing fine, leave as is for now
        results.append((pcase,points))
  
  return results
