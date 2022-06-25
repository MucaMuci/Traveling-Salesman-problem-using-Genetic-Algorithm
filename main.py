from tkinter import *
import nodes as node
import table as tb
import gc
import geneticAlgorithm as GA
import operator
import random as Rand

def init():
    global vertexNumber
    global Table
    vertexNumber += 1
    node.initialization(labels, middleFrame,"red", f"Location {vertexNumber}")
    labelsNames.append(f"Location {vertexNumber}")
    Table.destroyTable()
    Table=tb.Table(bottomFrame, labelsNames)
    
def delete():
    global vertexNumber
    global labels
    global Table
    if(len(labels)>2):
        node.removeNode(labelsNames[-1])
        labels[-1].destroy()
        del labels[-1]
        gc.collect()
        vertexNumber -= 1
        labelsNames.pop()
        Table.destroyTable()
        Table=tb.Table(bottomFrame, labelsNames)

def createEndLabel(text):
    return Label(middleFrame, bg = "blue", width =10, height= 5, text=text)

def populationOutput(newWindowFrame, startingPopulation, Kids):
    for i in range(0,startingPopulation):
        text = Text(newWindowFrame, height=2, width=170)
        text.insert(END, f"{i+1}. random parent:\n")
        for j in range(0, len(Kids[i].nodePath)):
            text.insert(END,f"{Kids[i].nodePath[j]} ")
        text.insert(END, f" fitness function: {Kids[i].fitness}")
        text.pack(side=TOP)

def removeFromFrame(frame):
    for widgets in frame.winfo_children():
      widgets.destroy()

def crossoverOutput(frame, Kid1, Kid2, Parent1, Parent2, breakPoint, mutation1, mutation2):
    text1 = Text(frame,height=2, width=170)
    text1.insert(END, "1. Parent:\n")
    for i in range(0, len(Parent1.nodePath)):
        text1.insert(END,f"{Parent1.nodePath[i]} ")
    text1.insert(END, f" fitness= {Parent1.fitness}")
    text1.pack(side=TOP)

    text2 = Text(frame,height=2, width=170)
    text2.insert(END, "2. Parent:\n")
    for i in range(0, len(Parent2.nodePath)):
        text2.insert(END,f"{Parent2.nodePath[i]} ")
    text2.insert(END, f" fitness= {Parent2.fitness}")
    text2.pack(side=TOP)

    text5 = Text(frame, height=1, width= 170)
    text5.insert(END, f"Point of break: {breakPoint}")
    text5.pack(side=TOP)

    if(mutation1 == 1):
        text3 = Text(frame,height=2, width=170, bg="cyan")
    if(mutation1 == 0):
        text3 = Text(frame,height=2, width=170)
    text3.insert(END, "1. Child:\n")
    for i in range(0, len(Kid1.nodePath)):
        text3.insert(END,f"{Kid1.nodePath[i]} ")
    text3.insert(END, f" fitness= {Kid1.fitness}")
    text3.pack(side=TOP)

    if(mutation2 == 1):
        text4 = Text(frame,height=2, width=170, bg="cyan")
    if(mutation2 == 0):
        text4 = Text(frame,height=2, width=170)
    text4.insert(END, "2. Child:\n")
    for i in range(0, len(Kid2.nodePath)):
        text4.insert(END,f"{Kid2.nodePath[i]} ")
    text4.insert(END, f" fitness= {Kid2.fitness}")
    text4.pack(side=TOP)

    text6 = Text(frame, height=1, width=170, bg="black")
    text6.pack(side=TOP)

def checkFitness(Kids):
    global numberOfParents
    flag = 1
    for i in range(0,numberOfParents-1):
        for j in range(i, numberOfParents):
            if Kids[i].fitness != Kids[j].fitness:
                flag = 0           
    return flag

def selectParents(lengthOfParentsArray):
    firstParentIndex = Rand.randint(0,lengthOfParentsArray)
    secondParentIndex = Rand.randint(0,lengthOfParentsArray)
    
    while(secondParentIndex == firstParentIndex):
        secondParentIndex = Rand.randint(0,lengthOfParentsArray)
    
    return firstParentIndex, secondParentIndex

def parentOutput(frame, Parent, mutation1):
    if(mutation1 == 1):
        text1 = Text(frame,height=2, width=170, bg="cyan")
    if(mutation1 == 0):
        text1 = Text(frame,height=2, width=170)
    text1.insert(END, "Parent:\n")
    for i in range(0, len(Parent.nodePath)):
        text1.insert(END,f"{Parent.nodePath[i]} ")
    text1.insert(END, f" fitness= {Parent.fitness}")
    text1.pack(side=TOP)

