#!/usr/bin/python
# import string
import sys
import os

# import numpy
from constraint import *

# from numpy import *
# import itertools

# ####################### Input reading ##################################
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

num_levels = len(map)
num_stacks = int((len(cells) / len(map)))
# Now fill each variable type list with the corresponding elements
# Each must be different, so we assign an index to each variable to later check its position in the cargo ship
i = 0
j = 0
while j < num_levels - 1:
    while i < num_stacks:
        var = cells[i + j * num_stacks] + str(j) + "-" + str(i)
        if cells[num_stacks * j + i] == 'N':
            variablesN.append(var)
        elif cells[num_stacks * j + i] == 'E':
            variablesE.append(var)
        i += 1
    i = 0
    j += 1

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
'''
print("map == ", map, "\tnum levels == ", num_levels, "\tnum stacks == ", num_stacks)
print("cells == ", cells)
print("variablesN == ", variablesN)
print("variablesE == ", variablesE)

print("allVariables == ", allVariables)
print("standardDomain == ", standardDomain)
print("energyDomain == ", energyDomain)
print("allDomains == ", allDomains)
# print("E count == ", e, "\t N count == ", n)
'''
# ############################################ CONSTRAINTS ######################################################

# Make sure a container doesn't get assigned to several cells at the same time
sum = 0
for i in id_list:
    sum += i
# print("Sum of all variables: ", sum)
problem.addConstraint(ExactSumConstraint(sum))
problem.addConstraint(MaxSumConstraint(sum))
# problem.addConstraint(AllDifferentConstraint())


# Now give preference to those cells which are on the bottom of the stack
def checkPortPreference(a, b):
    if b <= a:
        return True
    return False


def getVariableIndex(ii, jj):
    # print("getVariableIndex(", i, ",", j, ")")
    toReturn = -1
    for var in allVariables:
        iter = var[1:]
        div = iter.split("-")
        x = int(div[0])
        y = int(div[1])

        if int(ii) == x and int(jj) == y:
            # print("iter(", x, ",", y, ") with i = ", ii, "and j = ", jj)
            # print("getVarIn -> ", var)
            toReturn = allVariables.index(var)
    # print()
    return toReturn


print("allVariables == ", allVariables)

i = num_stacks - 1
j = num_levels - 1
while j >= 0:
    while i >= 0:
        if cells[i + j * num_stacks] != "X":
            if j > 0:
                # print("cells[i+j*num_stacks] == ", cells[i + j * num_stacks])
                index = getVariableIndex(int(i), int(j))
                if index != -1:
                    index2 = getVariableIndex(i, j - 1)
                    print("celda[", i, ", ", j, "] == index(", index, ")")
                    problem.addConstraint(checkPortPreference, (allVariables[index], allVariables[index2]))

            elif j == 0:
                index = getVariableIndex(i, j)

                print("j == 0")
        i -= 1
    i = num_stacks - 1
    j -= 1

solutions = problem.getSolution()
print("Solutions:\t", solutions)
