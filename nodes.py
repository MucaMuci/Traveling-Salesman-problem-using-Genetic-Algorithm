from tkinter import *
import math
import gc

def initialization(labels, window, color, name):
    labels.append(Label(window, bg = color, width =10, height= 5, text=name))
    labels[-1].pack(side=LEFT)
    labels[-1].bind("<Button-1>",drag_start)
    labels[-1].bind("<B1-Motion>",drag_motion)
    labels[-1].bind("<ButtonRelease-1>", lambda event, name=name: drag_end(event, name))

def drag_end(event,name):
    widget = event.widget
    x = widget.winfo_x() - widget.startX + event.x
    y = widget.winfo_y() - widget.startY + event.y
    widget.place(x=x,y=y)
    locationCounter(x,y,name)

def drag_start(event):
    widget = event.widget
    widget.startX = event.x
    widget.startY = event.y

def drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget.startX + event.x
    y = widget.winfo_y() - widget.startY + event.y
    widget.place(x=x, y=y)
    
def locationCounter(x,y,name):
    global nodeList
    for i in range(0,len(nodeList)):
        if nodeList[i].name == name:
            nodeList[i].x = x
            nodeList[i].y = y
            newDistanceCounter(nodeList, nodeList[i])
            return
    nodeList.append(Node(name,x,y))
    distanceCounter(nodeList, nodeList[-1])

def distanceCounter(nodeList, node):
    for i in range(0, len(nodeList)):
        if nodeList[i].name != node.name:                                                                                   #za svaki cvor u listi
            nodeList[i].connections.append(Edge(node.name,functionDistance(nodeList[i].x, nodeList[i].y, node.x, node.y)))            

    for i in range(0, len(nodeList)):
        if nodeList[i].name != node.name:                                                                    
            node.connections.append(Edge(nodeList[i].name, functionDistance(nodeList[i].x, nodeList[i].y, node.x, node.y) ))      

def newDistanceCounter(nodeList, node):
    for i in range(0, len(nodeList)):                                                                               #za svaki cvor u listi
        for j in range(0, len(nodeList[i].connections)):                                                            #za svaku vezu tog cvora
            if nodeList[i].connections[j].end == node.name:                                                         #provjeri je li ime promijenjenog cvora
                nodeList[i].connections[j].distance = functionDistance(nodeList[i].x, nodeList[i].y, node.x, node.y)#izračunaj novu udaljenost
    
    for i in range(0, len(node.connections)):                                                                       #za svaku vezu promijenjenog cvora
        for j in range(0, len(nodeList)):                                                                           #za svaki cvor u listi
            if node.connections[i].end == nodeList[j].name:                                                         #provjeri je li pasu imena
                node.connections[i].distance = functionDistance(nodeList[j].x, nodeList[j].y, node.x, node.y)       #izracunaj novu udaljenost

def functionDistance(node1X, node1Y, node2X, node2Y):
    return round(math.sqrt((node2X - node1X)**2 + (node2Y - node1Y)**2)/10,2)    

def removeNode(nodeName):
    global nodeList
    for i in range(0, len(nodeList)):
        for j in range(0, len(nodeList[i].connections)):
            if nodeList[i].connections[j].end == nodeName:
                del nodeList[i].connections[j]
                break
    gc.collect()        
    for i in range(0,len(nodeList)):
        if nodeList[i].name == nodeName:
            del(nodeList[i])
            gc.collect()
            return

def test(nodeList):
    print("\n\n")
    for i in range(0,len(nodeList)):
        print(len(nodeList[i].connections))
        for j in range(0, len(nodeList[i].connections)):
            print(f"{nodeList[i].name} has {nodeList[i].connections[j].end} with price {nodeList[i].connections[j].distance}")

class Node:
    x=0
    y=0
    name=""
    connections = []
    def __init__(self,name,x,y):
        self.name=name
        self.x=x
        self.y=y
        self.connections=[]

class Edge:
    end = ""
    distance = 0
    def __init__(self, end, distance):
        self.end = end
        self.distance = distance

nodeList=[]