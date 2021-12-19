#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from constraint import *
import sys
import os

# ------------------------------------
# PARAMETERS
# ------------------------------------
pathDataDirectory = 'parte-1/CSP-tests'
mapFileName = 'map1'
containerFileName = 'containers1'

if len(sys.argv) > 1:
    print(str(sys.argv))
    pathDataDirectory = sys.argv[1]
    mapFileName = sys.argv[2]
    containerFileName = sys.argv[3]

pathMapFile = os.path.join(pathDataDirectory, mapFileName)
pathContainerFile = os.path.join(pathDataDirectory, containerFileName)

problem = Problem()


# ------------------------------------
# Data loading
# ------------------------------------
def starting_up(map_bay, containers_list):
    map_file = open(map_bay, "r")
    map_file = map_file.read().splitlines()

    for i in range(len(map_file)):
        map_file[i] = map_file[i].split(' ')

    containers_file = open(containers_list, "r")
    containers_file = containers_file.read().splitlines()
    containers_dictionary = {}
    for i in range(len(containers_file)):
        containers_file[i] = containers_file[i].split(' ')
        containers_dictionary[containers_file[i][0]] = containers_file[i][1:]

    return map_file, containers_dictionary


map_file, containers_dictionary = starting_up(pathMapFile, pathContainerFile)
type_mapping = {'N': ["S"], "E": ["S", "R"], "X": ['']}

print("Containers dictinonary:")
print(containers_dictionary);

# ------------------------------------
# Output of the given configuration
# ------------------------------------
print("\nShip configuration:")
for row in map_file:
    print(row)

print("\nContainer to load:")
for container in containers_dictionary.items():
    print(container)

print("\nCell type to container type relation:")
for mapping in type_mapping.items():
    print(mapping)

# ------------------------------------
# Creating variables for each ship cell
# ------------------------------------
# print("\nVariables (ship cell: domain):")
i = 0
for x in range(len(map_file)):
    for y in range(len(map_file[x])):

        id_cell = (x, y)
        mapping = type_mapping[map_file[x][y]]

        domain = [map_file[x][y] + str(i)]
        for container in containers_dictionary.items():
            if container[1][0] in mapping:
                domain.append(container[0])

        problem.addVariable(id_cell, domain)
        i += 1
        print(str(id_cell) + ": " + str(domain))


# ------------------------------------
# Constraints
# ------------------------------------

# problem.addConstraint(lambda *vars: print(vars))


def containerIds(*cells):
    usedContainers = []
    for cell in cells:
        if cell.isdigit():
            usedContainers.append(cell)

    usedContainers = set(usedContainers)
    isValid = len(usedContainers) == len(containers_dictionary)
    # print(f"{usedContainers}, {isValid}")

    if not isValid:
        return False

    return True


problem.addConstraint(containerIds)

problem.addConstraint(AllDifferentConstraint())


def validateStackPair(lower, upper):
    isLowerCellUsed = lower.isdigit()
    isUpperCellUsed = upper.isdigit()

    isValid = not isUpperCellUsed or isLowerCellUsed

    # print(f"Usage | lower: {lower} upper: {upper} result: {isValid}")

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

    # print(f"Port | lower: {lowerPort} upper: {upperPort} result: {isValid}")

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

solutions = problem.getSolutions()
print(f'Number of solutions: {len(solutions)}')

path = os.path.join(pathDataDirectory, f'{mapFileName}-{containerFileName}.output')
with open(path, 'w') as file:
    file.write(f'Number of solutions: {len(solutions)}\n')
    for solution in solutions:
        variables = {}
        for item in solution.items():
            if item[1].isdigit():
                variables[item[1]] = item[0]

        file.write(f'{str(variables)}\n')
