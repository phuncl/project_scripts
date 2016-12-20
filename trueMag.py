"""TrueMag = RawMag - Intercept - (Slope * Colour(eg B-R) - (Attenuation * Airmass)"""

import time
import os
import csv
import glob as g
import numpy as np


def instr_mag(flux):
    """calculate the instrumental magnitude using flux"""
    mag = np.log10(float(flux)) * -2.5
    return mag


ATMOSPHERECONSTANTS = {'B': 0.2283, 'V': 0.1120, 'R': 0.0914, 'I': 0.0197}

os.chdir('/media/sf_LinuxShare/CSVcheck/CombinedData/Science')

ALL_FILES = g.glob('median*')

print('Files are being sorted...')
time.sleep(2)

# open calibration files to read
os.chdir('/media/sf_LinuxShare/CSVcheck/CombinedData/Standards')

B_CALIBRATION = open('B_Filter_Calibration.csv', 'r')
V_CALIBRATION = open('V_Filter_Calibration.csv', 'r')
R_CALIBRATION = open('R_Filter_Calibration.csv', 'r')
I_CALIBRATION = open('I_Filter_Calibration.csv', 'r')

# Read the calibration files and put the data in a list
# to work with

B_CAL = csv.reader(B_CALIBRATION, dialect='excel')

LINE_NUMBER = 1
for rowB in B_CAL:
    if LINE_NUMBER == 1:
        LINE_NUMBER += 1

    else:
        B_cal_list = rowB

V_CAL = csv.reader(V_CALIBRATION, dialect='excel')

LINE_NUMBER = 1
for rowV in V_CAL:
    if LINE_NUMBER == 1:
        LINE_NUMBER += 1

    else:
        V_cal_list = rowV

R_CAL = csv.reader(R_CALIBRATION, dialect='excel')

LINE_NUMBER = 1
for rowR in R_CAL:
    if LINE_NUMBER == 1:
        LINE_NUMBER += 1

    else:
        R_cal_list = rowR

I_CAL = csv.reader(I_CALIBRATION, dialect='excel')

LINE_NUMBER = 1
for rowI in I_CAL:
    if LINE_NUMBER == 1:
        LINE_NUMBER += 1

    else:
        I_cal_list = rowI

# now have a list of slope, intercept, rvalue, pvalue, stderror for each filter
# called B_cal_list, V_cal_list etc

os.chdir('/media/sf_LinuxShare/CSVcheck/CombinedData/Science')

for scienceobject in ALL_FILES:

    viewfile1 = open(scienceobject, 'r')
    # reads each line of file
    viewascsv1 = csv.reader(viewfile1, dialect='excel')
    # skips header line
    next(viewascsv1)

    writehere = open('truemags_' + scienceobject[8:], 'w')
    writer = csv.writer(writehere)
    writer.writerow(['#Name', 'Filter', 'True Magnitude'])

    starname = scienceobject[8:-4]

    print('Analysing', starname)
    # get magnitude for each filter from flux in each filter
    object_mags = []
    for line1 in viewascsv1:
        if str(line1[0]) == '-1':
            object_mags.append('NoData')
        # create a list with raw mag for each filter, order B V R I
        object_mags.append(float(instr_mag(line1[-2])))

    viewfile1.close()

    viewfile = open(scienceobject, 'r')
    viewascsv = csv.reader(viewfile, dialect='excel')
    next(viewascsv)

    for line in viewascsv:

        # for a filter, calculate the true magnitude
        # temp1 = Raw - Offset - (Slope * Colour) <-- B-R and V-I used
        # temp2 = Atmosphere Attenuation * Airmass

        if str(line[-1]) == '-1':
            continue

        elif line[-1] == 'B':
            try:
                temp1 = object_mags[0] - float(B_cal_list[1]) - \
                        (float(B_cal_list[0]) * ((object_mags[0]) - object_mags[2]))
                temp2 = (ATMOSPHERECONSTANTS['B'] * float(line[8]))
                true_magnitude = temp1 - temp2
            except:
                true_magnitude = 'nan'
                print('No B or R data')

        elif line[-1] == 'V':
            try:
                temp1 = object_mags[1] - float(V_cal_list[1]) - \
                        (float(V_cal_list[0]) * (object_mags[3] - object_mags[1]))
                temp2 = (ATMOSPHERECONSTANTS['V'] * float(line[8]))
                true_magnitude = temp1 - temp2
            except:
                true_magnitude = 'nan'
                print('No V or I data')

        elif line[-1] == 'R':
            try:
                temp1 = object_mags[2] - float(R_cal_list[1]) - \
                        (float(R_cal_list[0]) * (object_mags[0] - object_mags[2]))
                temp2 = (ATMOSPHERECONSTANTS['R'] * float(line[8]))
                true_magnitude = temp1 - temp2
            except:
                true_magnitude = 'nan'
                print('No B or R data')

        elif line[-1] == 'I':
            try:
                temp1 = object_mags[3] - float(I_cal_list[1]) - \
                        (float(I_cal_list[0]) * (object_mags[3] - object_mags[1]))
                temp2 = (ATMOSPHERECONSTANTS['I'] * float(line[8]))
                true_magnitude = temp1 - temp2
            except:
                true_magnitude = 'nan'
                print('No V or I data')

        else:
            print('Oops, something went wrong! Invalid filter name, exiting...')
            break

        templist = [starname, line[-1], true_magnitude]
        print(templist)
        writer.writerow(templist)

    print('File written for', scienceobject)

    writehere.close()
    viewfile.close()

print('Program complete. Exiting...')
