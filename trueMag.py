"""TrueMag = RawMag - Intercept - (Slope * Colour(eg B-R) - (Attenuation * Airmass)"""

import time
import os
import glob as g
import csv
import numpy as np


def instr_mag(flux):
    """calculate the instrumental magnitude using flux"""
    mag = np.log10(float(flux)) * -2.5
    return mag


ATMOSPHERECONSTANTS = {'B': 0.2283, 'V': 0.1120, 'R': 0.0914, 'I': 0.0197}

os.chdir('/media/sf_LinuxShare/CSVcheck/CombinedData/Science')

ALL_FILES = g.glob('sorted*')

print('Files are being sorted...')
time.sleep(2)

# open calibration files to read
os.chdir('/media/sf_LinuxShare/CSVcheck/CombinedData/Standards')

B_calibration = open('B_Filter_Calibration.csv', 'r')
V_calibration = open('V_Filter_Calibration.csv', 'r')
R_calibration = open('R_Filter_Calibration.csv', 'r')
I_calibration = open('I_Filter_Calibration.csv', 'r')

# Read the calibration files and put the data in a list
# to work with

B_cal = csv.reader(B_calibration, dialect='excel')

line_number = 1
for rowB in B_cal:
    if line_number == 1:
        line_number += 1

    else:
        B_cal_list = rowB

V_cal = csv.reader(V_calibration, dialect='excel')

line_number = 1
for rowV in V_cal:
    if line_number == 1:
        line_number += 1

    else:
        V_cal_list = rowV

R_cal = csv.reader(R_calibration, dialect='excel')

line_number = 1
for rowR in R_cal:
    if line_number == 1:
        line_number += 1

    else:
        R_cal_list = rowR

I_cal = csv.reader(I_calibration, dialect='excel')

line_number = 1
for rowI in I_cal:
    if line_number == 1:
        line_number += 1

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

    writehere = open('truemags_' + scienceobject[7:], 'w')
    writer = csv.writer(writehere)
    writer.writerow(['#Name', 'Filter', 'True Magnitude'])

    starname = scienceobject[7:-4]

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
        # NEXT STEP - WRITE TRUE MAGNITUDES TO A LIST AND SAVE TO CSV!!!

        if line[-1] == 'B':
            temp1 = object_mags[0] - float(B_cal_list[1]) - (float(B_cal_list[0]) * ((object_mags[0]) - object_mags[2]))
            temp2 = (ATMOSPHERECONSTANTS['B'] * float(line[8]))
            true_magnitude = temp1 - temp2

        elif line[-1] == 'V':
            temp1 = object_mags[1] - float(V_cal_list[1]) - (float(V_cal_list[0]) * (object_mags[1] - object_mags[3]))
            temp2 = (ATMOSPHERECONSTANTS['V'] * float(line[8]))
            true_magnitude = temp1 - temp2

        elif line[-1] == 'R':
            temp1 = object_mags[2] - float(R_cal_list[1]) - (float(R_cal_list[0]) * (object_mags[0] - object_mags[2]))
            temp2 = (ATMOSPHERECONSTANTS['R'] * float(line[8]))
            true_magnitude = temp1 - temp2

        elif line[-1] == 'I':
            temp1 = object_mags[3] - float(I_cal_list[1]) - (float(I_cal_list[0]) * (object_mags[1] - object_mags[3]))
            temp2 = (ATMOSPHERECONSTANTS['I'] * float(line[8]))
            true_magnitude = temp1 - temp2

        elif str(line[-1]) == '-1':
            continue

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
