import time
import csv

datafile = open('ing_standards_temp.txt', 'r')
USEDCOLS = [0,7,9,13,15]
outfile = open('ing_standards.csv','w')

for line in datafile:
    templine = line.lstrip()
    line = templine.rstrip()
    if '0' in line:
        tempstandardname = line[116:]
        nearlystandardname = tempstandardname.replace(' ','_')
        nearstandardname = nearlystandardname.replace('+','_')
        standardname = nearstandardname.replace('Feige','F')


        templine = line.split(' ')
        tempdata = []

        for element in templine:
            if element != '':
                tempdata.append(element)

        data = []
        for col in USEDCOLS:
            data.append(tempdata[col])
        data.append(standardname[:])
        print(data)

        writetarget = csv.writer(outfile, delimiter=',')
        writetarget.writerows([data])

outfile.close()

print('File converted successfully! Exiting...')