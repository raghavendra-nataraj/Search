import re
import sys
import time
from math import sqrt
cities = set()
cityDet = {}
cityIter = {}
cityMap = {}
fringe = []
depth = 0
oldDepth = 0
maxVal = sys.maxint
dScenic = sys.maxint
class Road():
    def __init__(self,c1,c2,distance,speed,name):
        self.c1 = c1
        self.c2 = c2
        self.distance = distance
        self.speed = speed
        self.name = name
class State():
    def __init__(self,path,distance,depth,time,hrst):
	self.path = path
	self.depth = depth
	self.distance = distance
	self.time = time
        self.hrst = hrst

class CDetails():
    def __init__(self,name,lat,lon):
	self.name = name
	self.lat = lat
	self.lon = lon
	

def update(state):
    global maxVal,dScenic
    options = {
	'distance':state.distance,
	'time' : state.time,
	'segments' : len(state.path),
	'scenic' : len([state.path[i] for i in range(1,len(state.path))  if cityIter[state.path[i-1]][state.path[i]].speed>=55])
    }
    tempValue = options[sys.argv[3]]
    if maxVal>tempValue:
	maxVal = tempValue
    if state.distance<dScenic:
        dScenic = state.distance

def heuristic(state,city1):
    if city1 in cityDet:
        c1 = cityDet[city1]
    else:
        return state.hrst
    c2 = cityDet[sys.argv[2]]
    return sqrt((c1.lat-c2.lat)**2 + (c1.lon-c2.lon)**2)

def getDistance(state,city):
    return (state.distance + cityIter[state.path[-1]][city].distance)

def getNodes(state,city):
    return len(state.path)

def getTime(state,city):
    cityDis = cityIter[state.path[-1]][city]
    return (state.time + cityDis.distance / float(cityDis.speed))

def getScenic(state,city):
    leng =  len([state.path[i] for i in range(1,len(state.path))  if cityIter[state.path[i-1]][state.path[i]].speed>=55])
    if leng==maxVal:
        if state.distance>dScenic:
            return sys.maxint
    else:
        return leng
    #return getDistance(state,city)

def dfs(state):
    fringe.append(state)

def bfs(state):
    fringe.insert(0,state)

def astar(state):
    global fringe
    fringe.append(state)
    fringe = sorted(fringe,key=getkey,reverse=True)

def getkey(state):
    return state.distance + state.hrst

def ids():
    global fringe,oldDepth
    if len(fringe)==0 and depth!=oldDepth:
    	startState()

def idsCheck(state):
    if  sys.argv[4]=="ids" and state.depth>depth:
        return False
    return True

funcPtr = {
    'distance': getDistance,
    'time' : getTime,
    'segments' : getNodes,
    'scenic' : getScenic
}

srchPtr = {
    'dfs': dfs,
    'bfs': bfs,
    'ids': dfs,
    'astar': astar
}

def parseCityFile(file):
    ifile = open(file,"r")
    city_data = ifile.readlines()
    for line in city_data:
	fields = line.split(' ')
	cityDet[fields[0]]= CDetails(fields[0],float(fields[1]),float(fields[2]))
    ifile.close()	

def parseFile(file):
    cityPat = "[\w\&\'\"\./\[\];,-]"
    pattern = "("+cityPat+"+) ("+cityPat+"+) (\d+) (\d+) ("+cityPat+"+)"
    patCmp = re.compile(pattern)
    ifile = open(file,"r")
    for line in ifile:
        patMat = re.match(patCmp,line)
        if patMat is not None and int(patMat.group(4))!=0:
            c1 = patMat.group(1)#.split(',')[0]
            c2 = patMat.group(2)#.split(',')[0]
            cities.add(c1)
            cities.add(c2)
            rd = Road(c1,c2,int(patMat.group(3)),int(patMat.group(4)),patMat.group(5))
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
                city[c1] = rd
                cityIter[c2] = city
            options = {
                'distance':cityIter[c1][c2].distance,
                'time' : cityIter[c1][c2].distance*cityIter[c1][c2].speed,
                'segments' : 1,
                'scenic' : 1
            }
            cityMap[c1+c2] = cityMap[c2+c1] = options[sys.argv[3]]
        #else:
        #    print line
    ifile.close()

def startState():
    global depth
    depth+=1
    del fringe[:] 
    state = State([sys.argv[1]],0,0,0,heuristic(None,sys.argv[1]))
    fringe.append(state)

def addState(state,city):
    return state.path[:]+[city]

def getConnectedCity(city):
    return cityIter[city].keys()

def getDetails(city1,city2):
    return cityIter[city1][city2]

def isValid(state,city,function):
    hashVal = state.path[0]+city
    funcVal = function(state,city)
    if hashVal in cityMap:
        if not funcVal<=cityMap[hashVal]:
            return False
        else:
            cityMap[hashVal] = funcVal
            return True
    else:
        cityMap[hashVal] = funcVal
        return True

def Successors(state,function):
    global oldDepth
    if state.depth>oldDepth:
	oldDepth = state.depth
    return [State(addState(state,city),\
	state.distance+cityIter[state.path[-1]][city].distance,state.depth+1,\
	          state.time+cityIter[state.path[-1]][city].distance/float(cityIter[state.path[-1]][city].speed),heuristic(state,city))\
	for city in getConnectedCity(state.path[-1]) \
	    if function(state,city)<=maxVal and city not in state.path and isValid(state,city,function) and idsCheck(state)]

def search(endNode,funcID,srchID):
    global iterDepth,goals
    startState()
    function = funcPtr[funcID]
    srchFunc = srchPtr[srchID]
    while len(fringe)>0:
        for state in Successors(fringe.pop(),function):
            #print state.path
            #time.sleep(1)
            if state.path[-1]==endNode:
                #print state.path
		#print state.distance
                goals = state
                update(state)
            srchFunc(state)
        srchID=="ids" and ids()

parseFile("road-segments.txt")
parseCityFile("city-gps.txt")
search(sys.argv[2],sys.argv[3],sys.argv[4])
if goals:
    print goals.distance,
    print goals.time,
    print ",".join(city for city in goals.path)
    
else:
    print "Solution not Found"

