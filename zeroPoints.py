"""
For all standard stars, find single magnitude for each filter
compare to the catalogue mag and calculate zero point magnitude
Take median zero point for each filter as final value

Apply zero point to science targets
"""

import os
import csv
import numpy as np
import math
import glob as g
import time

################################################################
# FUNCTION DEFINITIONS

def isnum(x):
    try:
        float(x)
        return True
    except:
        return False


def zp_data_grab():
    # read zero_magnitude_data.csv into program
    ZPdata = open('zero_magnitude_data.csv', 'r')
    ZPreader = csv.reader(ZPdata)

    next(ZPreader)

    Bvals = []
    Vvals = []
    Rvals = []
    Ivals = []
    values = [Bvals,Vvals,Rvals,Ivals]

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

    return values


def filter_medians(listlist):
    # take list of filter data for object
    # return median for each filter
    medians = []

    for filt in listlist:
        medians.append(np.median(filt))

    return medians


def zp_calc():
    # now take average value for data in each filter
    # and output to zero_magnitude_values.csv
    outfile = open('zero_magnitude_values.csv', 'w')
    outwrite = csv.writer(outfile)

    HEADERS = ['#B', 'V', 'R', 'I']
    outwrite.writerow(HEADERS)

    medians = filter_medians(vals)
    outwrite.writerow(medians)

    outfile.close()

    return medians


def correct_science(filename):

    Bvals = []
    Vvals = []
    Rvals = []
    Ivals = []
    values = [Bvals, Vvals, Rvals, Ivals]

    clustername = filename.split('_')[1]
    starnametmp = filename.split('_')[-1]
    starname = starnametmp.split('.')[0]

    # separate data by filter
    with open(filename, 'r') as infile:
        reader = csv.reader(infile)
        # skip headers line
        next(reader)

        for line in reader:
            if not math.isnan(float(line[-1])):
                values[FILTERS[line[-2]]].append(float(line[-1]))

    # produce median aa mag for target
    med_aamags = filter_medians(values)

    med_trumags = []
    med_trumags.append(starname)
    for k in range(0,4):
        med_trumags.append(med_aamags[k] + zp_vals[k])

    return clustername, med_trumags



################################################################
# MAIN FUNCTION

FILTERS = {'B': 0, 'V': 1, 'R': 2, 'I': 3}

os.chdir('CombinedData/Standards')
# get data from zero_magnitude_data and calculate zero points
vals = zp_data_grab()
zp_vals = zp_calc()

# apply zero point magnitude to aa_mags for each science target
# and compile all data into one file
os.chdir('../Science/')

# list all science files
SCI_list = g.glob('aamag*')

# get names of clusters in folder
clusternames = []
for eachthing in SCI_list:
    c = eachthing.split('_')[1]
    if c not in clusternames:
        clusternames.append(c)
# print names of clusters
print('The following clusters have been identified:')
for object in clusternames:
    print(object)

true_mags = {}
# initialise file for each cluster
for cluster in clusternames:
    mkfilename = 'true_mags_{0}.csv'.format(str(cluster))
    with open(mkfilename, 'w') as out:
        quickwrite = csv.writer(out)
        quickwrite.writerow(['#OBJ_ID','B','V','R','I'])
    # create dictionary key for the cluster
    true_mags[cluster] = []

print('\nBeginning magnitude corrections...\n')
time.sleep(2)

# from each file get a list of median corrected magnitude
for eachfile in SCI_list:
    clust, magnitudes = correct_science(eachfile)
    true_mags[clust].append(magnitudes)

for key in true_mags:
    writefilename = 'true_mags_{0}.csv'.format(str(key))
    with open(writefilename, 'a') as writefile:
        writer = csv.writer(writefile)
        writer.writerows(true_mags[key])