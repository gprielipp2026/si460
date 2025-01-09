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
        tosplit = line[327:372].strip() 
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

        self.districts = sorted(self.districts, key=lambda a: a[1])


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
        file = open(fn, 'w')
        file.write('<?xml version="1.0" endcoding="UTF-8"?>\n')
        file.write('<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">\n')
        file.write('<Document> id="1"')
        id_ = 2
        for num, district, (lat, lon) in self.districts:
            #lat = 'N'+lat[1:] if lat[0] == '+' else 'S'+lat[1:] 
            #lon = 'W'+lat[1:] if lon[0] == '+' else 'E'+lon[1:] 
       
            file.write(f'\t<Placemark id="{id_+1}">\n')
            file.write(f'\t\t<name>{district}</name>\n')
            file.write(f'\t\t<Point id="{id_}">\n')
            file.write(f'\t\t\t<latitude>{lat}</latitude>\n')
            file.write(f'\t\t\t<longitude>{lon}</longitude>\n')
            file.write(f'\t\t</Point>\n')
            file.write('\t</Placemark>\n')
            id_ += 2 

        file.write('</Document>\n')
        file.write('</kml>')
        
        file.close()
    

if __name__ == '__main__':
    mycensus = census('mdgeo2010.dp')

    mycensus.display()

    mycensus.searchByNum(60463)
    mycensus.searchByDistrict('Worton CDP')

    mycensus.saveKML('census.kml')


