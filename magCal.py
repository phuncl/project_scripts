"""
Take presorted data and work out the unknowns of equation
to map onto standard magnitude scale for each filter by
using linear regression on the data for each filter separately
"""

# pylint: disable-msg=C0103
import os
import csv
import time
import glob as g
import numpy as np
from scipy import stats
from matplotlib import pyplot

# Estimate peak wavelengths:  => Extinction (mag/airmass)
#
# B ---> 425nm              0.2283
# V ---> 520nm              0.1120
# R ---> 585nm              0.0914
# I ---> 775nm              0.0197

ATMOSPHERECONSTANTS = {'B': 0.2283, 'V': 0.1120, 'R': 0.0914, 'I': 0.0197}
FILTERCOLUMNINDEX = {'B': 1, 'V': 2, 'R': 3, 'I': 4}

STANDARD_DICT = {}
# here have x as a 2d array with 2 columns, one that has "raw mag - standard mag -colourconst*airmass
# of a particular colour as the first column and (B-R) as the second column
# (or whatever colour is needed).


def calibrate(xlist, ylist):
    """Hand 2 lists to plot"""
    slope, intercept, r_value, p_value, std_err = stats.linregress(xlist, ylist)
    return slope, intercept, r_value, p_value, std_err


def instr_mag(flux):
    """calculate the instrumental magnitude using flux"""
    mag = np.log10(flux) * -2.5
    return mag


def lhs(rawmagnitude, stdmag, colourconst, air_mass):
    """Left hand side of the conversion equation"""
    return float(rawmagnitude) - float(stdmag) - (float(colourconst) * float(air_mass))


def rhs(colour1, colour2):
    """Right hand side of the conversion equation"""
    return float(colour1) - float(colour2)


# create lists for axis data

X_AXIS_B = []
Y_AXIS_B = []

X_AXIS_R = []
Y_AXIS_R = []

X_AXIS_V = []
Y_AXIS_V = []

X_AXIS_I = []
Y_AXIS_I = []

os.chdir('/media/sf_LinuxShare/CSVcheck/CombinedData/Standards')
# Change CSVcheck to data/20161009 when ready

# obtain list of standards to get info from
ALL_STANDARDS = g.glob('sorted*')

print('Files are being sorted into a list...')
time.sleep(0.5)

# read csv file into a dictionary with keys as the star names
FILENAME = open('ing_standards.csv', 'r')
CATALOGUE = csv.reader(FILENAME, dialect='excel')
print('Collecting standard star data...')
time.sleep(0.5)

# fill standard dict with data
for line in CATALOGUE:
    STANDARD_DICT[line[5]] = line[:5]
    # create dictionary of standards, standard name maps to list of data

FILENAME.close()
# above dictionary works correctly

print('Beginning analysis of standard star data...')
time.sleep(0.5)

