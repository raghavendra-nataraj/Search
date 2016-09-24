import sys
from sets import Set
from copy import deepcopy
friends = {}
fringe = []
people = Set()
peopleCpy = Set()
minResult = sys.maxint
class State():
    def __init__(self,st,pl):
        self.st = st
        self.pl = pl

def parseFile():
    global peopleCpy
    global friends
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

def isValid(table,person):
    return len(Set(friends[person]).intersection(Set(table)))<1

def successors(state):
    if len(state.pl)>0:
        person = state.pl.pop()
        st =  [State(addPerson(deepcopy(state),table,person),deepcopy(state.pl)) for table in state.st if len(table)<int(sys.argv[2]) and isValid(table,person) and len(state.st)<=minResult]
        state.st.append([person])
        st.append(state)
        return st
    return []

def isGoal(state):
    isTrue = True
    if len(peopleCpy)==sum([len(s) for s in state.st]):
        return all([len(Set(friends[friend]).intersection(Set(table)))<1 \
                   for table in state.st for friend in table])
    else:
        isTrue = False
    return isTrue
            

def solve(state):
    global minResult,goal
    fringe.append(state)
    while len(fringe)>0:
        for st in successors(fringe.pop()):
            if isGoal(st):
                if len(st.st)<minResult:
                    goal = st.st
                    minResult = len(st.st)
            fringe.append(st)
        

parseFile()
initialState = []
state = State(initialState,people)
solve(state)
pResult = [["Table"+str(ids+1)+"-"+ps] for ids in range(0,len(goal)) for ps in goal[ids]]
print [len(goal)],pResult
