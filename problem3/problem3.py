import sys
from sets import Set
from copy import deepcopy
friends = {}
fringe = []
people = Set()
peopleCpy = Set()
class State():
    def __init__(self,st,pl):
        self.st = st
        self.pl = pl

def parseFile():
    global peopleCpy
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
    peopleCpy = deepcopy(people)

def addPerson(state,table,person):
    state.st[state.st.index(table)].append(person)
    return state.st
                    
def successors(state):
    #print state.st
    if len(state.pl)>0:
        person = state.pl.pop()
        st =  [State(addPerson(deepcopy(state),table,person),deepcopy(state.pl)) for table in state.st if len(table)<int(sys.argv[2])]
        state.st.append([person])
        st.append(state)
        z = [s.st for s in st]
        #print "\t",z
        return st
    return []

def isGoal(state):
    print len(peopleCpy),sum([len(s) for s in state.st])
    if len(peopleCpy)==sum([len(s) for s in state.st]):
        print [s for s in state.st]

def solve(state):
    fringe.append(state)
    while len(fringe)>0:
        for st in successors(fringe.pop()):
           #print st
            if isGoal(st):
                return state
            fringe.append(st)
        

parseFile()
initialState = []
state = State(initialState,people)
solve(state)
