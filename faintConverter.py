import time
import csv

datafile = open('ing_standards_temp.txt', 'r')
USEDCOLS = [0,7,9,13,15]
outfile = open('ing_standards.csv','w')

for line in datafile:
    if '0' in line:
        templine = line.split(' ')
        tempdata = []

        for element in templine:
            if element != '':
                tempdata.append(element)

        data = []
        for col in USEDCOLS:
            data.append(tempdata[col])

        writetarget = csv.writer(outfile, delimiter=',')
        writetarget.writerows([data])

outfile.close()