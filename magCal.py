import numpy as np
import math
from scipy import stats
import os
import glob as g
import pandas

ATMOSPHERECONSTANTS = {'B': 0.2, 'V': 0.2, 'R': 0.2, 'I': 0.2} #change these to correct values!
FILTERCOLUMNINDEX = {'B': 1, 'V': 2, 'R': 3, 'I': 4}

#here have x as a 2d array with 2 columns, one that has "raw mag - standard mag -0.263*airmass
#of a particular colour as the first column and (B-R) as the second column
#(or whatever colour is needed).
def calibrate(x, y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return slope, intercept, r_value, p_value, std_err

"""raw mag - standard mag - 0.263*airmass = sensitivity * (B-R) + offset """

def instr_mag(flux):
    """calculate the instrumental magnitude using flux"""
    mag = np.log10(flux) * -2.5
    return mag

def LHS(rawmag, stdmag, colourconstant, airmass):
    return rawmag - stdmag - (colourconstant * airmass)

def RHS(colour1, colour2):
    return colour1 - colour2


slope, intercept, r_value, p_value, std_err = calibrate('RHS', 'LHS') #get an array for this from data

x[]
y[]

os.chdir('/media/sf_LinuxShare/CSVcheck/CombinedData/Standards') #Change CSVcheck to data/20161009 when ready

#obtain list of standards to get info from
all_standards = g.glob('sorted*')

#each viewing will have different exposure times and different filters in there in lines
for viewing in all_standards:

    #open the datafile of the observed standard object
    readfile = open(viewing, 'r')

    #open the list of Landolt Faint Standards to eventually extract standard magnitudes
    readstandards = pandas.read_csv(filepath=ing_standards, skip_blank_lines=True)

    for line in readfile:
        #convert line into a list
        linedata = line.split('  ')
        rawmag = instr_mag(linedata[-2]) #this column is the flux, which we convert to mag here
        print(linedata[-2])
        airmass = linedata[8]
        colourconstant = ATMOSPHERECONSTANTS[linedata[-1]]

        #string manipulation to extract name of the standard currently being analysed
        rawname = viewing.split('.')[0]  #takes off csv extension
        splitrawname = rawname.split('_')
        standardname = splitrawname[-2] + '_' + splitrawname[-1]
        print(standardname)
        filter = linedata[-1]

        #find the standard star in the landolt standards dataframe pandas has created
        #Find relevant matrix element from knowing star name and filter, extract
        column = FILTERCOLUMNINDEX[filter]
        #find row of particular standard star and retrieve element corresponding to correct filter.
        magrow = readstandards.loc[[standardname]]
        magelement = magrow[column]
        


