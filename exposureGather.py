"""
Gathers data on standard stars from a data date folder and
appends it to files in exposure metre which are used for
exposure metre calculations
Program should be run from a data folder.
"""

import csv
import os
import glob as g
import numpy as np
from scipy import stats


################################################################


def get_sciencetargets():
    # Obtain science targets from text file in folder
    # useful once own data obtained
    science_targets = []
    datafile = open('science_targets.txt', 'r')
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


def mk_exposuredata(filter):
    # Cycle through all filters
    os.chdir(filter + '/')
    mag_expo_list = []

    for target in STANDARDS:
        os.chdir(target + '/')
        filelist = g.glob('sorted*')
        for fname in filelist:
            with open(fname, 'r') as fin:
                fread = csv.reader(fin)
                for line in fread:
                    std_name = line[1]
                    max_counts = float(line[-2])
                    exposure = float(line[-1])

                    if 300 < max_counts < 40000:
                        max_flux = max_counts / exposure
                        max_expo = 40000 / max_flux

                        try:
                            x = FILTERS.index(filter)
                            mag = float(STANDARD_DICT[std_name][x])
                        except KeyError:
                            print('An error occurred.\n', std_name, 'was not found in the standards star catalogue.')
                            mag = None

                        if mag:
                            mag_expo_list.append([mag, max_expo, std_name])
        os.chdir('..')

    os.chdir(EMD)
    fout_name = filter+'_exposure_data_{}.csv'.format(CWD.split('/')[-1])
    if not os.path.exists(fout_name):
        with open(fout_name, 'w') as fwr:
            writer = csv.writer(fwr)
            # write headers
            writer.writerow(['#magnitude', 'exposure', 'name'])

    with open(fout_name, 'a') as fwr:
        writer = csv.writer(fwr)
        # append data to file
        writer.writerows(mag_expo_list)

    os.chdir(CWD)

################################################################

FILTERS = ['B', 'V', 'R', 'I']

CWD = os.getcwd()
EMD = '/media/sf_LinuxShare/ExposureMetre'
if not os.path.exists(EMD):
    os.mkdir(EMD)

# get standard star catalogue into memory
os.chdir('/media/sf_LinuxShare/standards_catalogue')
STANDARD_DICT = {}
with open('ing_standards.csv', 'r') as stdin:
    catalogue = csv.reader(stdin, dialect='excel')
    for row in catalogue:
        STANDARD_DICT[row[4]] = row[:4]
    stdin.close()
    os.chdir(CWD)

# get science targets from .txt file
SCIENCE_TARGETS = get_sciencetargets()
# then get the standard objects
STANDARDS = get_standards()

print('The following standard objects have been identified:')
for i, item in enumerate(STANDARDS):
    print(item)

for flt in FILTERS:
    mk_exposuredata(flt)

print('Data harvested from this folder.')
print('Thank you for your cooperation.')