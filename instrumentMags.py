"""
For each line in each file in CombinedData/Standards/
Calc above atmosphere instrumental magnitude
Then take median value and calculate zero points
"""

import csv
import os
import glob as g
import numpy as np


# atmospheric constants
ATMOSPHERIC = {'B': 0.2081, 'V': 0.1027, 'R': 0.0670, 'I': 0.0118}
FILTERS = {'B': 0, 'V': 1, 'R': 2, 'I': 3}
os.chdir('CombinedData/')

#####################################################################


def aa_mag_calc():
    # list all relevant files
    print('Populating file list...')
    FILELIST = g.glob('sorted*')

    # for each file
    for filename in FILELIST:
        fileopen = open(filename, 'r')
        filereader = csv.reader(fileopen)
        # read headers
        HEADERS = next(filereader)
        # skip already processed files
        if HEADERS[-1] == 'AA_MAG':
            continue
        # add new aa_mag header
        HEADERS.append('AA_MAG')
        # read data into temp list of lists
        alldata = []
        filedata = []
        for row in filereader:
            alldata.append(row)
            if float(row[-1]) > 10:
                filedata.append(row)

        # close file
        fileopen.close()
        filedata = inst_to_aa(filedata)
        # open new output file
        magfile = open('aamag_'+filename[7:], 'w')
        magwriter = csv.writer(magfile)
        # write data to new file
        magwriter.writerow(HEADERS)
        magwriter.writerows(filedata)
        # close new file
        magfile.close()
        alldata = inst_to_aa(alldata)
        # open new output file
        magfile = open('pooraamag_'+filename[7:], 'w')
        magwriter = csv.writer(magfile)
        # write data to new file
        magwriter.writerow(HEADERS)
        magwriter.writerows(alldata)
        # close new file
        magfile.close()
        print(filename, 'processed.\n')


def inst_to_aa(listoflist):
    # for each data row
    for i in range(0, len(listoflist)):
        # read relevant values
        flux = float(listoflist[i][2])
        airmass = float(listoflist[i][1])
        filtername = str(listoflist[i][3])
        # get instrumental magnitude
        inst_mag = -2.5 * np.log10(flux)
        # apply first order atmosphere correction
        above_atmos_mag = inst_mag - (airmass * ATMOSPHERIC[filtername])
        listoflist[i].append(above_atmos_mag)
    return listoflist


def medianmag():
    FILELIST = g.glob('aamag*')
    mdnam = 'median_aamags.csv'
    outdata = []

    # for each file
    for filename in FILELIST:
        fileopen = open(filename, 'r')
        fileread = csv.reader(fileopen)
        # skip headers
        next(fileread)
        # create holding lists
        Bdata = []
        Vdata = []
        Rdata = []
        Idata = []
        filterdata = [Bdata, Vdata, Rdata, Idata]
        # read each aa_mag value into relevant filter list
        starname = 0

        for line in fileread:
            filterdata[FILTERS[line[3]]].append(float(line[5]))
            if not starname:
                starname = line[0]
                print('Analysing', starname)
        fileopen.close()
        # compute median values
        Bmed = np.median(Bdata)
        Vmed = np.median(Vdata)
        Rmed = np.median(Rdata)
        Imed = np.median(Idata)
        outline = [starname, Bmed, Vmed, Rmed, Imed]
        print('Output line:\n', outline)
        if starname:
            outdata.append(outline)
    # initialise compilation file
    # and then write data from list of lists
    mdopen = open(mdnam, 'w+')
    mdwrite = csv.writer(mdopen)
    mdwrite.writerow(['#OBJECT_ID', 'B', 'V', 'R', 'I'])
    mdwrite.writerows(outdata)
    mdopen.close()

    print('All object medians recorded in', mdnam)


def zeropoint():
    # open standards catalogue file
    STDfile = open('ing_standards.csv')
    STDreader = csv.reader(STDfile)
    # write standards catalogue data to dictionary
    STDdict = {}
    for line in STDreader:
        STDdict[line[-1]] = line[:-1]
    STDfile.close()
    # open compiled file
    compfile = open('median_aamags.csv', 'r')
    compread = csv.reader(compfile)
    # skip headers
    next(compread)
    # initialise zero magnitudes file
    zeromags = open('zero_magnitude_data.csv', 'w+')
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
            zeropt = float(STDdict[starname][i]) - float(dataline[i+1])
            zpline.append(zeropt)
        # write data line to zeromags
        zerowriter.writerow(zpline)

    zeromags.close()


###########################MAIN#####################################
# run procedure on standard stars
os.chdir('Standards/')
print('Processing Standards targets...')
# calculate aa_mags for all standards
aa_mag_calc()
# compile medians for all standard stars into one file
medianmag()
# record zero point magnitudes to file
zeropoint()

os.chdir('..')
# run procedure on science targets
os.chdir('Science')
print('Processing Science targets...')
aa_mag_calc()
print('All instrumental above-atmosphere magnitudes calculated!\a')