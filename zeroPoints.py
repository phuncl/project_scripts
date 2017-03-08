"""
For all standard stars, find single magnitude for each filter
compare to the catalogue mag and calculate zero point magnitude
Take median zero point for each filter as final value
Apply zero point to science targets
"""

import os
import csv
import numpy as np
import glob as g
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time

################################################################


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
    values = [Bvals, Vvals, Rvals, Ivals]

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
    medians = filter_medians(initial_vals)
    outwrite.writerow(medians)
    outfile.close()
    return medians


def correct_science(filename):
    # apply mag correction to science data
    Bvals = []
    Vvals = []
    Rvals = []
    Ivals = []
    values = [Bvals, Vvals, Rvals, Ivals]
    Bsnr = []
    Vsnr = []
    Rsnr = []
    Isnr = []
    snrs = [Bsnr, Vsnr, Rsnr, Isnr]
    # object name strings
    clustername = filename.split('_')[1]
    starnametmp = filename.split('_')[-1]
    starname = starnametmp.split('.')[0]
    datablock = []
    # separate data by filter
    with open(filename, 'r') as infile:
        reader = csv.reader(infile)
        # skip headers line
        next(reader)

        for line in reader:
            datablock.append(line)

    for line in datablock:
        if not math.isnan(float(line[-1])):
            values[FILTERS[line[3]]].append(float(line[-1]))
            snrs[FILTERS[line[3]]].append(float(line[-2]))

    # produce median aa mag for target
    med_aamags = filter_medians(values)
    med_trumags = []
    med_trumags.append(starname)
    # for each filter add zp to median selected mag
    for k in range(0, 4):
        med_trumags.append(med_aamags[k] + zp_vals[k])
    med_trumags[1] += colcheck_values[0] * (med_trumags[1] - med_trumags[3]) + colcheck_values[1]

    return clustername, med_trumags


def colour_check(zpvalues):
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

    for line in stardata:
        # line: name, B, V, R, I
        if math.isnan(float(line[2])) or math.isnan(float(line[4])):
            continue
        else:
            # V discrepancy = V_cat - V_aamag - V_zp
            tempmag = float(INGdict[line[0]][1]) - float(line[2]) - float(zpvalues[1])
            # V-I = V_true - I_true = V_aamag + V_zp - I_aamag - I_zp
            tempcol = float(line[2]) + float(zpvalues[1]) - float(line[4]) - float(zpvalues[3])

            if -0.5 < tempcol < 3:
                mag_discrepancy.append(tempmag)
                colourdata.append(tempcol)

    mag_discrep = np.asarray(mag_discrepancy)
    colour = np.asarray(colourdata)

    def ct(x, grad, int):
        return grad * x + int

    c_grad, c_int = curve_fit(ct, colour, mag_discrepancy)[0]
    plt.plot(colour, mag_discrep, "o", color='grey', label='Data')
    plt.plot(colour, ct(colour, c_grad, c_int), color='red', label='Optimised fit')
    plt.xlabel('V-I')
    plt.ylabel('V_cat - V_obs')
    plt.legend(loc=0)
    plt.show()
    plt.clf()

    print('Slope:', c_grad, '\nIntercept:', c_int)

    with open('colour_term.dat', 'w') as fout:
        fwrite = csv.writer(fout)
        fwrite.writerow([c_grad, c_int])

    return [c_grad, c_int]


def rezp_calc():
    # now take average value for data in each filter
    # and output to zero_magnitude_values.csv
    outfile = open('rezero_vals.csv', 'w')
    outwrite = csv.writer(outfile)
    HEADERS = ['#B', 'V', 'R', 'I']
    outwrite.writerow(HEADERS)
    medians = filter_medians(vals)
    outwrite.writerow(medians)
    outfile.close()
    return medians

def rezp_data_grab():
    # read zero_magnitude_data.csv into program
    ZPdata = open('rezero_magnitude_data.csv', 'r')
    ZPreader = csv.reader(ZPdata)
    next(ZPreader)
    Bvals = []
    Vvals = []
    Rvals = []
    Ivals = []
    values = [Bvals, Vvals, Rvals, Ivals]

    for line in ZPreader:
        if not math.isnan(float(line[1])):
            Bvals.append(float(line[1]))

        if not math.isnan(float(line[2])) and not math.isnan(float(line[4])):
            # correction for V-I colour
            Vvals.append(float(line[2]) + c_int + c_grad * (float(line[2]) - float(line[4])))

        if not math.isnan(float(line[3])):
            Rvals.append(float(line[3]))

        if not math.isnan(float(line[4])):
            Ivals.append(float(line[4]))

    ZPdata.close()
    return values

