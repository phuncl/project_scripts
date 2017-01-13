"""
Plot a CMD for chosen cluster
"""

import matplotlib.pyplot as plt
import csv
import math

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
        mag_data.append(line[1])
        col_data.append(float(line[1])-float(line[3]))

    fig = plt.figure()
    plt.plot(col_data, mag_data, 'o')
    plt.xlabel('V-I')
    plt.ylabel('V')
    plt.title(filename.split("_")[-1])

    plt.show()