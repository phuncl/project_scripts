"""
Plot a CMD for chosen cluster
"""

import matplotlib.pyplot as plt
import csv
import math
from scipy import stats
import numpy as np


# dict pointing to list of gradient, intercept, x_min, x_max, y_min, y_max
dict = {'true_mags_Berkeley18.csv': [8.0, 10.0, -0.5, 2.5, 10.0, 16.5],
        'true_mags_NGC2099.csv': [5.0, 12.5, -2.0, 2.0, 9.0, 17.0],
        'true_mags_NGC6940.csv': [6.0, 11.0, -0.5, 3.0, 9.0, 17.0],
        'true_mags_NGC7092.csv': [5.5, 11.0, -0.5, 3.2, 9.0, 16.5]}


def clip_data(x, y, file):
    """
    clip high standard deviation data (arbitrarily fit straight line to data
    for now, clip at some high std like 7)

    :param x: x axis data (list)
    :param y: y axis data (list)
    :return: clipped data x and y, fit data x and y
    """
    # m, c, r_value, p_value, stderr = stats.linregress(x, y)

    residuals = []

    # get gradient and intercept from dictionary (fit by eye)
    m3 = dict[file][0]
    c3 = dict[file][1]

    # calculate residuals (y data minus fitted y data)
    for i, q in enumerate(x):
        res = abs( y[i] - (m3*q + c3) ) # changed from m and c above
        residuals.append(res)

    sigma = np.std(residuals)
    print(sigma)

    # collate new data within clipping boundaries
    x_new = []
    y_new = []

    for i, res in enumerate(residuals):
        if res < 6 * sigma:
            x_new.append(x[i])
            y_new.append(y[i])

    # get fit line too
    x_fit = []
    y_fit = []

    m2, c2, rv, pv, err = stats.linregress(x_new, y_new)

    print(m2, c2)

    for i in np.linspace(0.0, 2.5, 50):
        x_fit.append(i)
        y_fit.append(m2 * i + c2)

    return x_new, y_new, x_fit, y_fit


files = ['true_mags_Berkeley18.csv',
         'true_mags_NGC2099.csv',
         'true_mags_NGC6940.csv',
         'true_mags_NGC7092.csv']

for filename in files:
    filehandle = open(filename, 'r')
    filereader = csv.reader(filehandle)
    next(filereader)

    # plot V against V-I
    mag_data = []
    col_data = []
    for line in filereader:
        if math.isnan(float(line[1])) or math.isnan(float(line[3])):
            continue
        mag_data.append(float(line[1]))
        col_data.append(float(line[1])-float(line[3]))

    ####################################
    ###### Fit by eye per cluster ######
    ####################################

    x_ifit = []
    y_ifit = []

    m3 = dict[filename][0]
    c3 = dict[filename][1]

    print(m3, c3)

    for i in np.linspace(-0.5, 2.0, 80):
        x_ifit.append(i)
        y_ifit.append(m3*i + c3)

    x_min = dict[filename][2]
    x_max = dict[filename][3]
    y_min = dict[filename][4]
    y_max = dict[filename][5]

    ####################################

    magnitude, colour, mag_fit, col_fit = clip_data(col_data, mag_data, filename) # returns x_new, y_new
    fig = plt.figure()
    plt.plot(magnitude, colour, 'o') # cluster data
    plt.plot(mag_fit, col_fit, 'ro') # fit data
    plt.plot(x_ifit, y_ifit, 'go') # fit by eye for each cluster
    plt.axis([x_min, x_max, y_min, y_max])
    plt.gca().invert_yaxis()
    plt.xlabel('V-I')
    plt.ylabel('V')
    plt.title(filename.split("_")[-1])

    plt.show()