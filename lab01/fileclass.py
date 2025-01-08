#!/usr/bin/env python3

class census:
    def __init__(self, fn):
        self.districts = []
        self.ljust = 21
        self.parse(fn)

    def separate(self, data: str) -> tuple:
        # find first non-digit
        i = 0
        while data[i].isdigit():
            i += 1
        return (data[:i], data[i:])

    def getdata(self, line: str) -> str:
        a = 213
        b = 316 
        return line[a:b].strip() 

    def parse(self, fn: str) -> list[tuple]:
        self.districts = []
    
        fd = open(fn, 'r')

        for line in fd.readlines():
            data = self.getdata(line)
            self.districts.append( self.separate(data) )

        fd.close()

        self.districts = sorted(self.districts, key=lambda a: a[1])


    def display(self):
        for val, district in self.districts:
            print(val.ljust(self.ljust) + district)

    def searchByNum(self, num: int):
        num = str(num)
        for n,d in self.districts:
            if n == num:
                print(n.ljust(self.ljust) + d)
                break

    
    def searchByDistrict(self, district: str):
        for n,d in self.districts:
            if d == district:
                print(n.ljust(self.ljust) + d)
                break

