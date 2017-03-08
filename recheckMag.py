"""
Calculate true magnitudes for all standard stars
Plot against catalogue magnitudes to check calibration
"""

import matplotlib.pyplot as plt
import csv
import numpy as np

FILTERS = {'B':0, 'V':1, 'R':2, 'I':3}
SRETLIF = {0:'B', 1:'V', 2:'R', 3:'I'}

# read zero point magnitudes in
ZPopen = open('rezero_vals.csv', 'r')
ZPreader = csv.reader(ZPopen)

next(ZPreader)
Bzp, Vzp, Rzp, Izp = next(ZPreader)

zeropoints = [Bzp, Vzp, Rzp, Izp]
ZPopen.close()

with open('zero_magnitude_values.csv', 'r') as fzp:
    zread = csv.reader(fzp)
    next(zread)
    oldzp = next(zread)

with open('colour_term.dat', 'r') as fin:
    line = fin.readline().split(',')
col_grad = float(line[0])
col_int = float(line[1])

# create catalogue and value lists for each filter
Bcat = []
Bval = []
Bavg = []
Vcat = []
Vval = []
Vavg = []
Rcat = []
Rval = []
Ravg = []
Icat = []
Ival = []
Iavg = []
cats = [Bcat, Vcat, Rcat, Icat]
vals = [Bval, Vval, Rval, Ival]
#avgs = [Bavg, Vavg, Ravg, Iavg]

INGopen = open('ing_standards.csv', 'r')
INGread = csv.reader(INGopen)
next(INGread)

INGdict = {}
for line in INGread:
    INGdict[line[-1]] = line[0:-1]
INGopen.close()

mdopen = open('median_aamags.csv', 'r')
mdread = csv.reader(mdopen)
# skip headers
next(mdread)
oldv = []
for line in mdread:
    for i in range(0, 4):
        # read measured magnitude CORRECTED FOR colour term
        if i == 1:
            vals[i].append(float(line[i+1]) + float(zeropoints[i]) - col_int + col_grad * (float(line[2]) - float(line[4])))
            oldv.append(float(line[i+1]) + float(oldzp[1]))
        else:
            vals[i].append(float(line[i+1]) + float(zeropoints[i]))
        # same for weighted average values
        # avgs[i].append(float(line[2i + 4]))
        # read catalogue values
        cats[i].append(float(INGdict[line[0].replace('-','_')][i]))

line = [5,20]
for j in range(0,4):
    fig = plt.figure()
    if j == 1:
        plt.plot(cats[j], oldv, 'o', color = 'green', label = 'Corrected ZP')
        plt.plot(cats[j], vals[j], "o", color='red', label = 'Original ZP')
        ymin = min([min(vals[j]), min(oldv)]) - 0.5
        ymax = max([max(vals[j]), max(oldv)]) + 0.5
    else:
        plt.plot(cats[j], vals[j], "o", color = 'red')
        ymin = min(vals[j]) - 0.5
        ymax = max(vals[j]) + 0.5
    #plt.plot(cats[j], avgs[j], "o", color = 'green')
    plt.plot(line,line, color = 'black')
    plt.xlabel('catalogue mag')
    plt.ylabel('observed mag')
    plt.title(SRETLIF[j] + ' standard stars')
    plt.legend(loc=0)
    xmin = float(min(cats[j])) - 0.5
    xmax = float(max(cats[j])) + 0.5
    plt.axis([xmin, xmax, ymin, ymax])
    plt.show()

print('All calibration figures shown. Exiting...')