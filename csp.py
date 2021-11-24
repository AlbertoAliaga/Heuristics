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

def compareDestination(a, b):
    if a == 'R' and b == 'S' and a < b:
	    return True

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

print(id_list[1:])
print(type_list)
print(destination_list, "\n")

for id in id_list[1:]:
    id = int(id)
    problem.addConstraint(compareDestination, (type_list[id], type_list[id-1]))
    print("id: ", id, ", id-1: ", id-1)







