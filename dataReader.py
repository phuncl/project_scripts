"""Describe how the program works"""

import math
import glob as g
import numpy as np
import os

def get_fluxed(list, exposure):
    #is it overexposed
    max_count = float(list[-1])
    if max_count <= 45000:
        #convert counts into flux
        flux = (max_count)/float(exposure)
        return flux

def arraysplitter(arrayname):
    bjd_list = []
    object_list = []
    data_list = []

    # Open the data file
    datafile = open(filename, 'r')
    for line in datafile:
        newline = line.split('  ')
        bjd_list.append(float(newline[0]))
        object_list.append(str(newline[1]))
        data_list.append(newline[2:])

    return bjd_list,object_list,data_list



"""
filename = '/media/sf_LinuxShare/CSVcheck/Testtest.txt'
a,b,c = arraysplitter(filename)
print(a)
print(b)
print(c)

for entry in c:
    result = get_fluxed(entry,1)
    print(result)
"""