"""Convert each photometry file into a CSV, ignoring the first line"""

import glob as g

def convert2csv(filename):
    """Read each file in dir and subdir, change double space to comma"""
    convertfile = open(filename, 'r')

    #Take off .extension at the end
    rawname = filename.split('.')

    csv = open(rawname[0] + '.csv', 'w+')
    linenumber = 1
    for line in convertfile:
        if linenumber == 1:
            linenumber = 2
        else:
            newline = line.replace('  ', ',')
            csv.write(newline)
    csv.close()
    convertfile.close()

#Create a list of all files, including those in subdirectories
print('Converting the following photometry files to CSV format...')
EVERY_FILE = g.glob('**/*.phot', recursive=True)         #Change this to .phot 'MEMBER

print(EVERY_FILE)

#Convert each phot file found into csv
for file in EVERY_FILE:
    convert2csv(file)
    print(file + ' successfully converted')

print('All photometry files successfully successfully converted into CSV')
