#!/usr/bin/python


import sys
import os
from constraint import *


######################## Input reading ##################################
# In order to run this code on Linux: python3 csp.py /home/rbn/pyCharmProjects/Heuristica/lab-2/Heuristics/P2 Input-cells.txt Input-cont.txt

path = sys.argv[1]
map = sys.argv[2]
container = sys.argv[3]

os.chdir(path)
map_file_size = os.stat(str(path)+"/"+str(map)).st_size
container_file_size = os.stat(str(path)+"/"+str(container)).st_size


map = open(map, "r")
container = open(container, "r")

map = map.read(map_file_size)
container = container.read(container_file_size)

map = map.split("\n")
container = container.split("\n")

#########################  ##################################

'''
    Each input on Input-cont.txt is a variable. The domains indicate whether it needs a power
    supplied cell or not (if it is an R type container it is needed) and their port destination.
'''

problem = Problem()

# Domain 0 = N     Domain 1 = E       Destination X = X    

# One list per field on container
id_list = []
type_list = []
destination_list = []

# This loop takes variables from the containers and assigns domains 
for elem in container:
    index = container.index(elem)
    container[index] = elem.split()      # List with separated elements from container list
    id_list.append(int(container[index][0]))
    type_list.append(container[index][1])
    destination_list.append(int(container[index][2]))
    #print("id = ", id, "\ttype = ", type, "\tdest = ", destination)

    id = id_list[index]     #Aux var to avoid memory accesses

    if(type_list[index] == "S"):
        print("Container w/ S's id = ", id)
        problem.addVariable(id, ['N', destination_list[index]])
    elif(type_list[index] == "R"):
        print("Container w/ R's id = ", id)
        problem.addVariable(id, ['N','E', destination_list[index]])
    else:
        print("Input error. ", sys.argv[3], " contains wrong data.")

print(id_list)
print(type_list)
print(destination_list, "\n")

def compareDestination(a, b):
    if a < b:
	    return True

# This loop iterates over each container and compares its destination to all others
for id in range(0, len(id_list)):
    a = destination_list[id]
    for id_iter in range(0, len(id_list)):
        print(type_list[id_iter])
        for dest in range(1, max(destination_list)):
            if id != id_iter and a != dest:
                b = destination_list[id_iter]
                problem.addConstraint(compareDestination, (a, b))

#print(problem.getSolution())







