#!/usr/bin/python
# import string
import sys
import os
from constraint import *

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
# Variables and domains for each type of container (X has the empty set as domain, so we ignore it)
S_variables = []
R_variables = []
domainR = []
domainS = []

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

print("container == ", container)
print("cells == ", cells)

for id in id_list:
    if type_list[id_list.index(id)] == 'S':
        S_variables.append(id_list.index(id) + 1)
    elif type_list[id_list.index(id)] == 'R':
        R_variables.append(id_list.index(id) + 1)

print("S_vars == ", S_variables)
print("R_vars == ", R_variables)

for c in range(len(cells)):
    if cells[c] == 'N':
        domainS.append(c)
    if cells[c] == 'E':
        domainS.append(c)
        domainR.append(c)

print("Domain S == ", domainS)
print("Domain R == ", domainR)

problem.addVariables(S_variables, domainS)
problem.addVariables(R_variables, domainR)


# ############################################ CONSTRAINTS ######################################################

# https://www.studytonight.com/python-howtos/pass-a-list-to-a-function-to-act-as-multiple-arguments

def checkCellOrder(a, b, *vars):
    # num_levels = len(map)
    num_stacks = int((len(cells) / len(map)))

    bl = False

    # if a < num_stacks and b == a-1:
    if b == a - 1:
        # comprobar que la celda de abajo (a-1+num_stacks) no está vacía
        for v in vars:
            if v == (a - 1 + num_stacks):
                bl = True
    if a >= num_stacks:  # and b == upperCell:
        upperCell = a - num_stacks
        if b == upperCell:
            bl = True

    return bl


def checkCells(*variables):
    ii = 0
    jj = 1
    ll = len(variables)
    ret = False
    while ii < ll:
        while jj < ll:
            # print("ii == ", ii, " jj == ", jj)
            # if destination_list[ii] > destination_list[jj]:
            if checkCellOrder(variables[ii], variables[jj], *variables):
                ret = True
            jj += 1
        ii += 1
        jj = ii + 1

    return ret


def translateIndexToCell(ind):
    # num_levels = len(map)
    num_stacks = int((len(cells) / len(map)))

    level = int(ind / num_stacks)
    stack = ind % num_stacks
    cell = (stack, level)
    return cell


'''
for i in range(len(cells)):
    print("translate cells[", i, "] to ", translateIndexToCell(i))

allVariables = S_variables.copy()
allVariables.extend(R_variables)
print("len allVariables == ", len(allVariables))
print("allVariables == ", allVariables)
print("id_list == ", id_list)
'''
print("id_list == ", id_list)

problem.addConstraint(AllDifferentConstraint())

problem.addConstraint(checkCells, id_list)
'''
numVars = len(id_list)
i = 0
j = 1
while i < numVars:
    # print("i == ", i)
    while j < numVars:
        # print("j == ", j)
        if destination_list[i] > destination_list[j]:
            problem.addConstraint(checkCellOrder, [id_list[i], id_list[j]])
        j += 1
    i += 1
    j = i + 1
'''
solutions = problem.getSolutions()

print("Number of solutions: ", len(solutions))
# Print every solution with correct index
for solution in solutions:
    for i in solution:
        solution[i] = translateIndexToCell(solution[i])
    # print(solution)

print("Number of solutions: ", len(solutions))
