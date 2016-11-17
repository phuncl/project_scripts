"""
For each file in a target folder, extract all data and
write to a CSV file, append exposure times to end of
each line.
"""

import glob as g
import os

FILTERS = ['B/','V/','R/','I/']
CWD = os.getcwd()

def sort_in_folder():
    # create a list of photometry files with target folder
    file_list = g.glob('*.phot')
    for filename in file_list:
        # take off extension
        target = filename.split('.')[0]
        file_prefix = target.split('-')[0]
        readfile = open(filename, 'r')
        for line in readfile:
            # Headers line in photometry files begin with #, want to ignore
            if line[0] != '#':
                # name object
                object_id = line.split('  ')[1]
                print(object_id)

                # create/open csv file for object
                target
                writefilename = 'sorted_' + str(file_prefix) + '_' + str(object_id) + '.csv'
                print(writefilename)
                grouptocsv = open(writefilename, 'w+')

                # attach exposure time to line and write to file
                exposure = filename.split('-')[2]
                writeline = line[:-1] + '  ' + exposure[1:] #gets rid of E at start of name
                grouptocsv.write(writeline)
                grouptocsv.close()
        readfile.close()

"""
Want to scan through B,V,R,I folders within a data folder automatically.
This program should be launched from within the data folder.
"""

def subdir_listing():
    # obtain a list of all subdirectories
    subdirectories_temp = os.listdir('.') #list dirs in that filter - should be same for all filters!
    subdirectories = []
    for entry in subdirectories_temp:
        if '.' not in entry:
            subdirectories.append(entry)
    os.chdir(CWD)
    return subdirectories

#################################################################
########################    MAIN    #############################
#################################################################

# navigate on a per filter basis
for filtername in FILTERS:
    print('Sorting in filter', filtername, 'in the following subdirectories:')
    os.chdir(filtername)
    subdirs = subdir_listing()
    print(subdirs)
    print(os.getcwd())
    #navigate to each object folder
    for directory in subdirs:
        os.chdir(filtername+directory+'/')
        sort_in_folder()
        print(directory, 'in', filtername, 'filter organised.')
        os.chdir(CWD)
    print(filtername, 'complete!\nStarting next filter...')        
