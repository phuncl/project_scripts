"""
For all standard stars, find single magnitude for each filter
compare to the catalogue mag and calculate zero point magnitude
"""

import os
import csv
import numpy as np
import math

os.chdir('CombinedData/Standards')

def isnum(x):
    try:
        float(x)
        return True
    except:
        return False


# read zero_magnitude_data.csv into program
ZPdata = open('zero_magnitude_data.csv', 'r')
ZPreader = csv.reader(ZPdata)

next(ZPreader)

Bvals = []
Vvals = []
Rvals = []
Ivals = []

vals = [Bvals,Vvals,Rvals,Ivals]

for line in ZPreader:
    if not math.isnan(float(line[1])):
        Bvals.append(float(line[1]))

    if not math.isnan(float(line[2])):
        Vvals.append(float(line[2]))

    if not math.isnan(float(line[3])):
        Rvals.append(float(line[3]))

    if not math.isnan(float(line[4])):
        Ivals.append(float(line[4]))

ZPdata.close()

# now take average value for data in each filter
# and output to zero_magnitude_values.csv

outfile = open('zero_magnitude_values.csv', 'w')
outwrite = csv.writer(outfile)
HEADERS = ['#B', 'V', 'R', 'I']
outwrite.writerow(HEADERS)

outdata = []

for filterdata in vals:
    average = np.average(filterdata)
    median = np.median(filterdata)

    print('Average value:', average, '\n')
    print('Median value: ', median, '\n')

    outdata.append(median)

outwrite.writerow(outdata)

outfile.close()