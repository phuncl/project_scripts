import numpy as np
from scipy import stats
import os
import glob as g
import csv

# Estimate peak wavelengths:  => Extinction (mag/airmass)
#
# B ---> 425nm              0.2283
# V ---> 520nm              0.1120
# R ---> 585nm              0.0914
# I ---> 775nm              0.0197

ATMOSPHERECONSTANTS = {'B': 0.2283, 'V': 0.1120, 'R': 0.0914, 'I': 0.0197}
FILTERCOLUMNINDEX = {'B': 1, 'V': 2, 'R': 3, 'I': 4}

STANDARD_DICT = {}
# here have x as a 2d array with 2 columns, one that has "raw mag - standard mag -0.263*airmass
# of a particular colour as the first column and (B-R) as the second column
# (or whatever colour is needed).


def calibrate(x, y):
    """Hand 2 lists to plot"""
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return slope, intercept, r_value, p_value, std_err


def instr_mag(flux):
    """calculate the instrumental magnitude using flux"""
    mag = np.log10(flux) * -2.5
    return mag


def lhs(rawmag, stdmag, colourconstant, airmass):
    return float(rawmag) - float(stdmag) - (float(colourconstant) * float(airmass))


def rhs(colour1, colour2):
    return float(colour1) - float(colour2)


# slope, intercept, r_value, p_value, std_err = calibrate(xaxis_B, yaxis_B) #get an array for this from data
# repeat for other colours (write to file perhaps?)

xaxis_B = []
yaxis_B = []

xaxis_R = []
yaxis_R = []

xaxis_V = []
yaxis_V = []

xaxis_I = []
yaxis_I = []

os.chdir('/media/sf_LinuxShare/CSVcheck/CombinedData/Standards')  # Change CSVcheck to data/20161009 when ready

# obtain list of standards to get info from
all_standards = g.glob('sorted*')

# read csv file into a dictionary with keys as the star names
filename = open('ing_standards.csv', 'r')
catalogue = csv.reader(filename, dialect='excel')

for line in catalogue:
    STANDARD_DICT[line[5]] = line[:5]   # create dictionary of standards, standard name maps to list of data

# above dictionary works correctly

# each viewing will have different exposure times and different filters in there in lines
for viewing in all_standards:

    # open the datafile of the observed standard object
    readfile = open(viewing, 'r')

    for line in readfile:
        # convert line into a list
        linedata = line.split('  ')
        rawmag = instr_mag(float(linedata[-2]))  # this column is the flux, which we convert to mag here using instr_mag
        # print(linedata[-2])  # check this is flux
        # print(linedata[-1][0])  # check this is a filter
        airmass = linedata[8]
        colourconstant = ATMOSPHERECONSTANTS[linedata[-1][0]]     # [0] to avoid \n included in string
        # print(colourconstant)  # check this is attenuation of atmosphere for each filter

        # string manipulation to extract name of the standard currently being analysed
        rawname = viewing.split('.')[0]  # takes off csv extension
        splitrawname = rawname.split('_')
        standardname = splitrawname[-2] + '_' + splitrawname[-1]
        # print(standardname)  # check this gives a valid standard name
        filter = linedata[-1][0]  # [0] to avoid \n again
        # print(filter)
        # find the standard star in the landolt standards dataframe pandas has created
        # Find relevant matrix element from knowing star name and filter, extract
        column = FILTERCOLUMNINDEX[filter]
        # find row of particular standard star and retrieve element corresponding to correct filter.

        datarow = STANDARD_DICT[standardname]

        stdmagnitude = datarow[column]

        if filter == 'B':
            xaxis_B.append(rhs(datarow[1], datarow[3]))
            yaxis_B.append(lhs(rawmag, stdmagnitude, colourconstant, airmass))

        elif filter == 'R':
            xaxis_R.append(rhs(datarow[1], datarow[3]))
            yaxis_R.append(lhs(rawmag, stdmagnitude, colourconstant, airmass))

        elif filter == 'V':
            xaxis_V.append(rhs(datarow[2], datarow[4]))
            yaxis_V.append(lhs(rawmag, stdmagnitude, colourconstant, airmass))

        elif filter == 'I':
            xaxis_I.append(rhs(datarow[2], datarow[4]))
            yaxis_I.append(lhs(rawmag, stdmagnitude, colourconstant, airmass))

        else:
            print('Something has gone wrong, filter name invalid, exiting...')
            break


# now do linear regression on all the data pairs and write to file (CSV)