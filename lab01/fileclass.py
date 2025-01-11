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

    def coords(self, line):
        tosplit = line[328:373].strip() 
        latInd = line.index('.') - 3
        longInd = line.index('.', latInd + 4) - 4
        endLong = line.index(' ', longInd) 
        #print(tosplit, latInd, longInd, endLong, line[latInd:longInd], line[longInd:endLong])
        return (line[latInd:longInd], line[longInd:endLong])

    def parse(self, fn: str) -> list[tuple]:
        self.districts = []
    
        fd = open(fn, 'r')

        for line in fd.readlines():
            data = self.getdata(line)
            #print(self.coords(line))
            self.districts.append( (*self.separate(data), self.coords(line)) )

        fd.close()

        self.districts = sorted(self.districts, key=lambda a: a[1]+" "+a[0])


    def display(self):
        for val, district, *junk in self.districts:
            print(val.ljust(self.ljust) + district)

    def searchByNum(self, num: int):
        num = str(num)
        for n,d, *junk in self.districts:
            if n == num:
                print(n.ljust(self.ljust) + d)
                break

    
    def searchByDistrict(self, district: str):
        for n,d, *junk in self.districts:
            if d == district:
                print(n.ljust(self.ljust) + d)
                break

    def saveKML(self, fn):
        from kml import KML, Placemark, Point, SimpleAttr
       
        k = KML(fn)
        placemarks = 0
        for num, dist, coords in self.districts:
            name = SimpleAttr('name', dist)
            point = Point(coords)
            placemark = Placemark(placemarks, name, point)
            k.addEntity(placemark)
            placemarks += 1
        k.saveKML()

if __name__ == '__main__':
    mycensus = census('mdgeo2010.dp')

    mycensus.display()

    mycensus.searchByNum(60463)
    mycensus.searchByDistrict('Worton CDP')

    mycensus.saveKML('census.kml')


