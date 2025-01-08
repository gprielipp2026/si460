#!/usr/bin/env python3

import sys

def isprime(x: int) -> bool:
    f  = 2
    while f < 512:
        if x % f == 0 and x != f:
            return False
        f += 1

    return True


def usage():
    print("usage: isprime.py ###")
    sys.exit(0)

if len(sys.argv) != 2:
    usage()
   

x = None
try:
    x = int(sys.argv[1])
except:
    print(f'"{x}" is not an integer')
    sys.exit(1)

if x < 512:
    print("Prime!" if isprime(x) else "Not Prime!")
else:
    print("Choose a number less than 512")
