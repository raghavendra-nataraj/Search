''' Abstracttion for problem 1:
a. Valid State, S: Any valid city name
b. Initial state, S0: Start city
c. Goal State, G: {S| S is the destination city}
d. Successor function, Succ(S) = {S' | S' is a list of valid city names connected directly to city S}
However, successor function will be different for routing option scenic as mentioned below:
Successor function, Succ(S) = {S' | S' is a list of valid city names connected directly to city S such that the speed limit on the connecting highways is 55 mph or greater}
e. Depending on the routing option cost function can be defined as:
For segments, Cost Function = Number of cities explored to reach the destination city
For distance, Cost Function = Distance travelled to reach the destination city
For time, Cost Function = Time taken to reach the destination city
For scenic, Cost Function = Distance travelled to reach the destination city
f. Heuristic function defined: Distance from the current city to the destination city
The below program measures the distance (based on the latitude and longitude) from the current city to the destination city. The one with the least distance is explored first. However, we have cities in data for which we do not have the corresponding latitude and longitude information. For all such cities, A* will not have any heuristic value and will thus work as BFS.
The above heuristic function is admissible since it calculates the direct distance between the current city and the destination city.
If there exists a direct connecting highways between the current city and the destination, in that case the heuristic value will correctly estimate the distance for the goal state. If there is no direct highway between the two, even in that case, the direct distance will always be less than or equal to the sum of the distances of the segments between the current city and destination city. Thus, in this way, our heuristic function will never overestimate the goal and hence is admissible.

1) which search algorithm seems to work best for each routing options

   	distance ----- astar
	time ----- bfs
	scenic ----- astar
	segments------ bfs

-For distance as the routing option, A-star algorithm works best.
	This is because,A-star algorithm selects the shortest path to traverse based on the heuristic function. Whereas the BFS traverses through all the successors till the goal is reached.
-For time as the routing option, BFS algorithm works best.
	Time finds the fastest route, for a car that always travels at the speed limit. BFS works faster than A-star in this case, because the heuristic used in A-star uses Euclidean distance between cities and calculating this heuristic is slow compared to bfs with time as routing option.		
-For scenic as the routing option, A-star algorithm works best.			
-For segments as the routing option, bfs algorithm works best 
	Least number of segments(highways) is returned faster in the case BFS ,as it finds the least number of nodes required to reach the goal.Where as a-star uses least distance heuristic

2) Which algorithm is fastest in terms of the amount of computation time required by your program, and by how much, according to your experiments?

We tested the algorithm for the 4 available options and A* turns out to perform the best in terms of the computation time required.
The difference is quite significant with respect to DFS and IDS. With BFS, however, the difference is around that of 4 seconds.
3)Which algorithm requires the least memory, and by how much, according to your
experiments?

astar uses the least memory because the maximum length of fringe at anytime for the longest path(Skagway) is 230 whereas the other algorithm bfs is around 5957

4) Which heuristic function did you use, how good is it, and how might you make it
better?

We used the euclidean distance as our heuristic.

5) Supposing you start in Bloomington, which city should you travel to if you want to take the longest possible drive (in miles) that is still the shortest path to that city? (In other words, which city is furthest from Bloomington?)

The furthest city from Bloomington is Skagway, Alaska. The total distance between the two is 4542.
Thus, one can travel to Skagway, Alaska to take the longest possible drive from Bloomington.
'''

import re
import sys
import time
from math import sqrt
cities = set()
cityDet = {}
cityIter = {}
cityMap = {}
fringe = []
depth = 1
oldDepth = 0
maxVal = sys.maxint
goals = None
class Road():
    def __init__(self,c1,c2,distance,speed,name):
        self.c1 = c1
        self.c2 = c2
        self.distance = distance
        self.speed = speed
        self.name = name
class State():
    def __init__(self,path,distance,depth,time,hrst,speed):
	self.path = path
	self.depth = depth
	self.distance = distance
	self.time = time
        self.hrst = hrst
	self.speed = speed

