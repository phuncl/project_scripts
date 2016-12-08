"""
Move through pre-existing 'sorted_...' files for science objects.
Isolate data for each filter and take median flux from all available.
Output this data for each filter to a new file.
Program should be run from central data folder
"""

import os
import glob as g
import csv

CWD = os.getcwd()
FILTERS = ['B','V','R','I']

###############################################################
def median_flux(listy):
    listy.sort()
    length = len(listy)
    mid_index = int((length+1)/2 -1)

    return listy[mid_index]
###############################################################

os.chdir('CombinedData/Science/')
objectslist = g.glob('sorted*')
#objectslist = ['sorted_Berkeley18_33.csv']

# for each file, take median value for each filter
for object in objectslist:
    objectfile = open(object, 'r')
    objectreader = csv.reader(objectfile, dialect='excel')
    # skip header line
    next(objectreader)

    print('Finding median values for', object)

    # initialise list of lists for each filter
    b_lines = []
    v_lines = []
    r_lines = []
    i_lines = []
    lines_set = [b_lines,v_lines,r_lines,i_lines]

    for line in objectreader:
        lines_set[FILTERS.index(line[-1])].append(line)

    objectfile.close()

    out_lines = []

    for set in lines_set:
        temp_fluxlist = []

        for line in set:
            # make a list of flux values
            if float(line[-2]) > 0:
                temp_fluxlist.append(line[-2])

        if temp_fluxlist:
            medianflux = median_flux(temp_fluxlist)

            for line in set:
                if line[-2] == medianflux:
                    out_lines.append(line)
                    break
                else:
                    pass
        else:
            dead_line = [-1]*14
            out_lines.append(dead_line)

    print('Median flux values determined for file!')
    # write to file

    outputname = 'medians_' + object.split('_',1)[1]
    outputfile = open(outputname, 'w')
    outputwriter = csv.writer(outputfile,dialect='excel')

    headers = ['#BJD', 'OBJECT_ID', 'X', 'Y', 'RSI', 'RSO', 'COUNTS', 'COUNTS_ERR', 'AIRMASS', 'FLAG', 'COUNTS_MAX', 'EXPOSURE', 'FLUX', 'FILTER']

    outputwriter.writerow(headers)
    outputwriter.writerows(out_lines)
    outputfile.close()