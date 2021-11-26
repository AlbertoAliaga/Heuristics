#!/usr/bin/python
import string
import sys
import os

import numpy
from constraint import *
# from numpy import *
import itertools

######################## Input reading ##################################
# In order to run this code on Linux: python3 csp.py /home/rbn/pyCharmProjects/Heuristica/lab-2/Heuristics/P2 Input-cells.txt Input-cont.txt

path = sys.argv[1]
map = sys.argv[2]
container = sys.argv[3]

os.chdir(path)
map_file_size = os.stat(str(path) + "/" + str(map)).st_size
container_file_size = os.stat(str(path) + "/" + str(container)).st_size

map = open(map, "r")
container = open(container, "r")

map = map.read(map_file_size)
container = container.read(container_file_size)

map = map.split("\n")
container = container.split("\n")

############################################# VARIABLES ######################################################

'''
    Each input on Input-cont.txt is a variable. The domains indicate whether it needs a power
    supplied cell or not (if it is an R type container it is needed) and their port destination.
'''

problem = Problem()

# One list per field on container
id_list = []
type_list = []
destination_list = []
# Domain for each type of container (X has the empty set as domain, so we ignore it)
standardDomain = []
energyDomain = []
numStacks = len(map)
stackSize = len(map[0].split())
variablesN = [] # numpy.zeros((numStacks, stackSize))
variablesE = []

# This loop takes variables from the containers and assigns domains
for elem in container:
    index = container.index(elem)
    container[index] = elem.split()  # List with separated elements from container list
    id_list.append(int(container[index][0]))
    type_list.append(container[index][1])
    destination_list.append(int(container[index][2]))

# Get a list of chars to properly iterate the cells
stackLevel = []
for i in map:
    # print(i)
    line_num = map.index(i)
    line = map[line_num].split()
    # print("map line ", line_num, " == ", line)
    j = 0
    while j < len(line):
        # print("line[", j, "] == ", line[j])
        stackLevel.append(line[j])
        j = j + 1


# Fill standardDomain and endergyDomain with their corresponding container id's
i = 0
while i < len(type_list):
    if type_list[i] == 'S':
        standardDomain.append(id_list[i])
    elif type_list[i] == 'R':
        energyDomain.append(id_list[i])
        standardDomain.append(id_list[i])

    i = i + 1

# Now fill each variable type list with the corresponding elements
# Each must be different, so we assign an index to each N and another to each E
n = 0
e = 0
for i in stackLevel:
    lvl = stackLevel.index(i)
    if i == 'N':
        var = i + str(n)
        variablesN.append(var)
        n = n + 1
    elif i == 'E':
        var = i + str(e)
        variablesE.append(var)
        e = e + 1

print("variablesN == ", variablesN)
print("variablesE == ", variablesE)
print("standardDomain == ", standardDomain)
print("energyDomain == ", energyDomain)

# Now add the variables to the problem
for i in variablesE:
    problem.addVariable(i, energyDomain)
for i in variablesN:
    problem.addVariable(i, standardDomain)

############################################# CONSTRAINTS ######################################################

'''
e = 0
n = 0
ii = 0
while ii < numStacks:
    jj = 0
    while jj < stackSize:
        if stackLevel[ii + jj] == 'N':
            ## Add loop variable
            problem.addVariable(variables[ii+jj], standardDomain)
            # variablesN.append(0)
            n = n + 1
        elif stackLevel[ii + jj] == 'E':
            ## Add loop variable
            #problem.addVariable(variables[ii+jj], energyDomain)
            variablesE.append(0)
            e = e + 1
        jj = jj + 1
    ii = ii + 1
'''
print("E == ", e, "\t N == ", n)

'''
# List with the cartesian product of all possible types of cells and destination ports
domain = []
for i in itertools.product(['N', 'E'], list(range(1, max(destination_list) + 1))):
    domain.append(i)
print("Domain: ")
print(domain)

#
for elem in container:
    index = container.index(elem)
    cont_id = id_list[index]  # Aux var to avoid memory accesses

    if type_list[index] == "S":
        toInputList = []
        for i in domain:
            if i[1] == destination_list[index]:
                toInputList.append(i)

        problem.addVariable(cont_id, toInputList)
        print("Container w/ S's id = ", cont_id)

    elif type_list[index] == "R":
        toInputList = []
        for i in domain:
            if i[1] == destination_list[index]:
                toInputList.append(i)

        problem.addVariable(cont_id, toInputList)
        print("Container w/ R's id = ", cont_id)

    else:
        print("Input error. ", sys.argv[3], " contains wrong data.")

print("\nID list: ", id_list)
print("Type list: ", type_list)
print("Destination list: ", destination_list, "\n")


def compareDestination(a, b):
    print("a: ", a, ", b: ", b)
    if a < b:
        return True


# This loop iterates over each container and compares its destination to all others
for id_index in range(0, len(id_list)):
    a = destination_list[id_index]
    for id_iter in range(id_index + 1, len(id_list)):
        # print(type_list[id_iter])
        b = destination_list[id_iter]
        problem.addConstraint(compareDestination, (a, b))


'''

# solutions = problem.getSolutions()
# print(solutions)
