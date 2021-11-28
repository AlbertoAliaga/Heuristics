#!/usr/bin/python
# import string
import sys
import os

# import numpy
from constraint import *

# from numpy import *
# import itertools

######################## Input reading ##################################
# In order to run this code on Linux: python3 csp.py /home/rbn/pyCharmProjects/Heuristica/lab-2/Heuristics/input-files cells-00.txt containers-00.txt

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

# ############################################ VARIABLES ######################################################

problem = Problem()

# One list per field on container
id_list = []
type_list = []
destination_list = []
# Domain for each type of container (X has the empty set as domain, so we ignore it)
standardDomain = []
energyDomain = []
variablesN = []  # numpy.zeros((numStacks, stackSize))
variablesE = []

# This loop takes variables from the containers and assigns domains
for elem in container:
    index = container.index(elem)
    container[index] = elem.split()  # List with separated elements from container list
    id_list.append(int(container[index][0]))
    type_list.append(container[index][1])
    destination_list.append(int(container[index][2]))

# Get a list of chars to properly iterate the cells
cells = []
for i in map:
    # print(i)
    line_num = map.index(i)
    line = map[line_num].split()
    # print("map line ", line_num, " == ", line)
    j = 0
    while j < len(line):
        # print("line[", j, "] == ", line[j])
        cells.append(line[j])
        j = j + 1

# Fill standardDomain and energyDomain with their corresponding container id's
standardDomain.append(0)
energyDomain.append(0)
for i in range(len(type_list)):
    if type_list[i] == 'S':
        standardDomain.append(id_list[i])
    elif type_list[i] == 'R':
        energyDomain.append(id_list[i])
        # standardDomain.append(id_list[i])

# Now fill each variable type list with the corresponding elements
# Each must be different, so we assign an index to each N and another to each E
n = 0
e = 0
for i in cells:
    lvl = cells.index(i)
    if i == 'N':
        var = i + str(n)
        variablesN.append(var)
        n = n + 1
    elif i == 'E':
        var = i + str(e)
        variablesE.append(var)
        e = e + 1

num_levels = len(map)
num_stacks = (len(cells) / len(map))

# Now add the variables to the problem
allVariables = variablesN.copy()
allVariables.extend(variablesE)
allDomains = standardDomain.copy()
allDomains.extend(energyDomain)

for i in allVariables:
    if i[0] == "N":
        # print("of type N > ", i)
        problem.addVariable(i, allDomains)
    elif i[0] == "E":
        # print("of type E > ", i)
        problem.addVariable(i, energyDomain)


print("map == ", map, "\tnum levels == ", num_levels, "\tnum stacks == ", num_stacks)
print("cells == ", cells)
print("variablesN == ", variablesN)
print("variablesE == ", variablesE)

print("allVariables == ", allVariables)
print("standardDomain == ", standardDomain)
print("energyDomain == ", energyDomain)
print("allDomains == ", allDomains)
print("E count == ", e, "\t N count == ", n)


# ############################################ CONSTRAINTS ######################################################

# Make sure a container doesn't get assigned to several cells at the same time
sum = 0
for i in id_list:
    sum += i
# print("Sum of all variables: ", sum)
problem.addConstraint(ExactSumConstraint(3))


# Now give preference to those cells which are on the bottom of the stack
def checkPortPreference(a, b):
    if a >= b:
        return True
    return False


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

solutions = problem.getSolution()
print("Solutions:\t", solutions)
