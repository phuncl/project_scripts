"""
Calculate true magnitudes for all standard stars
Plot against catalogue magnitudes to check calibration
"""

import matplotlib.pyplot as plt
import csv

FILTERS = {'B':0, 'V':1, 'R':2, 'I':3}
SRETLIF = {0:'B', 1:'V', 2:'R', 3:'I'}

# read zero point magnitudes in
ZPopen = open('zero_magnitude_values.csv', 'r')
ZPreader = csv.reader(ZPopen)

next(ZPreader)
Bzp, Vzp, Rzp, Izp = next(ZPreader)

zeropoints = [Bzp, Vzp, Rzp, Izp]

ZPopen.close()

# create catalogue and value lists for each filter
Bcat = []
Bval = []
Vcat = []
Vval = []
Rcat = []
Rval = []
Icat = []
Ival = []
cats = [Bcat, Vcat, Rcat, Icat]
vals = [Bval, Vval, Rval, Ival]

INGopen = open('ing_standards.csv', 'r')
INGread = csv.reader(INGopen)
next(INGread)

INGdict = {}
for line in INGread:
    INGdict[line[-1]] = line[1:-1]
INGopen.close()

mdopen = open('median_aamags.csv', 'r')
mdread = csv.reader(mdopen)
next(mdread)

for line in mdread:
    for i in range(0, len(line)-1):
        # read measured values CORRECTED FOR ZERO POINT
        # should probably make a file of these - truemags
        vals[i].append(float(line[i+1]) + float(zeropoints[i]))
        # read catalogue values
        cats[i].append(INGdict[line[0]][i])

line = [9,13,17]

for j in range(0,4):
    fig = plt.figure()
    plt.plot(cats[j], vals[j], "o")
    plt.plot(line,line)
    plt.xlabel
    plt.show()

print('All calibration figures shown. Exiting...')