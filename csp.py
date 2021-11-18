#!/usr/bin/python

import sys
import os
from constraint import *

######################## Input reading ##################################

path = sys.argv[1]
cells = sys.argv[2]
containers = sys.argv[3]

os.chdir(path)
cells_file_size = os.stat(str(path)+"/"+str(cells)).st_size
containers_file_size = os.stat(str(path)+"/"+str(containers)).st_size


cells = open(cells, "r")
containers = open(containers, "r")

cells = cells.read(cells_file_size)
containers = containers.read(containers_file_size)

cells = cells.split("\n")
containers = containers.split("\n")

#Cells become a reversed tuple matrix, since container height goes upwards
for i in range(0, len(cells)):
    cells[i] = tuple(cells[i].split())
cells.reverse()
cells = tuple(cells)

#Containers are represented as a tuple of tuples
for i in range(0, len(containers)):
    containers[i] = tuple(containers[i].split())
containers = tuple(containers)

print(cells, "\n")
#print(containers, "\n")

######################### Variable Assignation ##########################

problem = Problem()

