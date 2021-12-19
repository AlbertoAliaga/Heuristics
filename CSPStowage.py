#!/usr/bin/python
# import string
import sys
import os
from constraint import *

# ####################### Input reading ##################################
# In order to run this code on Linux: python3 csp.py /home/rbn/pyCharmProjects/Heuristica/lab-2/Heuristics/input-files cells-00.txt containers-00.txt
# python3 CSPStowage.py ./input-files cells-00.txt containers-00.txt

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

# https://www.studytonight.com/python-howtos/pass-a-list-to-a-function-to-act-as-multiple-arguments

for aa in cells:
    print("aa, ", cells.index(aa), "aa+num_stacks", cells.index(aa) + num_stacks)


def checkCellOrder(a, b, *vars):
    if a in bottomCells:
        return True

    for v in vars:
        if v != a and v == a + num_stacks:
            return True

    return False


# ############################COPIADO#########################################################
'''
def validateStackPair(lower, upper):
    isLowerCellUsed = lower.isdigit()
    isUpperCellUsed = upper.isdigit()

    isValid = not isUpperCellUsed or isLowerCellUsed

    #print(f"Usage | lower: {lower} upper: {upper} result: {isValid}")

    if not isValid:
        return False
    return True

def validatePortPair(lower, upper):
        lowerPort = 0
        upperPort = 0

        if lower.isdigit():
            lowerPort = int(containers_dictionary[lower][1])

        if (upper.isdigit()):
            upperPort = int(containers_dictionary[upper][1])

        isValid = lowerPort >= upperPort

        #print(f"Port | lower: {lowerPort} upper: {upperPort} result: {isValid}")

        if not isValid:
            return False
        return True

# Creates a constraints for each cell pair
for column in range(len(map_file[0])):
    for row in reversed(range(len(map_file) - 1)):
        if (map_file[row + 1][column] != "X"):
            lowerCell = (row + 1, column)
            upperCell = (row, column)
            problem.addConstraint(validateStackPair, [lowerCell, upperCell])
            problem.addConstraint(validatePortPair, [lowerCell, upperCell])
'''
# ############################COPIADO########################################################
'''
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

    # return bl
    # END FUNCTION
'''


def checkCells(*variables):
    # ii = 0
    # jj = 1
    # ll = len(variables)
    ret = False
    '''
    while ii < ll:
        while jj < ll:
            # print("ii == ", ii, " jj == ", jj)
            # if destination_list[ii] > destination_list[jj]:
            if checkCellOrder(variables[ii], variables[jj], *variables):
                ret = True
            jj += 1
        ii += 1
        jj = ii + 1
    '''
    for ii in variables:
        for jj in variables:
            if ii != jj:
                if checkCellOrder(ii, jj, *variables):
                    ret = True
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

problem.addConstraint(checkCells)

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
