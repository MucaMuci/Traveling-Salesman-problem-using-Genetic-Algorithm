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

For this project we used a bit modified traveling salesman problem: 
*"Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city exactly once **and get to the end city**"*

