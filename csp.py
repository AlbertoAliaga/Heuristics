#!/usr/bin/python


import sys
import os
from constraint import *


######################## Input reading ##################################
# para correr el programa en el PC de RBN: python3 csp.py /home/rbn/pyCharmProjects/Heuristica/lab-2/Heuristics/P2 Input-cells.txt Input-cont.txt

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

'''
print(map)
print()
print(container)
print()'''

#########################  ##################################

'''
    Cada input de Input-cont.txt es una variable. Los dominios son si necesita una posición con
    energía o no (si es R la necesita, si es S no tiene por qué) y a qué puerto van
'''

problem = Problem()

# Dominio 0 = N     Dominio 1 = E       Destino X = X

# En este bucle se sacan las variables de contenedores y se asignan los dominios
for i in container:
    unit_container = i.split()
    id = unit_container[0]
    type = unit_container[1]
    destination = unit_container[2]
    #print("id = ", id, "\ttype = ", type, "\tdest = ", destination)


    if(type == "R"):
        print("Container w/ R's id = ", id)
        problem.addVariable(id, ['N', destination])
    elif (type == "S"):
        print("Container w/ S's id = ", id)
        problem.addVariable(id, ['N','E', destination])
    else:
        print("Input error. ", sys.argv[3], " contains wrong data.")


