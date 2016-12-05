"""
Collection of functions that will perform photometry
on the data that we obtain from the telescope
"""

import glob as g
import numpy as np
import os
import time
import csv

# Global Constants
FILTERS = ['B', 'V', 'R', 'I']
CWD = os.getcwd()


def get_fluxed(list):
    # is it overexposed
    max_count = float(list[-2])
    exposure = int(list[-1])
    counts = float(list[6])

    # Carry over only appropriate data (not over- or under-exposed
    if  0 < max_count <= 40000:
        # convert counts into flux
        flux = counts / float(exposure)
        return flux
    else:
        return 0


def instr_mag(flux):
    # Calculate the instrumental magnitude using flux
    mag = np.log10(flux) * -2.5
    return mag


'''
def arraysplitter(filename):
    # Split data from a phot file into lists for easier use
    bjd_list = []
    object_list = []
    data_list = []
    # Open the data file
    datafile = open(filename, 'r')
    lineread = csv.reader(datafile, dialect='excel')
    for line in lineread:
        # extract data and append to appropriate list
        bjd_list.append(float(line[0]))
        object_list.append(str(line[1]))
        data_list.append(line[2:])

    return bjd_list, object_list, data_list
'''


def get_sciencetargets():
    # Obtain science targets from text file
    # useful once own data obtained
    science_targets = []
    datafile = open("science_targets.txt", 'r')
    for line in datafile:
        if line != '':
            science_targets.append(line[:-1])
    datafile.close()
    return science_targets


def get_standards():
    # Retrieve standard stars using R filter as reference
    os.chdir('R/')
    subdirectories = os.listdir('.')  # list dirs in cwd
    standards = []
    for entry in subdirectories:
        if '.' not in entry:
            if entry not in SCIENCE_TARGETS:
                standards.append(entry)
    os.chdir(CWD)
    return standards


def combine_standards():
    os.chdir(CWD)
    # Collate a standard star's data from each filter into one folder
    for filter in FILTERS:
        for name in STANDARDS:
            # exception in case all images for a standard were inadequate
            try:
                # go to standard star's directory and get list of CSV files
                os.chdir(CWD + '/' + filter + '/' + name)
                objects_list = g.glob('sorted*')

                for object in objects_list:
                    # from existing file, write data to new file, append flux and filter to end
                    datafile = open(object, 'r')
                    datareader = csv.reader(datafile, dialect='excel')
                    # skip headers
                    next(datareader)

                    # initialise files with headers
                    if not os.path.isfile(CWD + '/CombinedData/Standards/' + object):
                        tmp_combinedfile = open(CWD + '/CombinedData/Standards/' + object, 'w')
                        tmp_writer = csv.writer(tmp_combinedfile, dialect='excel')

                        headers = ['#BJD', 'OBJECT_ID', 'X', 'Y', 'RSI', 'RSO', 'COUNTS', 'COUNTS_ERR', 'AIRMASS',
                                   'FLAG', 'COUNTS_MAX', 'EXPOSURE', 'FLUX', 'FILTER']

                        tmp_writer.writerow(headers)
                        tmp_combinedfile.close()

                    combinedfile = open(CWD + '/CombinedData/Standards/' + object, 'a')
                    combinedwriter = csv.writer(combinedfile, dialect='excel')
                    print('Opened combined file for ' + filter + '/' + name + '/' + object)

                    for line in datareader:
                        flux = get_fluxed(line)  # takes a list!
                        if flux != 0:
                            line.append(flux)
                            line.append(filter)

                            combinedwriter.writerow(line)
                    combinedfile.close()
                    print(object + ' complete')

            except:
                print('Some error occured!', name, 'not processed!\n')

            print(name, 'complete')
        print(filter, 'complete')
    os.chdir(CWD)
    return 0


def combine_science():
    os.chdir(CWD)
    # Collate a science target data for each object into combined files
    for filter in FILTERS:
        for name in SCIENCE_TARGETS:
            # exception clause in case of photometry failure
            try:
                # go to directory and get list of CSV files
                os.chdir(CWD + '/' + filter + '/' + name)
                objects_list = g.glob('sorted*')

                for object in objects_list:
                    # from existing file, write data to new file, append flux and filter to end
                    datafile = open(object, 'r')
                    datareader = csv.reader(datafile, dialect='excel')
                    # skip headers
                    next(datareader)

                    # initialise files with headers
                    if not os.path.isfile(CWD + '/CombinedData/Science/' + object):
                        print('Initialising file for', object)
                        tmp_combinedfile = open(CWD + '/CombinedData/Science/' + object, 'w')
                        tmp_writer = csv.writer(tmp_combinedfile, dialect='excel')

                        headers = ['#BJD', 'OBJECT_ID', 'X', 'Y', 'RSI', 'RSO', 'COUNTS', 'COUNTS_ERR', 'AIRMASS',
                                   'FLAG', 'COUNTS_MAX', 'EXPOSURE', 'FLUX', 'FILTER']

                        tmp_writer.writerow(headers)
                        tmp_combinedfile.close()

                    combinedfile = open(CWD + '/CombinedData/Science/' + object, 'a')
                    combinedwriter = csv.writer(combinedfile, dialect='excel')
                    print('Opened combined file for ' + filter + '/' + name + '/' + object)

                    for line in datareader:
                        flux = get_fluxed(line)  # takes a list!
                        if flux != 0:
                            line.append(flux)
                            line.append(filter)
                            print(line)
                            combinedwriter.writerow(line)
                    combinedfile.close()
                    print(object + ' complete')

            except:
                print('Some error occured!', name, 'not processed!\n')

            print(name, 'complete')
        print(filter, 'complete')
    os.chdir(CWD)
    return 0


##########################################################
################ TESTING THE FUNCTION ####################
##########################################################

SCIENCE_TARGETS = get_sciencetargets()
STANDARDS = get_standards()
print('Science Targets are:', SCIENCE_TARGETS, '\n')
print('Standard objects are:', STANDARDS, '\n')
print("""
BEGINNING STANDARDS DATA ANALYSIS...
""")
time.sleep(2)
if not os.path.exists('CombinedData'):
    os.mkdir('CombinedData')
if not os.path.exists('CombinedData/Science'):
    os.mkdir('CombinedData/Science')
if not os.path.exists('CombinedData/Standards'):
    os.mkdir('CombinedData/Standards')

combine_standards()
print("""
BEGINNING SCIENCE DATA ANALYSIS...
""")
time.sleep(2)
combine_science()
print('Exiting...')