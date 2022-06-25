# pocetna populacija na random => fiksiran pocetak
# izracunat f dobrote
# uzet 5 6 najboljih 
# krizanje => random tocka => i prvi dio uzima od prvog roditelja, drugi od drugog.
# a b c d c b e h 
# d f g a e f g h
import random as Rand

class path:
    nodePath = []
    fitness = 0
    def __init__(self):
        self.nodePath = []
        self.fitness = 0    

def startPopulation(listOfNodes, data, numberOfKids):
    themKids = []

    for i in range(0, numberOfKids):
        tempList = listOfNodes[:]
        
        Kid = path()
        
        Kid.nodePath.append("start")
        tempList.remove("start")
        
        Kid.nodePath.append("end")
        tempList.remove("end")
        
        while(len(tempList)):
            randomNumber = Rand.randint(0,len(tempList)-1)
            Kid.nodePath.insert(1, tempList[randomNumber])
            tempList.pop(randomNumber)
            Kid.fitness += calculateDistance(Kid.nodePath[1], Kid.nodePath[2], data)
        Kid.fitness += calculateDistance(Kid.nodePath[0], Kid.nodePath[1], data)
        themKids.append(Kid)
        del Kid
       
    return themKids

def calculateDistance(location1, location2, data):
    for i in range(0, len(data)):
        if data[i].name != location1 and data[i].name != location2:
            continue
        for j in range(0, len(data[i].connections)):
            if data[i].connections[j].end != location1 and data[i].connections[j].end != location2:
                continue
            return data[i].connections[j].distance
    return 0

def mutation(unit, data):
    firstIndex = Rand.randint(1,len(unit.nodePath)-2)
    secondIndex = Rand.randint(1,len(unit.nodePath)-2)

    while(firstIndex == secondIndex):
        secondIndex = Rand.randint(1,len(unit.nodePath)-2)
    
    temp = unit.nodePath[firstIndex]
    unit.nodePath[firstIndex] = unit.nodePath[secondIndex]
    unit.nodePath[secondIndex] = temp

    unit.fitness = 0

    for i in range(1,len(unit.nodePath)):
        unit.fitness += calculateDistance(unit.nodePath[i-1], unit.nodePath[i], data)

    return unit

def singleCrossover(Parent1, Parent2, pointOfBreak, listOfNodes, data):
    #Save 2 lists of names
    tempList1 = listOfNodes[:]
    tempList2 = listOfNodes[:]
    
    #Initialize 2 Kids
    Kid1 = path()
    Kid2 = path()

    #break both parents and add first part of the array to kids
    Kid1.nodePath = Parent1.nodePath[:pointOfBreak]
    Kid2.nodePath = Parent2.nodePath[:pointOfBreak]

    #Initialize 2 temporary variables
    secondPartOfKid1 = path()
    secondPartOfKid2 = path()

    #Let them become the second part of the opposite parent's array
    secondPartOfKid1.nodePath = Parent2.nodePath[pointOfBreak:]
    secondPartOfKid2.nodePath = Parent1.nodePath[pointOfBreak:]
    
    #Remove all the nodes that already occure in Kid1 from temporary List
    for nodeName in Kid1.nodePath:
        tempList1.remove(nodeName)

    #Remove all the nodes that already occure in Kid2 from temporary list
    for nodeName in Kid2.nodePath:
        tempList2.remove(nodeName)
    
    #Remove end from both lists so that end node isn't available for change
    tempList1.remove("end")
    tempList2.remove("end")

    # for each node in new part of the array 
    for i in range(0, len(secondPartOfKid1.nodePath) - 1):
        # If current Node is in the list of missing nodes, it means we don't have to change it, because it hasn't occured before
        if secondPartOfKid1.nodePath[i] in tempList1:
            # Remove that node's name from the missing nodes list so that we know we don't need it anymore 
            tempList1.remove(str(secondPartOfKid1.nodePath[i]))
            # Continue onto the new node
            continue
        
        # If this point is reached that means we have a node that already exists, we need to replace it.
        # Select random node from the missing nodes list and replace the duplicate.
        index = Rand.randint(0,len(tempList1)-1)
        secondPartOfKid1.nodePath[i] = tempList1[index]
        # Remove the node's name from the missing nodes list
        del tempList1[index]

    for i in range(0, len(secondPartOfKid2.nodePath) - 1):
        if secondPartOfKid2.nodePath[i] in tempList2:
            tempList2.remove(str(secondPartOfKid2.nodePath[i]))
            continue

        index = Rand.randint(0,len(tempList2)-1)
        secondPartOfKid2.nodePath[i] = tempList2[index]
        del tempList2[index]    

    for node in secondPartOfKid1.nodePath:
        Kid1.nodePath.append(node)
    
    for node in secondPartOfKid2.nodePath:
        Kid2.nodePath.append(node)

    for i in range(1,len(Kid1.nodePath)):
        Kid1.fitness += calculateDistance(Kid1.nodePath[i-1], Kid1.nodePath[i], data)
        Kid2.fitness += calculateDistance(Kid2.nodePath[i-1], Kid2.nodePath[i], data)

    return Kid1, Kid2