# Prielipp (265112) Lab08 Submission

## Part 1

```text
Case 1:
- takes the cube over to the right and rotates it

Case 2:
- move the cube to the right, but the rotate moves it off axis, it ends up higher on the screen

Case 3:
- the cube remains in the center, but rotated and stretched

Case 4:
- the cube remains in the center, it appears slightly squished
```

## Part 2:

```text
a) matrix M for glTranslatef(...)
glTranslatef(0.0, 0.0, 20.0)
M = [
     [1.0  0.0  0.0  0.0]
     [0.0  1.0  0.0  0.0]
     [0.0  0.0  1.0 20.0]
     [0.0  0.0  0.0  1.0]
    ]

b) order of matrix multiplications for case 4
glTranslatef() * glScalef() * glRotatef()
```

## Part 3:

```text
glTranslatef(7.5, 7.5, 0.0)
glRotatef(45.0, 0.0, 0.0, 1.0)
glTranslatef(-7.5, -7.5, 0.0)
```

## Part 4:

```text
mag = 7.5
glTranslatef(-mag, 0.0, 0.0)
glTranslatef( mag, mag, 0.0)
glTranslatef( mag,-mag, 0.0)
glTranslatef(-mag,-mag, 0.0)
```


