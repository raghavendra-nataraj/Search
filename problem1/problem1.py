import re
import sys
import time
from Queue import PriorityQueue
cities = set()
cityIter = {}
fringe = []
goals = []
depth = 0
class Road():
    def __init__(self,c1,c2,distance,speed,name):
        self.c1 = c1
        self.c2 = c2
        self.distance = distance
        self.speed = speed
        self.name = name

def getDistance(state):
    return sum([cityIter[state[index]][state[index+1]].distance for index in range(0,len(state)-1)])

def getNodes(state):
    return len(state)

def getTime(state):
    return sum([cityIter[state[index]][state[index+1]].distance*cityIter[state[index]][state[index+1]].speed for index in range(0,len(state)-1)])

def getScenic(state):
    return state[-1]>55 

def dfs(state):
    fringe.append(state)

def bfs(state):
    fringe.insert(0,state)

def ids():
    global fringe
    if len(fringe)==0:
    	startState()

def idsCheck(state):
    if  sys.argv[4]=="ids" and len(state)>depth:
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
    'ids': dfs
}

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
        #else:
        #    print line
def startState():
    global depth
    depth+=1
    del fringe[:] 
    fringe.append([sys.argv[1]])

def addState(state,city):
    return state[0:len(state)]+[city]

def getConnectedCity(city):
    return cityIter[city].keys()

def printGraph():
    graphFile = open("Graph.dot","w")
    graphFile.write("digraph tring_graph {\n")
    for city in cityIter:
        for city2 in cityIter[city]:
            graphFile.write("\t"+city+"->"+city2+";\n")
    graphFile.write("}");
            
def getDetails(city1,city2):
    return cityIter[city1][city2]

def Successors(state,function,maxVal):
    return [addState(state,city) for city in getConnectedCity(state[-1]) if idsCheck(state) and city not in state and function(state)<maxVal]

def search(endNode,funcID,srchID):
    global iterDepth
    startState()
    function = funcPtr[funcID]
    srchFunc = srchPtr[srchID]
    maxVal = sys.maxint
    while len(fringe)>0:
        for state in Successors(fringe.pop(),function,maxVal):
            # print fringe
            #print depth
            time.sleep(1)
            if state[-1]==endNode:
                print state
                goals.append(state)
                tempValue = function(state)
                if maxVal>tempValue:
                    maxVal = tempValue
            srchFunc(state)
        #print depth
        srchID=="ids" and ids()

parseFile("road-segments.txt")
search(sys.argv[2],sys.argv[3],sys.argv[4])
