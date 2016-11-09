import os
import glob as g

#Purpose is to read in .phot file and convert it to a CSV (Comma Separated Values) file.

#""""""""""""""""""""""
#First iteration - Convert a single file --> generalise for all files in data folder
#Second iteration - Go through all files in the current directory and subdirectories and convert all those
#""""""""""""""""""""""

#filename = input('Which file do you want to convert? ')

def convert2csv(filename):
    f = open(filename, 'r')

    #Take off .extension at the end
    rawname = filename.split('.')

    csv = open(rawname[0] + '.csv', 'w+')        # Change this to replace .phot extension with .csv
    linenumber = 1                             # after moving onto real data
    for line in f:
        if linenumber == 1:
            linenumber = 2
            pass

        else:
            newline = line.replace('  ', ',')
            csv.write(newline)
    csv.close()
    f.close()

#Create a list of all files, including those in subdirectories
print('Converting the following photometry files to CSV format...')
file_list = g.glob('**/*.phot', recursive=True)         #Change this to .phot 'MEMBER

print(file_list)

#Convert each phot file found into csv
for file in file_list:
    convert2csv(file)
    print(file + ' successfully converted')



