"""
Calculate true magnitudes for all standard stars
Plot against catalogue magnitudes to check calibration
"""

import matplotlib.pyplot as plt
import csv

FILTERS = {'B':0, 'V':1, 'R':2, 'I':3}
SRETLIF = {0:'B', 1:'V', 2:'R', 3:'I'}

# read zero point magnitudes in
ZPopen = open('rezero_vals.csv', 'r')
ZPreader = csv.reader(ZPopen)

next(ZPreader)
Bzp, Vzp, Rzp, Izp = next(ZPreader)

zeropoints = [Bzp, Vzp, Rzp, Izp]
ZPopen.close()

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

for line in mdread:
    for i in range(0, 4):
        # read measured magnitude CORRECTED FOR colour term
        if i == 1:
            vals[i].append(float(line[i+1]) + float(zeropoints[i]) + col_int + col_grad * (float(line[2]) - float(line[4])))
        else:
            vals[i].append(float(line[i+1]) + float(zeropoints[i]))
        # same for weighted average values
        # avgs[i].append(float(line[2i + 4]))
        # read catalogue values
        cats[i].append(INGdict[line[0].replace('-','_')][i])

line = [9,17]
for j in range(0,4):
    fig = plt.figure()
    plt.plot(cats[j], vals[j], "o", color = 'red')
    #plt.plot(cats[j], avgs[j], "o", color = 'green')
    plt.plot(line,line)
    plt.xlabel('catalogue mag')
    plt.ylabel('observed mag')
    plt.title(SRETLIF[j] + ' data')
    plt.show()

print('All calibration figures shown. Exiting...')