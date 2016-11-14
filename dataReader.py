"""Describe how the program works"""

import math
import glob as g
import numpy as np
import os
import time

FILTERS = ['B', 'V', 'R', 'I']
CWD = os.getcwd()

def get_fluxed(list):
    #is it overexposed
    max_count = float(list[-2])
    exposure = int(list[-1])
    if max_count <= 45000:
        #convert counts into flux
        flux = (max_count)/float(exposure)
        return flux
    else:
        return 0

def instr_mag(flux):
    mag = np.log10(flux) * -2.5
    return mag

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

def get_sciencetargets():
    science_targets = []
    datafile = open("science_targets.txt", 'r')
    for line in datafile:
        science_targets.append(line[:-1])
    datafile.close()
    return science_targets

def get_standards():
    os.chdir('R/')
    subdirectories = os.listdir('.')
    standards = []
    for entry in subdirectories:
        if '.' not in entry:
            if entry not in SCIENCE_TARGETS:
                standards.append(entry)
    os.chdir(CWD)
    return standards

def combine_standards():

    for filter in FILTERS:
        for name in STANDARDS:
            try:
                os.chdir(filter+'/'+name+'/')
                objects_list = g.glob('sorted*')
                print(objects_list)
                time.sleep(.1)
                for object in objects_list:
                    datafile = open(str(CWD + '/' + filter + '/' + name + '/' + object), 'r')
                    combinedfile = open(CWD+'/CombinedData/Standards/' + object, 'w+')
                    print('Opened combined file for' + filter + name + object)

                    for line in datafile:
                        datafromline = line.split('  ')
                        flux = get_fluxed(datafromline)
                        if flux != 0:
                            writeline = line[:-2] + '  ' + str(flux) + '  ' + filter
                            combinedfile.write(writeline)
                    combinedfile.close()
                    print(object + ' complete')
                os.chdir(CWD)
            except:
                pass
            print(name + ' complete')
        print(filter + ' complete')
    return 0
#########################################################
#########################################################
#########################################################

SCIENCE_TARGETS = get_sciencetargets()
STANDARDS = get_standards()
print('Science Targets are:',SCIENCE_TARGETS)
print('Standard objects are:',STANDARDS)
time.sleep(10)
if not os.path.exists('CombinedData'):
    os.mkdir('CombinedData')
    os.mkdir('CombinedData/Science')
    os.mkdir('CombinedData/Standards')

combine_standards()

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