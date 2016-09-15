import re

class Road():
    def __init__(self,c1,c2,distance,speed,name):
        self.c1 = c1
        self.c2 = c2
        self.distance = distance
        self.speed = speed
        self.name = name


cities = set()
cityIter = {}

def parseFile(file):
    cityPat = "[\w\&\'\"\./\[\];,-]"
    pattern = "("+cityPat+"+) ("+cityPat+"+) (\d+) (\d+) ("+cityPat+"+)"
    patCmp = re.compile(pattern)
    ifile = open(file,"r")
    for line in ifile:
        patMat = re.match(patCmp,line)
        if patMat is not None:
            c1 = patMat.group(1).split(',')[0]
            c2 = patMat.group(2).split(',')[0]
            cities.add(c1)
            cities.add(c2)
            rd = Road(c1,c2,patMat.group(3),patMat.group(4),patMat.group(5))
            if c1 in cityIter:
                cityIter[c1][c2] = rd
            else:
                city = {}
                city[c2] = rd
                cityIter[c1]= city
            if c2 in cityIter:
                cityIter[c2][c1] = rd
            else:
                city = {}
                city[c2] = rd
                cityIter[c2] = city
        #else:
        #    print line

def getConnectedCity(city):
    return cityIter[city].keys()

def getDetails(city1,city2):
    return cityIter[city1][city2]

parseFile("road-segments.txt")
print getConnectedCity("Aberdeen")
    

    
    
