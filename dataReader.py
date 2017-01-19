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
GAIN = 1.22

# FUNCTION DEFINITIONS

def get_fluxed(list):
    # is it overexposed
    max_count = float(list[-2])
    exposure = int(list[-1])
    counts = float(list[6])

    # Carry over only appropriate data (not over- or under-exposed - minimum counts?)
    if  0 < max_count <= 40000 and counts > 0:
        # convert counts into flux
        flux = counts / float(exposure)
        return flux
    else:
        return 0


def snratio(counts, sky_background, gain):
    """
    calculate signal to noise ratio, disregarding read noise and
    dark current

    :param counts: float type, number of electrons, needs conversion
    to photons by gain division
    :param sky_background: ditto
    :param gain: number of electrons created per photon detected
    :return: object counts / noise
    """
    signal = float(counts) / float(gain)
    object_noise = np.sqrt(float(counts) / float(gain))
    background_noise = np.sqrt(float(sky_background) / float(gain))

    return signal / (object_noise + background_noise)


def instr_mag(flux):
    # Calculate the instrumental magnitude using flux
    mag = np.log10(flux) * -2.5
    return mag


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

                        headers = ['#BJD', 'OBJECT_ID', 'X', 'Y', 'RSI', 'RSO', 'COUNTS', 'COUNTS_ERR',
                                   'SKY_COUNTS', 'SKY_COUNTS_ERR', 'AIRMASS',
                                   'FLAG', 'COUNTS_MAX', 'EXPOSURE', 'FLUX', 'FILTER', 'SNR']

                        tmp_writer.writerow(headers)
                        tmp_combinedfile.close()

                    combinedfile = open(CWD + '/CombinedData/Standards/' + object, 'a')
                    combinedwriter = csv.writer(combinedfile, dialect='excel')
                    print('Opened combined file for ' + filter + '/' + name + '/' + object)

                    for line in datareader:
                        flux = get_fluxed(line)  # takes a list!
                        object_counts = line[6]
                        sky_background_counts = line[8]

                        # work out signal to noise ratio, add it to end of line
                        snr = snratio(object_counts, sky_background_counts, GAIN)

                        if flux != 0:
                            line.append(flux)
                            line.append(filter)
                            line.append(snr)

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

                        headers = ['#BJD', 'OBJECT_ID', 'X', 'Y', 'RSI', 'RSO', 'COUNTS', 'COUNTS_ERR',
                                   'SKY_COUNTS', 'SKY_COUNTS_ERR', 'AIRMASS',
                                   'FLAG', 'COUNTS_MAX', 'EXPOSURE', 'FLUX', 'FILTER', 'SNR']

                        tmp_writer.writerow(headers)
                        tmp_combinedfile.close()

                    combinedfile = open(CWD + '/CombinedData/Science/' + object, 'a')
                    combinedwriter = csv.writer(combinedfile, dialect='excel')
                    print('Opened combined file for ' + filter + '/' + name + '/' + object)

                    for line in datareader:
                        flux = get_fluxed(line)  # takes a list!
                        object_counts = line[6]
                        sky_background_counts = line[8]

                        # work out signal to noise ratio and add it to end of line
                        snr = snratio(object_counts, sky_background_counts, GAIN)

                        if flux != 0:
                            line.append(flux)
                            line.append(filter)
                            line.append(snr)

                            combinedwriter.writerow(line)
                    combinedfile.close()
                    print(object + ' complete')

            except:
                print('Some error occured!', name, 'not processed!\n')

            print(name, 'complete')
        print(filter, 'complete')
    os.chdir(CWD)
    return 0

# MAIN FUNCTION

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

if not os.path.isfile('CombinedData/Standards/ing_standards.csv'):
    print('ING standards data file not yet in the Standards folder!')

print('Exiting...')