# each viewing will have different exposure times and different filters in there in lines
for viewing in ALL_STANDARDS:

    # open the datafile of the observed standard object
    readfile = open(viewing, 'r')
    readascsv = csv.reader(readfile, dialect='excel')
    next(readascsv)
    for line in readascsv:
        # impose a hard limit on maximum and minimum flux to get rid of bad data
        fluxx = float(line[-2])

        if 100 < fluxx < 6000:

            # convert line into a list
            # print(line)
            rawmag = instr_mag(float(line[-2]))
            # this column is the flux, which we convert to mag here using instr_mag
            # print(linedata[-2])  # check this is flux
            # print(linedata[-1][0])  # check this is a filter
            airmass = line[8]
            colourconstant = ATMOSPHERECONSTANTS[line[-1][0]]
            # [0] to avoid \n included in string
            # print(colourconstant)  # check this is attenuation of atmosphere for each filter

            # string manipulation to extract name of the standard currently being analysed
            rawname = viewing.split('.')[0]  # takes off csv extension
            splitrawname = rawname.split('_')
            standardname = splitrawname[-2] + '_' + splitrawname[-1]
            # print(standardname)  # check this gives a valid standard name
            filtername = line[-1][0]  # [0] to avoid \n again
            # print(filter)
            # find the standard star in the landolt standards dataframe pandas has created
            # Find relevant matrix element from knowing star name and filter, extract
            column = FILTERCOLUMNINDEX[filtername]
            # find row of particular standard star and
            # retrieve element corresponding to correct filter.

            datarow = STANDARD_DICT[standardname]

            stdmagnitude = datarow[column]

            if filtername == 'B':
                X_AXIS_B.append(rhs(datarow[1], datarow[3]))
                Y_AXIS_B.append(lhs(rawmag, stdmagnitude, colourconstant, airmass))
                print('Data for', standardname, 'added to', filtername, 'filter data')

            elif filtername == 'R':
                X_AXIS_R.append(rhs(datarow[1], datarow[3]))
                Y_AXIS_R.append(lhs(rawmag, stdmagnitude, colourconstant, airmass))
                print('Data for', standardname, 'added to', filtername, 'filter data')

            elif filtername == 'V':
                X_AXIS_V.append(rhs(datarow[4], datarow[2]))
                Y_AXIS_V.append(lhs(rawmag, stdmagnitude, colourconstant, airmass))
                print('Data for', standardname, 'added to', filtername, 'filter data')

            elif filtername == 'I':
                X_AXIS_I.append(rhs(datarow[4], datarow[2]))
                Y_AXIS_I.append(lhs(rawmag, stdmagnitude, colourconstant, airmass))
                print('Data for', standardname, 'added to', filtername, 'filter data')

            else:
                print('Something has gone wrong, filter name invalid, exiting...')
                break

            time.sleep(0.05)
    readfile.close()

time.sleep(0.5)
print('All data for plotting acquired, analysing plots...')

# now do linear regression on all the data pairs and write to file (CSV)
slope_B, intercept_B, r_value_B, p_value_B, std_err_B = calibrate(X_AXIS_B, Y_AXIS_B)
slope_V, intercept_V, r_value_V, p_value_V, std_err_V = calibrate(X_AXIS_V, Y_AXIS_V)
slope_R, intercept_R, r_value_R, p_value_R, std_err_R = calibrate(X_AXIS_R, Y_AXIS_R)
slope_I, intercept_I, r_value_I, p_value_I, std_err_I = calibrate(X_AXIS_I, Y_AXIS_I)

# make these values into a list so it can be easily written into a csv
B_LIST = [slope_B, intercept_B, r_value_B, p_value_B, std_err_B]
V_LIST = [slope_V, intercept_V, r_value_V, p_value_V, std_err_V]
R_LIST = [slope_R, intercept_R, r_value_R, p_value_R, std_err_R]
I_LIST = [slope_I, intercept_I, r_value_I, p_value_I, std_err_I]

# iterate through above lists
LIST_OF_ALL_LISTS = [B_LIST, V_LIST, R_LIST, I_LIST]

FILTER_LIST = ['B', 'V', 'R', 'I']
# save these values to a CSV file
for i in range(1, 5):
    filename = FILTER_LIST[i-1] + '_Filter_Calibration.csv'
    openfile = open(filename, 'w')
    print('Writing', FILTER_LIST[i-1], 'filter data to file')
    writer = csv.writer(openfile, delimiter=',')
    writer.writerow(['#Slope', 'Intercept', 'R Value', 'P Value', 'Standard Error'])
    writer.writerow(LIST_OF_ALL_LISTS[i-1])
    time.sleep(0.5)

    openfile.close()

# create plots of each filter data
pyplot.plot(X_AXIS_I, Y_AXIS_I, 'ro')
pyplot.xlabel('I-V')
pyplot.ylabel('Magnitude')
pyplot.show()

print('Science has been successful, please continue this trend!')
