"""TrueMag = RawMag - Intercept - (Slope * Colour(eg B-R) - (Attenuation * Airmass)"""

import time
import os
import glob as g
import csv
import numpy as np


def instr_mag(flux):
    """calculate the instrumental magnitude using flux"""
    if flux > 0:
        mag = np.log10(flux) * -2.5
    else:
        mag = -1
    return mag


ATMOSPHERECONSTANTS = {'B': 0.2283, 'V': 0.1120, 'R': 0.0914, 'I': 0.0197}

os.chdir('/media/sf_LinuxShare/data/20161009/CombinedData/Standards')

ALL_FILES = g.glob('median*')

print('Files are being sorted...')
time.sleep(2)

B_calibration = open('B_Filter_Calibration.csv', 'r')
V_calibration = open('V_Filter_Calibration.csv', 'r')
R_calibration = open('R_Filter_Calibration.csv', 'r')
I_calibration = open('I_Filter_Calibration.csv', 'r')

B_cal = csv.reader(B_calibration, dialect='excel')
next(B_cal)
B_cal_list = next(B_cal)

V_cal = csv.reader(V_calibration, dialect='excel')
next(V_cal)
V_cal_list = next(V_cal)

R_cal = csv.reader(R_calibration, dialect='excel')
next(R_cal)
R_cal_list = next(R_cal)

I_cal = csv.reader(I_calibration, dialect='excel')
next(I_cal)
I_cal_list = next(I_cal)

B_calibration.close()
V_calibration.close()
R_calibration.close()
I_calibration.close()

# now have a list of slope, intercept, rvalue, pvalue, stderror for each filter
# called B_cal_list, V_cal_list etc


for stdobject in ALL_FILES:

    viewfile = open(stdobject, 'r')
    # reads each line of file, except headers
    viewascsv = csv.reader(viewfile, dialect='excel')
    next(viewascsv)

    writehere = open('truemags' + stdobject[7:], 'w')
    writer = csv.writer(writehere)
    writer.writerow(['#Name', 'Filter', 'True Magnitude'])


    # get magnitude for each filter from flux in each filter
    object_mags = []

    B_line = next(viewascsv)
    V_line = next(viewascsv)
    R_line = next(viewascsv)
    I_line = next(viewascsv)

    starname = I_line[1]

    viewfile.close()

    lines = [B_line,V_line,R_line,I_line]

    for line in lines:
        object_mags.append(instr_mag(float(line[-4])))

    for line in lines:
        if line[-1] == 'B':
            temp1 = object_mags[0] - float(B_cal_list[1]) - (float(B_cal_list[0]) * (object_mags[0] - object_mags[2]))
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

        elif line[-1] == -1:
            print('Missing data for', starname, '.\n',
                  'Skipping line...')
            true_magnitude = -1

        else:
            print('Something strange has happened in', starname, 'data.\nSkipping...')
            true_magnitude = -99

        # write starname, filter, magnitude
        writer.writerow([starname, line[-1], true_magnitude])

    writehere.close()

print('All magnitudes calculated! Exiting...')