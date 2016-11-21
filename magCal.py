import numpy as np
import math
from scipy import stats
from /media/sf_LinuxShare/codes/project_scripts/dataReader.py import instr_mag

import os

#here have x as a 2d array with 2 columns, one that has "raw mag - standard mag -0.263*airmass
#of a particular colour as the first column and (B-R) as the second column
#(or whatever colour is needed).
def calibrate(x, y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return slope, intercept, r_value, p_value, std_err

"""raw mag - standard mag - 0.263*airmass = sensitivity * (B-R) + offset """

def LHS(rawmag, stdmag, colourconstant, airmass):
    return rawmag - stdmag - (colourconstant * airmass)

def RHS(colour1, colour2):
    return colour1 - colour2

slope, intercept, r_value, p_value, std_err = calibrate('RHS', 'LHS') #get an array for this from data



