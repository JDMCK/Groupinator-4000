import copy
from art import tprint

# Ensures proper inputs (options should be listed as lowercase, inputs will be returned in the case they are written)
def inputSafe(msg, intInput=False, freeInput=False, options=['y', 'n']) -> str:
    while True:
        inp = input(msg)
        if inp == 'BACK':
            return inp
        elif freeInput:
            return inp
        elif intInput and inp.isdigit():
            return inp
        elif inp.lower() in options:
            return inp
        print('INVALID INPUT')

def printBreak():
    print('\n\n\n***************************************************\n\n\n')

def enterNewGroup():
    numOfStudents = inputSafe('How many students would you like to add?: ', intInput=True)
    if numOfStudents == 'BACK':
        printBreak()
        return
    numOfStudents = int(numOfStudents)
    students = []
    for s in range(numOfStudents):
        name = inputSafe(f'{s+1}. ', freeInput=True)
        if name == 'BACK':
            printBreak()
            return
        students.append(name + '\n')
    
    with open('Student_List.txt', 'w') as file:
        file.writelines(students)
    
    print('\nNew group saved to Student_List.txt')

def genNewGroups():
    students = []
    try:
        with open('Student_List.txt', 'r') as file:
            students = file.readlines()
    except:
        print('You have not added any students yet.')
        input('\nPress enter to continue...')
        return

    weeks = inputSafe('How many weeks do you need groups for this term?: ', intInput=True)
    if weeks == 'BACK':
        printBreak()
        return
    weeks = int(weeks)

    # Remove newline
    for i in range(len(students)):
        students[i] = students[i].strip()

    pairings = CombinationHandler.makeGrouping(students).groups
    finalPairings = fillOutWeeks(pairings, weeks)

    with open('Student_Pairings.txt', 'w') as file:
        for i in range(len(finalPairings)):
            print(f'Week {i+1}:\n')
            file.write(f'Week {i+1}: \n\n')
            for j in range(len(finalPairings[i])):
                pairingStr = f'{finalPairings[i][j][0]}, {finalPairings[i][j][1]}'
                print(pairingStr)
                file.writelines(pairingStr + '\n')
            print('\n')
            file.write('\n')

def readablePairings(pairings):

    # Convert all tuples to lists
    for i in range(len(pairings)):
        pairings[i] = list(pairings[i])
        for j in range(len(pairings[i])):
            pairings[i][j] = list(pairings[i][j])


    for p in pairings:
        for i in range(len(p)):
            p[i] = f'{p[i][0]} / {p[i][1]}'
    return pairings

def displayStudents():
    students = []
    try:
        with open('Student_List.txt', 'r') as file:
            students = file.readlines()
    except:
        print('You have not created this file yet.')
    for s in range(len(students)):
        print(f'{s+1}. {students[s]}', end="")
    input('\n\nPress enter to continue...')

def displayGroups():
    groupInfo = []
    try:
        with open('Student_Pairings.txt') as file:
            groupInfo = file.readlines()
    except:
        print('You have not created this file yet.')
    for g in groupInfo:
        print(g.strip())
    input('\nPress enter to continue...')

def menuHelp():
    print('This program works out of a console, but you can access the student list and pairings by navigating to this project in your files.')
    print('At any point, you may type \'BACK\' to return to the main menu, nothing will be saved.')
    print('You can\'t name someone \'BACK\'.')
    print('If an uneven number of students is entered, a "NO PARTNER" student will be generated.')
    print('This program may take some time to work, just let it load and it should finish!')

def fillOutWeeks(pairings, weeks):
    pairingsToAdd = weeks - len(pairings)

    if weeks < len(pairings):
        cutPairings = []
        for i in range(weeks):
            cutPairings.append(pairings[i])
        return cutPairings

    for i in sequence(len(pairings), pairingsToAdd):
        pairings.append(pairings[i])

    return pairings

def sequence(max, len, min=0):
    nums = []
    i = min
    for _ in range(len):
        if i > max-1:
            i = min
        nums.append(i)
        i = i+1
    return nums 

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

class CombinationHandler:

    def combinations(loe):
        combinations = []
        for i in range(len(loe)-1):
            for j in range(len(loe)-i-1):
                combinations.append((loe[i], loe[j+i+1]))
        return combinations
    
    def possiblePairs(grouping: Grouping, loe):
        possiblePairs = []
        for i in loe:
            if grouping.canAddPair(i):
                possiblePairs.append(i)
        return possiblePairs
    
    @staticmethod
    def makeGrouping(loe):

        pairs = CombinationHandler.combinations(loe)

        groupings = [Grouping([], {}, [], len(loe))]
        for index, g in enumerate(groupings):
            #print(len(groupings))
            if len(g.usedPairs) == len(pairs):
                return g
            for p in CombinationHandler.possiblePairs(g, pairs):
                grouping = copy.deepcopy(g)
                grouping.addPair(p)
                groupings.insert(index+1, grouping)

def displayMainMenu():
    while True:
        tprint('Groupinator-4000')
        print('1. Enter New Set of Students')
        print('2. Generate New Grouping')
        print('3. Display Current Students')
        print('4. Display Existing Groups')
        print('5. Help')
        print('6. Quit')
        inp = inputSafe('Enter the number of the option you would like to select: ', options=['1', '2', '3', '4', '5', '6'])
        match inp:
          case '1':
              printBreak()
              enterNewGroup()
          case '2':
              printBreak()
              genNewGroups()
          case '3':
              printBreak()
              displayStudents()
          case '4':
              printBreak()
              displayGroups()
          case '5':
              printBreak()
              menuHelp()
          case '6':
              quit()

displayMainMenu()