import sys
from sets import Set
from copy import deepcopy
friends = {}
fringe = []
people = Set()

class State():
    def __init__(self,st,pl):
        self.st = st
        self.pl = pl

def parseFile():
    ifile = open(sys.argv[1],"r")
    content = ifile.readlines()
    for line in content:
        lst = line[:len(line)-1].split(" ")
        people.update(lst)
        if lst[0] not in friends:
            friends[lst[0]] = Set(lst[1:])
        else:
            friends[lst[0]].update(lst[1:])
            for friend in friends[lst[0]]:
                if friend in friends:
                    friends[friend].add(lst[0])
                else:
                    friends[friend] = Set([lst[0]])
def addPerson(state):
    sgh =  state.st[state.st.index(table)].append(state.pl.pop())
    print sgh
                    
def successors(state):
    return [State(addPerson(deepcopy(state),table),state.pl) for table in state.st]

def solve(state):
    fringe.append(state)
    print state.st
    while len(fringe)>0:
        for st in successors(fringe.pop()):
            #if isGoal(state):
            #    return state
            fringe.append(st)
        

parseFile()
initialState = []
state = State(initialState,people)
solve(state)
