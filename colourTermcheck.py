"""
Plot of m_cat - m_aa - m_zp against colour index
for all standard stars, to find gradient with colour (cC term)
"""

import matplotlib.pyplot as plt
import numpy as np
import csv
import math
from scipy.optimize import curve_fit



FILTERS = {'B':0, 'V':1, 'R':2, 'I':3}

def colour_check():
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
    # calculate and plot for V against V - I
    mag_discrepancy = []
    colourdata = []

    watson = 0
    moriarty = 0
    mycroft = 0

    for line in stardata:
        # line: name, B, V, R, I
        if math.isnan(float(line[2])) or math.isnan(float(line[4])):
            continue
        else:
            # V discrepancy = V_cat - V_aamag - V_zp
            tempmag = float(INGdict[line[0]][1]) - float(line[2]) - float(zpvals[1])

            # V-I = V_true - I_true = V_aamag + V_zp - I_aamag - I_zp
            tempcol = float(line[2]) + float(zpvals[1]) - float(line[4]) - float(zpvals[3])

            if -0.5 < tempcol < 3:
                mag_discrepancy.append(tempmag)
                colourdata.append(tempcol)

    mag_discrep = np.asarray(mag_discrepancy)
    colour = np.asarray(colourdata)


    def CT(x, grad, int):
        return grad * x + int


    c_grad, c_int = curve_fit(CT, colour, mag_discrepancy)[0]
    print(c_grad, c_int)

    plt.plot(colour, mag_discrep, "o", color = 'grey', label = 'Data')
    plt.plot(colour, CT(colour, c_grad, c_int), color = 'red', label = 'Optimised fit')
    plt.xlabel('V-I')
    plt.ylabel('V_cat - V_obs')
    plt.legend(loc = 0)
    plt.show()
    plt.clf()

    print('Slope:',c_grad, '\nIntercept:', c_int)

    with open('colour_term.dat', 'w') as fout:
        fwrite = csv.writer(fout)
        fwrite.writerow([c_grad, c_int])