def rezeropoint():
    # open standards catalogue file
    STDfile = open('ing_standards.csv')
    STDreader = csv.reader(STDfile)
    # write standards catalogue data to dictionary
    STDdict = {}
    for line in STDreader:
        STDdict[line[-1]] = line[:-1]
    STDfile.close()
    print('Standard dictionary imported')
    # open compiled file
    compfile = open('median_aamags.csv', 'r')
    compread = csv.reader(compfile)
    # skip headers
    next(compread)
    # initialise zero magnitudes file
    zeromags = open('rezero_magnitude_data.csv', 'w+')
    zerowriter = csv.writer(zeromags)
    zerowriter.writerow(['#OBJECT_NAME', 'B_mag', 'V_mag', 'R_mag', 'I_mag'])

    # for each line of data
    for dataline in compread:
        # initialise zpline with starname
        starname = dataline[0].replace('-','_')
        if not starname:
            continue
        zpline = []
        zpline.append(starname)

        for i in range(0,4):
            if i == 1:
                # zp = Mcat - (M_aamag + col_grad * V-I + col_int)
                zeropt = float(STDdict[starname][i]) - (float(dataline[i+1]) + (float(dataline[1]) - float(dataline[3]) * c_grad - c_int))
            else:
                zeropt = float(STDdict[starname][i]) - float(dataline[i+1])
            zpline.append(zeropt)
        # write data line to zeromags
        print(starname, zpline)
        time.sleep(0.5)
        zerowriter.writerow(zpline)

    zeromags.close()


################################################################

FILTERS = {'B': 0, 'V': 1, 'R': 2, 'I': 3}
os.chdir('CombinedData/Standards')
# get data from zero_magnitude_data and calculate zero points for standards
initial_vals = zp_data_grab()
# initial_vals used here in zp_calc
initial_zp = zp_calc()
print('Initial zero point magnitudes are:')
for key in FILTERS:
    print(key, initial_zp[FILTERS[key]])

######
# CONTENT OF REZERO
# run colour check, calculate and apply correction to V
colcheck_values = colour_check(initial_zp)
c_int = float(colcheck_values[1])
c_grad = float(colcheck_values[0])
print(c_int, c_grad)

rezeropoint()
# get zp data, correct for colour term
vals = rezp_data_grab()
zp_vals = rezp_calc()
print('Recalculated zero point magnitudes are:')
for key in FILTERS:
    print(key, zp_vals[FILTERS[key]])
#####

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
for obj in clusternames:
    print(obj)

true_mags = {}
# initialise file for each cluster
for cluster in clusternames:
    mkfilename = 'true_mags_{0}.csv'.format(str(cluster))
    with open(mkfilename, 'w') as out:
        quickwrite = csv.writer(out)
        quickwrite.writerow(['#OBJ_ID', 'B', 'V', 'R', 'I', 'SNR'])
    # create dictionary key for the cluster
    true_mags[cluster] = []

print('\nBeginning magnitude corrections...\n')
# from each file get a list of median corrected magnitude
for eachfile in SCI_list:
    clust, magnitudes = correct_science(eachfile)
    true_mags[clust].append(magnitudes)

for key in true_mags:
    writefilename = 'true_mags_{0}.csv'.format(str(key))
    with open(writefilename, 'a') as writefile:
        writer = csv.writer(writefile)
        writer.writerows(true_mags[key])

# same for poor mags
POOR_list = g.glob('pooraamag*')
poor_mags = {}
# initialise file for each cluster
for cluster in clusternames:
    mkfilename = 'true_poormags_{0}.csv'.format(str(cluster))
    with open(mkfilename, 'w') as out:
        quickwrite = csv.writer(out)
        quickwrite.writerow(['#OBJ_ID', 'B', 'V', 'R', 'I', 'SNR'])
    # create dictionary key for the cluster
    poor_mags[cluster] = []

for poorfile in POOR_list:
    poorclust, poormag = correct_science(poorfile)
    poor_mags[poorclust].append(poormag)

for key in poor_mags:
    writepoorname = 'true_poormags_{0}.csv'.format(str(key))
    with open(writepoorname, 'a') as poorout:
        poorwriter = csv.writer(poorout)
        poorwriter.writerows(poor_mags[key])
