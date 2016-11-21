"""
Collection of functions that will perform photometry
on the data that we obtain from the telescope
"""

import glob as g
import numpy as np
import os
import time

#Global Constants
FILTERS = ['B', 'V', 'R', 'I']
CWD = os.getcwd()

def get_fluxed(list):
    #is it overexposed
    max_count = float(list[-2])
    exposure = int(list[-1])
    counts = float(list[6])
    if max_count <= 45000:
        # convert counts into flux
        flux = counts/float(exposure)
        return flux
    else:
        return 0

def instr_mag(flux):
    """calculate the instrumental magnitude using flux"""
    mag = np.log10(flux) * -2.5
    return mag

def arraysplitter(filename):
    """Split data from a phot file into lists for easier use"""
    bjd_list = []
    object_list = []
    data_list = []
    # Open the data file
    datafile = open(filename, 'r')
    for line in datafile:
        #extract data and append to appropriate list
        newline = line.split('  ')
        bjd_list.append(float(newline[0]))
        object_list.append(str(newline[1]))
        data_list.append(newline[2:])

    return bjd_list,object_list,data_list

def get_sciencetargets():
    """Obtain science targets from text file
    useful once own data obtained"""
    science_targets = []
    datafile = open("science_targets.txt", 'r')
    for line in datafile:
        if line != '':
            science_targets.append(line[:-1])
    datafile.close()
    return science_targets

def get_standards():
    """Retrieve standard stars using R filter as reference"""
    os.chdir('R/')
    subdirectories = os.listdir('.') #list dirs in cwd
    standards = []
    for entry in subdirectories:
        if '.' not in entry:
            if entry not in SCIENCE_TARGETS:
                standards.append(entry)
    os.chdir(CWD)
    return standards

def combine_standards():
    """Collate a standard star's data from each filter into one folder"""
    for filter in FILTERS:
        for name in STANDARDS:
            #exception in case all images for a standard were inadequate
            try:
                #go to standard star's directory and get list of CSV files
                os.chdir(filter+'/'+name+'/')
                objects_list = g.glob('sorted*')
                print(objects_list)
                time.sleep(.1)
                for object in objects_list:
                    #from existing file, write data to new file, append flux and filter to end
                    datafile = open(str(CWD + '/' + filter + '/' + name + '/' + object), 'r')
                    combinedfile = open(CWD+'/CombinedData/Standards/' + object, 'a')
                    print('Opened combined file for ' + filter + '/' + name + '/' + object)

                    for line in datafile:
                        datafromline = line.split('  ')
                        flux = get_fluxed(datafromline) #takes a list!
                        if flux != 0:
                            #caution, get rid of endline characters in line
                            writeline = line[:-1] + '  ' + str(flux) + '  ' + filter + '\r\n'
                            combinedfile.write(writeline)
                    combinedfile.close()
                    print(object + ' complete')
                os.chdir(CWD)
            except:
                pass
            print(name + ' complete')
        print(filter + ' complete')
    return 0

def combine_science():
    """Collate data for all science objects into combined files"""
    for filter in FILTERS:
        for name in SCIENCE_TARGETS:
            # exceptions in case files do not exist
            try:
                os.chdir(filter+'/'+name+'/')
                objects_list = g.glob('sorted*')
                for object in objects_list:
                    # from existing file, write data to new file, append flux and filter to end
                    datafile = open(str(CWD + '/' + filter + '/' + name + '/' + object), 'r')
                    combinedfile = open(CWD + '/CombinedData/Science/' + object, 'a')
                    print('Opened combined file for ' + filter + '/' + name + '/' + object)

                    for line in datafile:
                        datafromline = line.split('  ')
                        flux = get_fluxed(datafromline)  # takes a list!
                        if flux != 0:
                            # caution, get rid of endline characters in line
                            writeline = line[:-1] + '  ' + str(flux) + '  ' + filter + '\r\n'
                            combinedfile.write(writeline)
                    combinedfile.close()
                    print(object + ' complete')
                os.chdir(CWD)
            except:
                print(object, ' was not found.\nPhotometry may have failed for this object.')
            print(name + ' complete')
        print(filter + ' complete')
    return 0


##########################################################
################ TESTING THE FUNCTION ####################
##########################################################

SCIENCE_TARGETS = get_sciencetargets()
STANDARDS = get_standards()
print('Science Targets are:',SCIENCE_TARGETS)
print('Standard objects are:',STANDARDS)
time.sleep(5)
if not os.path.exists('CombinedData'):
    os.mkdir('CombinedData')
    os.mkdir('CombinedData/Science')
    os.mkdir('CombinedData/Standards')

combine_standards()
print("""

BEGINNING SCIENCE DATA ANALYSIS...

""")
time.sleep(5)
combine_science()

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