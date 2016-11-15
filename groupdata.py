"""
For each file in a target folder, extract all data and
write to a CSV file, append exposure times to end of
each line.
"""

import glob as g

# create a list of photometry files with target folder
file_list = g.glob('*.phot')

for filename in file_list:
    print(filename)
    # take off extension
    target = filename.split('.')[0]
    print(target)
    readfile = open(filename, 'r')
    for line in readfile:
        # Headers line in photometry files begin with #, want to ignore
        if line[0] != '#':
            # name object
            object_id = line.split('  ')[1]
            print(object_id)

            # create/open csv file for object
            writefilename = 'sorted_' + str(target) + '_' + str(object_id) + '.csv'
            print(writefilename)
            grouptocsv = open(writefilename, 'w+')

            # attach exposure time to line and write to file
            exposure = filename.split('-')[2]
            writeline = line[:-1] + '  ' + exposure[1:] #gets rid of E at start of name
            grouptocsv.write(writeline)
            grouptocsv.close()
    readfile.close()
