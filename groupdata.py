"""
For each file in a target folder, extract all data and
write to a CSV file, append exposure times to end of
each line.
"""

import os
import glob as g
import time

file_list = g.glob('*.phot')

for filename in file_list:
    print(filename)
    target = filename.split('.')[0]
    print(target)
    readfile = open(filename, 'r')
    for line in readfile:
        #name object
        object_id = line.split('  ')[1]
        print(object_id)

        #create/open csv file for object
        writefilename = 'sorted_' + str(target) + '_' + str(object_id) + '.csv'
        print(writefilename)
        grouptocsv = open(writefilename, 'w+')

        #attach exposure time to line and write to file
        exposure = filename.split('-')[2]
        line.append('  ' + exposure[1:])
        grouptocsv.write(line)
        grouptocsv.close()
    readfile.close()
