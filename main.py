import copy
from timeit import default_timer as timer
class Grouping:
    
    def __init__(self, usedP, usedE, groups, size) -> None:  
        self.usedPairs = usedP
        self.usedElements = usedE
        self.groups = groups
        self.size = size
        self.sets = size-1

    def canAddPair(self, pair):
        if pair in self.usedPairs:
            return False
        for p in pair:
            if p in self.usedElements.keys():
                if self.usedElements[p] == self.sets:
                    return False
        if len(self.groups) != 0:
            for p in pair:
                if len(self.groups[-1]) != self.size/2:
                    for g in self.groups[-1]:
                        for e in g:
                            if p == e:
                                return False
        return True

    def addEl(self, pair):
        for p in pair:
            if p not in self.usedElements.keys():
                self.usedElements[p] = 1
            else:
                self.usedElements[p] = self.usedElements[p] + 1

    def addPair(self, pair):
        if len(self.groups) == 0:
            self.groups.append([pair])
            self.usedPairs.append(pair)
            self.addEl(pair)
            return self
        if len(self.groups[-1]) != self.size/2:
            self.groups[-1].append(pair)
            self.usedPairs.append(pair)
            self.addEl(pair)
            return self
        self.groups.append([pair])
        self.usedPairs.append(pair)
        self.addEl(pair)
        return self

def combinations(loe):
    combinations = []
    for i in range(len(loe)-1):
        for j in range(len(loe)-i-1):
            combinations.append((loe[i], loe[j+i+1]))
    return combinations

def makeGrouping(loe):

    pairs = combinations(loe)

    groupings = [Grouping([], {}, [], len(loe))]
    for index, g in enumerate(groupings):
        #print(len(groupings))
        if len(g.usedPairs) == len(pairs):
            return g
        for p in possiblePairs(g, pairs):
            grouping = copy.deepcopy(g)
            grouping.addPair(p)
            groupings.insert(index+1, grouping)

def possiblePairs(grouping: Grouping, loe):
    possiblePairs = []
    for i in loe:
        if grouping.canAddPair(i):
            possiblePairs.append(i)
    return possiblePairs

loe = []
for i in range(12):
    loe.append(i)
start = timer()

print(makeGrouping(loe).groups)

end = timer()

print(f'Time is: {end-start}')