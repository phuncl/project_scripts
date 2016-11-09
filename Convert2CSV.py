import os

#Purpose is to read in .phot file and convert it to a CSV (Comma Separated Values) file.

#""""""""""""""""""""""
#First iteration - Convert a single file --> generalise for all files in data folder
#""""""""""""""""""""""

filename = input('Which file do you want to convert? ')

f = open(filename, 'r')

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
