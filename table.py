from asyncio.windows_events import NULL
from tkinter import *
import gc

class Table:
    lastTableSize = 0
    entry=[[]]

    def destroyTable(self):
        for i in range(0,self.lastTableSize):
            for j in range(0,self.lastTableSize):
                self.entry[i][j].destroy()
            gc.collect()
    
    #CONSTRUCTOR
    def __init__(self, gui, labels):
        matrixSize = len(labels)+1
        #Initialize entry to 2D matrix
        self.entry=[[]]
        #Remove the empty array
        self.entry.pop()
        #Create an empty 2D matrix
        for i in range(0,matrixSize):
            self.entry.append(matrixSize*[None])
        
        for i in range(matrixSize):
            for j in range(matrixSize):
                #MAKE FIRST FIELD SAY PRICES 
                if i==0 and j==0:
                    self.entry[i][j] = Entry(gui, width=10, bg='Black',fg='Black', font=('Arial', 11, 'bold'))
                    self.entry[i][j].insert(END, "PRICES")
                    self.entry[i][j].grid(row=i, column=j)
                    self.entry[i][j].config(state=DISABLED)
                    continue
                #MAKE THE MAIN DIAGONAL 0
                if i==j:
                    self.entry[i][j] = Entry(gui, width=10, bg='Black',fg='Black', font=('Arial', 11, 'bold'))
                    self.entry[i][j].insert(END, "0")
                    self.entry[i][j].grid(row=i, column=j)
                    self.entry[i][j].config(state=DISABLED)
                    continue
                #INITIALIZE COLUMN NAME
                if i ==0:
                    self.entry[i][j] = Entry(gui, width=10, bg='LightSteelBlue',fg='Black', font=('Arial', 11, 'bold'))
                    self.entry[i][j].grid(row=i, column=j)
                    self.entry[i][j].insert(END, labels[j-1])
                    self.entry[i][j].config(state=DISABLED)
                    continue
                #INITIALIZE ROW NAME
                if j==0:
                    self.entry[i][j] = Entry(gui, width=10, bg='LightSteelBlue',fg='Black', font=('Arial', 11, 'bold'))
                    self.entry[i][j].grid(row=i, column=j)
                    self.entry[i][j].insert(END, labels[i-1])
                    self.entry[i][j].config(state=DISABLED)
                    continue
                #THE MAIN TABLE
                self.entry[i][j] = Entry(gui, width=10, fg='blue', font=('Arial', 11, ''))
                self.entry[i][j].grid(row=i, column=j)
        self.lastTableSize= matrixSize
                
                

