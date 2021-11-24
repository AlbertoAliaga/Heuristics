#!/usr/bin/python


import sys
import os
from constraint import *
import itertools


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

# List with the cartesian product of all possible types of cells and destination ports
domain = []
for i in itertools.product(['N','E'], list(range(1, max(destination_list)+1))):
    domain.append(i)
print("Domain: ")
print(domain)

#
for elem in container:
    if(type_list[index] == "S"):
        for i in domain:
            print("Container w/ S's id = ", id)
            problem.addVariable(id, ['N'])
            problem.addVariable(id, [destination_list[index]])
    elif(type_list[index] == "R"):
        for
            print("Container w/ R's id = ", id)
            problem.addVariable(id, domain)
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
for id in range(0, len(id_list)):
    a = destination_list[id]
    for id_iter in range(id+1, len(id_list)):
        #print(type_list[id_iter])
        b = destination_list[id_iter]
        #problem.addConstraint(compareDestination, (a, b))

solutions = problem.getSolutions()