class CDetails():
    def __init__(self,name,lat,lon):
	self.name = name
	self.lat = lat
	self.lon = lon
	

def update(state):
    global maxVal
    options = {
	'distance':state.distance,
	'time' : state.time,
	'segments' : len(state.path),
	'scenic' : state.speed
    }
    tempValue = options[routingOption]
    if maxVal>tempValue:
	maxVal = tempValue

def heuristic(state,city1):
    if city1 in cityDet and destinationCity in cityDet:
        c1 = cityDet[city1]
    else:
        return state.hrst
    c2 = cityDet[destinationCity]
    return state.distance + sqrt((c1.lat-c2.lat)**2 + (c1.lon-c2.lon)**2)

def getDistance(state,city):
    return (state.distance + cityIter[state.path[-1]][city].distance)

def getNodes(state,city):
    return len(state.path)

def getTime(state,city):
    cityDis = cityIter[state.path[-1]][city]
    return (state.time + cityDis.distance / float(cityDis.speed))

def getScenic(state,city):
    leng = state.speed
    return leng

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
    global fringe,oldDepth,depth
    if len(fringe)==0 and depth!=oldDepth:
        depth+=1
    	startState()

def idsCheck(state):
    if  routingAlgorithm=="ids" and state.depth>depth:
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
        #else:
        #    print line
    ifile.close()

def startState():
    global depth,cityMap
    depth+=1
    cityMap = {}
    del fringe[:]
    #maxVal = sys.maxint
    state = State([startCity],0,0,0,0,0)
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
        if not funcVal<cityMap[hashVal]:
            return False
        else:
            cityMap[hashVal] = funcVal
            return True
    else:
        cityMap[hashVal] = funcVal
        return True

def isHighway(state,city):
    if cityIter[state.path[-1]][city].speed>=55:
	return 1
    else:
	return 0

def Successors(state,function):
    global oldDepth
    if state.depth>oldDepth:
	oldDepth = state.depth
    return [State(addState(state,city),\
	state.distance+cityIter[state.path[-1]][city].distance,state.depth+1,\
	          state.time+cityIter[state.path[-1]][city].distance/float(cityIter[state.path[-1]][city].speed),heuristic(state,city),\
	state.speed+isHighway(state,city))\
	for city in getConnectedCity(state.path[-1]) \
	    if function(state,city)<maxVal and city not in state.path and isValid(state,city,function) and idsCheck(state)]

def search(endNode,funcID,srchID):
    global goals
    startState()
    #print depth
    function = funcPtr[funcID]
    srchFunc = srchPtr[srchID]
    while len(fringe)>0:
        for state in Successors(fringe.pop(),function):
            if state.path[-1]==endNode:
                goals = state
                update(state)
            srchFunc(state)

startCity = sys.argv[1]
destinationCity = sys.argv[2]
routingOption = sys.argv[3]
routingAlgorithm = sys.argv[4]
parseFile("road-segments.txt")
parseCityFile("city-gps.txt")
if destinationCity not in cityDet:
    routingAlgorithm = "bfs"
if routingAlgorithm=="ids":
    while depth<len(cities):
        search(destinationCity,routingOption,routingAlgorithm)
else:
    search(destinationCity,routingOption,routingAlgorithm)

if goals:
    for i in range(1,len(goals.path)):
        c1 = goals.path[i-1]
        c2 = goals.path[i]
        cityObj = cityIter[c1][c2]
        # print c1,c2,cityObj.distance,cityObj.speed,round(cityObj.distance/float(cityObj.speed),4),cityObj.name
        print "Drive from city " + c1 + " to city " + c2 + " covering a distance of " + str(cityObj.distance) + " miles at a speed of " + str(cityObj.speed)\
            + " mph " + "in " + str(round(cityObj.distance / float(cityObj.speed), 4)) + " hours on highway " + cityObj.name
    print "\n"
    print goals.distance,
    print round(goals.time,4),
    print len(goals.path),
    print ",".join(city for city in goals.path)
    
else:
    print "Solution not Found"

