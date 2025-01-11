#!/usr/bin/env python3

import sys

def usage():
    print("usage: ./fileread.py <filename>")
    sys.exit()

def separate(data: str) -> tuple:
    # find first non-digit
    i = 0
    while data[i].isdigit():
        i += 1

    return (data[:i], data[i:])

def getdata(line: str) -> str:
    a = 213
    b = 316 
    return line[a:b].strip() 

def parse(fn: str) -> list[tuple]:
    districts = []
    
    fd = open(fn, 'r')

    for line in fd.readlines():
        #line = list(filter(lambda x: x != '', line.split(' ') ))
        data = getdata(line)
        
        districts.append( separate(data) )

    fd.close()

    return districts

def display(districts: list[tuple], ljust=21):
    for val, district in districts:
        print(val.ljust(ljust) + district)

fn = None
if len(sys.argv) != 2:
    usage()
else:
    fn = sys.argv[1]


districts = parse(fn)

districts = sorted(districts, key=lambda a: a[1]+" "+a[0])

display(districts)