def crossoverPhase(frame, Parents):
    global startingPopulation
    global numberOfRounds
    global mutationChance
    
    Kids = []
    numberOfRounds+=1
    mutation1 = 0
    mutation2 = 0

    my_canvas = Canvas(frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    my_scrollbar = Scrollbar(frame, orient=VERTICAL, command= my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    second_frame = Frame(my_canvas)

    my_canvas.create_window((0,0), window= second_frame, anchor="nw")

    # Add two of the most successful parents (by fitness function) to the next generation
    if Rand.uniform(0, 1) < mutationChance:
        Parents[0] = GA.mutation(Parents[0], node.nodeList)
        mutation1 = 1
        
    if Rand.uniform(0, 1) < mutationChance:
        Parents[1] = GA.mutation(Parents[1], node.nodeList)
        mutation2 = 1

    Kids.append(Parents[0])
    Kids.append(Parents[1])

    parentOutput(second_frame, Parents[0], mutation1)
    parentOutput(second_frame, Parents[1], mutation2)

    # The only "unwritten rule" in this code is that starting Population has to be a multiple of 2 because of this line
    # Create almost whole population except 2 
    for i in range(0, int(startingPopulation/2)-1):
        # Mutation variables that we use for output
        mutation1 = 0
        mutation2 = 0
        # Randomly select 2 parents
        fpi, spi = selectParents(len(Parents)-1)
        # Randomly choose routes breaking point
        pointOfBreak = Rand.randint(1, len(Parents[fpi].nodePath) - 1)
        # Generate 2 kids from parents and add them to the Kids array and show them on the screen 
        Kid1, Kid2 = GA.singleCrossover(Parents[fpi], Parents[spi], pointOfBreak, labelsNames, node.nodeList)
        
        # If randomly generated number is lower than mutation Chance (percentage) do the mutation 
        if Rand.uniform(0, 1) < mutationChance:
            Kid1 = GA.mutation(Kid1, node.nodeList)
            mutation1 = 1
        
        if Rand.uniform(0, 1) < mutationChance:
            Kid2 = GA.mutation(Kid2, node.nodeList)
            mutation2 = 1

        Kids.append(Kid1)
        Kids.append(Kid2)
        crossoverOutput(second_frame, Kid1, Kid2, Parents[fpi], Parents[spi], pointOfBreak, mutation1, mutation2)

    

    selectionButton = Button(frame, text="Next", command=lambda:[removeFromFrame(frame),loopFirstPhase(frame, Kids)])
    selectionButton.pack(side=TOP, pady=20)

def secondPhase(frame, Kids):
    global numberOfParents
    global numberOfRounds
    Kids.sort(key=operator.attrgetter('fitness'))
    Kids[:numberOfParents]
    populationOutput(frame,numberOfParents, Kids)
    
    crossoverButton = Button(frame, text= "Next", command =lambda:[removeFromFrame(frame), crossoverPhase(frame, Kids)])
    crossoverButton.pack(side=BOTTOM, pady=20)
    
    if numberOfRounds == 20 or checkFitness(Kids):
        crossoverButton.destroy()
        text = Text(frame, height=1)
        text.insert(END,"GA reached end")
        text.pack(side=BOTTOM, pady=20)

def loopFirstPhase(frame, Kids):
    global startingPopulation
    populationOutput(frame, startingPopulation, Kids)
    selectionButton = Button(frame, text="Next", command=lambda:[removeFromFrame(frame),secondPhase(frame, Kids)])
    selectionButton.pack(side=BOTTOM, pady=20)

def firstPhase():
    # Variables
    global labelsNames
    global startingPopulation
    # Open new window
    newWindow = Tk()
    newWindowFrame = Frame(newWindow)
    newWindowFrame.pack(fill=BOTH)

    Kids = GA.startPopulation(labelsNames, node.nodeList, numberOfKids = startingPopulation)
    populationOutput(newWindowFrame, startingPopulation, Kids)
    selectionButton = Button(newWindowFrame, text="Next", command=lambda:[removeFromFrame(newWindowFrame),secondPhase(newWindowFrame, Kids)])
    selectionButton.pack(side=BOTTOM, pady=20)
    newWindow.mainloop()

def updateTable():
    global Table
    global labelsNames
    distance = 0
    for i in range(1,len(Table.entry)):
        for j in range(1,len(Table.entry[i])):
            if i == j:
                continue
            distance = 0
            for k in range(0,len(node.nodeList)):
                if node.nodeList[k].name != labelsNames[j-1]:
                    continue
                for l in range(0, len(node.nodeList[k].connections)):
                    if node.nodeList[k].connections[l].end != labelsNames[i-1]:
                        continue
                    distance = node.nodeList[k].connections[l].distance
                    Table.entry[i][j].delete(0,END)
                    Table.entry[i][j].insert(0,distance)

window = Tk()

#SETTING UP FRAMES
#TOP FRAME
topFrame = Frame(window)
topFrame.pack(side=TOP,fill=X)
#MIDDLE FRAME
middleFrame = Frame(window,borderwidth=2, relief="groove")
middleFrame.pack(fill=BOTH, expand=1)
#BOTTOM FRAME
bottomFrame = Frame(window)
bottomFrame.pack(side=BOTTOM)

#DATA INITIALIZATION
vertexNumber = 0
labels=[]
labelsNames=[]
data=[[]]
startingPopulation = 20 # Has to be a multiple of 2
numberOfParents = 10
numberOfRounds = 0 # We set limit to 20 in function secondPhase
mutationChance = 0.1

#START NODE
start = createEndLabel("start")
node.initialization(labels, middleFrame, "blue", "start")
labelsNames.append("start")

#END NODE
end = createEndLabel("end")
node.initialization(labels, middleFrame, "blue", "end")
labelsNames.append("end")

#CREATE NODE BUTTON
createNodeButton = Button(topFrame, text ="Create block", command = init)
createNodeButton.pack(side=LEFT, padx=10)

#DELETE NODE BUTTON
deleteNodeButton = Button(topFrame, text = "Delete block", command= delete)
deleteNodeButton.pack(side=LEFT, padx=10)

#RUN ALGORITHM BUTTON
runAlgorithmButton = Button(topFrame, text="Run", command=firstPhase)
runAlgorithmButton.pack(side=RIGHT, padx=20)

#UPDATE TABLE BUTTON
updateTableButton = Button(topFrame, text="Update", command=updateTable)
updateTableButton.pack(side=RIGHT, padx=20)

#TABLE DISTANCE TABLE
Table=tb.Table(bottomFrame, labelsNames)

window.mainloop()