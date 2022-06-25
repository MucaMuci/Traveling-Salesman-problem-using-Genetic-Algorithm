# Traveling-Salesman-problem-using-Genetic-Algorithm
Solving Traveling Salesman problem using my custom made Genetic Algorithm.

## What are Genetic Algorithms?
Classic genetic algorithm consist of 4 phases:
1. Create starting population
2. Determine each unit's fitness function
4. Create reproduction pool (Selection)
5. Crossover and mutation

This process is repeated until number of iterations reaches its maximum (that we defined). Also some things need to be noted: 
- Starting population is created randomly or pseudo-randomly.
- Fitness function is a crucial part of each GA and is also specific for each domain. It determines the goodness of unit by some measures.
- Selection takes the best units by fitness function and lets them pass on their genes.
- Crossover takes one or two (or even more) parent units and crossess their genes to create child unit.
- Mutation is random and usually rare (to avoid complete randomness).

## Traveling Salesman problem
In short, traveling salesman problem answers the question: 
*"Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the origin city"*.

For this project I used a bit modified traveling salesman problem: 
*"Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city exactly once **and gets us to the end city**"*

## How does my GA work?
Let's go shortly go, step by step, through each GA phase.
1. Starting population is created randomly, so that each starting unit has each node (location) once, and starts with start node, and ends with end node. Then for each unit in starting population fitness function is calculated.
2. Selection is done so that only the best parent units pass on their genetic material (path).
3. For the next generation we pass on two of the best parent unit's, so that good genetic material can't be lost. The rest of the population is created by crossover between two randomly selected parents. Each pair of parents creates a pair of children. Firstly, we select *point of break*. For the first child, left of that point we take path from the first parent, and right of that point we append second parents path. For the second child we do the opposite. For example:

Parent1: Start L1 L3 L5 L6 L2 L4 End

Parent2: Start L3 L2 L4 L3 L5 L6 End

Point of Break = 3

Child1: **Start L1 L3** L4 L3 L5 L6 End

Child2: **Start L3 L2** L5 L6 L2 L4 End

The problem is, some nodes repeat more than once, and some nodes get lost in crossover. This was solved by changing up the second part of a child before it is added to the first part.*The list of missing nodes* was created, by going through the fist part of a child and removing all the nodes that are already there from the list of all nodes. End node was removed from the list so that when we need to replace reappearing node, end isn't available for selection. So the example would actually look like this (for one child):

Parent1: Start L1 L3 L5 L6 L2 L4 End

Parent2: Start L3 L2 L4 L3 L5 L6 End

Point of Break = 3

0.  Child1: **Start L1 L3**
    
    List_of_missing_nodes1: L2 L4 L5 L6
    
    Second_part_of_child1: L4 L3 L5 L6 End


1.  Second_part_of_child1: **L4** L3 L5 L6 End
    
    List_of_missing_nodes1: L2 **L4** L5 L6 
    
    Node **is in** the list, we don't need to change *Second_part_of_child1*. **REMOVE** node from the list.


2.  Second_part_of_child1: L4 **L3** L5 L6 End
    
    List_of_missing_nodes1: L2 L5 L6
    
    Node is not in the list. That means it already appeared before. We need to replace it. **We RANDOMLY** select a node from the list of missing nodes and replace L3.
 
 
3.  Second_part_of_child1: L4 L2 **L5** L6 End
    
    List_of_missing_nodes1: **L5** L6


4.  Second_part_of_child1: L4 L3 L5 **L6** End
    
    List_of_missing_nodes1: **L6**


5.  Second_part_of_child1: L4 L3 L5 L6 End
    
    List_of_missing_nodes1: NULL
    
    Second part is ready to be added to the first one. So in the end the Child1 would look like this:
    
    Child1: Start L1 L3 L4 L3 L5 L6 End
  

4. Only thing left is mutation, and it is simply achieved by swapping 2 nodes (locations) in one unit. Only rule is that start and end nodes have to remain the same.
