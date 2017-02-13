"""
In ExposureMetre directory, create proc files for each filter
"""

import csv
import os
import glob as g
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

#####################   CONSTANTS   #######################

FILTERS = ['B', 'V', 'R', 'I']
CWD = os.getcwd()


def proc_exposuredata(flt):
    # Get all files for a filter, use data to create proc file
    flist = g.glob(flt + '*')
    mag = []
    log_expo = []
    for fname in flist:
        with open(fname, 'r') as fin:
            freader = csv.reader(fin)
            # skip headers
            next(freader)
            for line in freader:
                mag.append(float(line[0]))
                log_expo.append(np.log10(float(line[1])))
    # calculate fit of mag vs log_expo
    fit_output = stats.linregress(mag, log_expo)
    # show plot of mag vs log_expo
    plt.plot(mag, log_expo, 'o')
    plt.xlabel('Magnitude')
    plt.ylabel('log(Exposure)')
    plt.show()

    with open('proc_{}.csv'.format(flt), 'w') as fout:
        fwriter = csv.writer(fout)
        fwriter.writerow(['#slope', 'intercept', 'rvalue', 'pvalue', 'stderr'])
        fwriter.writerow(fit_output)


def read_exposuredata(proc_filename):
    with open(proc_filename, 'r') as proc_file:
        proc_reader = csv.reader(proc_file, dialect='excel')
        # skip headers
        next(proc_reader, None)
        plot_data = next(proc_reader)

    return plot_data


def calc_exposurerec():
    # open desired filter and allow calculation of exposure for a given magnitude
    req_filter = input('Which filter do you require?\nPlease enter either B, V, R, or I:\n').upper()
    # check if processed file already exists - if not, create it
    proc_filename = 'proc_{}.csv'.format(req_filter)
    if not os.path.exists(proc_filename):
        # here create PROC file
        print('Data not yet processed for this filter!\nProcessing data...')
        proc_exposuredata(req_filter)
    else:
        # here read from PROC file
        print('Opening file...')
    fit_data = read_exposuredata(proc_filename)
    slope = float(fit_data[0])
    intercept = float(fit_data[1])

    input_mag = float(input('Enter the magnitude of the object:\n'))
    output_max_exposure = np.power(10, (slope * input_mag + intercept))

    print('Object of magnitude', input_mag, 'has recommended exposure of',
          float('{0:.2f}'.format(output_max_exposure)), 'seconds.')

    return 0


#####################     MAIN      #######################

# create proc data files if they do not exist, if desired
recalc = input('Would you like to recalculate exposures from current data? (y/n) ').lower()
if recalc == 'y':
    for filt in FILTERS:
        proc_exposuredata(filt)


exit_request = 0
while exit_request == 0:
    calc_exposurerec()
    exit_check = input('Would you like to check another object? (y/n) ')

    if exit_check.lower() == 'y':
        pass
    else:
        print('Exiting program...')
        exit_request += 1
# program ends
