"""
Plot of m_cat - m_aa - m_zp against colour index
for all standard stars, to find gradient with colour (cC term)
"""

import matplotlib.pyplot as plt
import csv
import math
from scipy import stats

FILTERS = {'B':0, 'V':1, 'R':2, 'I':3}

# open zero point file and grab values
with open('zero_magnitude_values.csv', 'r') as zpopen:
    zpread = csv.reader(zpopen)
    # skip headers
    next(zpread)
    # get values
    zpvals = next(zpread)

# open catalogue and grab values
with open('ing_standards.csv', 'r') as INGopen:
    INGread = csv.reader(INGopen)
    # skip headers
    next(INGread)
    # import values to dictionary
    INGdict = {}
    for line in INGread:
        INGdict[line[-1]] = line[:-1]

# get median aa_mag for each object & filter
stardata = []
# open median aa_mag data
with open('median_aamags.csv', 'r') as mdopen:
    mdread = csv.reader(mdopen)
    # skip headers
    next(mdread)
    # read magnitudes into list
    for magnitudes in mdread:
        stardata.append(magnitudes)

# plot colour term check figure for whatever filters
# calculate and plot for V against B-V
data = []
colour = []


watson = 0
moriarty = 0
mycroft = 0

for line in stardata:
    if math.isnan(float(line[3])) or math.isnan(float(line[4])):
        continue
    # Vdata = m_cat - m_aamag - m_zp
    data.append(float(INGdict[line[0]][3]) - float(line[4]) - float(zpvals[3]))
    # BminV = (B_aamag + B_zp) - (V_aamag + V_zp)
    colour.append(float(line[3]) + float(zpvals[2]) - float(line[4]) - float(zpvals[3]))

    holmes = float(INGdict[line[0]][3]) - float(line[4])
    if holmes > watson:
        watson = holmes
        mycroft = moriarty
        moriarty = str(line[0])


colourfig = plt.figure()
plt.plot(colour, data, "o")
plt.xlabel('R-I')
plt.ylabel('I data')
plt.show()

slope, intercept, rval, pval, stderr = stats.linregress(colour, data)

print('Slope:',slope, '\nIntercept:', intercept)

print(moriarty, mycroft)