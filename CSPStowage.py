#!/usr/bin/python
# import string
import sys
import os
from constraint import *

# ####################### Input reading ##################################

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
    

# num_levels = len(map)
num_stacks = int((len(cells) / len(map)))
bottomCells = []
for c in range(len(cells)):
    if c < len(cells) - num_stacks:
        if cells[c] != 'X' and cells[c + num_stacks] == 'X':
            bottomCells.append(c)
    else:
        if cells[c] != 'X':
            bottomCells.append(c)

print("BottomCells == ", bottomCells)
print("Domain S == ", domainS)
print("Domain R == ", domainR)

problem.addVariables(S_variables, domainS)
problem.addVariables(R_variables, domainR)

# ############################################ CONSTRAINTS ######################################################


def checkCellOrder(a, b):
    if a == b+num_stacks or b == a+num_stacks:
       return True
    return False
    
def checkPortOrder(a, b, dest):
    ret = False
    for ii in dest:
        for jj in dest:
            if ii >= jj and a < b+num_stacks:
                ret=True
            else:
                ret=False
    return ret

def checkCells(*variables):
    ret = False
    for ii in variables:
        for jj in variables:
            if ii != jj:
                if checkCellOrder(ii, jj) and checkPortOrder(ii, jj, destination_list):
                    ret = True
    return ret


def translateIndexToCell(ind):
    # num_levels = len(map)
    num_stacks = int((len(cells) / len(map)))

    level = int(ind / num_stacks)
    stack = ind % num_stacks
    cell = (stack, level)
    return cell


print("id_list == ", id_list)

problem.addConstraint(AllDifferentConstraint())

problem.addConstraint(checkCells)

solutions = problem.getSolutions()

print("Number of solutions: ", len(solutions))
# Print every solution with correct index
for solution in solutions:
    for i in solution:
        solution[i] = translateIndexToCell(solution[i])
    #print(solution)

print("Number of solutions: ", len(solutions))

path = sys.argv[1]
path = path[:-12]
path = str(path) + "/output-files"
out_file = "cells-00-cotainers-00.txt"
os.chdir(path)

with open(out_file, 'w') as file:
    file.write(f'Number of solutions: {len(solutions)}\n')
    for solution in solutions:
        variables = {}
        for item in solution.items():
            variables[item[1]] = item[0]
        file.write(f'{str(variables)}\n')

