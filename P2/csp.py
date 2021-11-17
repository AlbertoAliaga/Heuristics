#!/usr/bin/python

import sys
import os

######################## Input reading ##################################

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

print(map)
print("\t")
print(container)
print("\t")

#########################  ##################################
