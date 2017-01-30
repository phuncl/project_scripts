"""
Plot a CMD for all clusters
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpat
import csv
import math
import glob as g

files = g.glob('true_mags*')
print(files)
poorfiles = g.glob('true_poormags*')

CLUSTERS = ['Berkeley18', 'NGC2099', 'NGC6940', 'NGC7092']


#zamsdata = []
#with open('/media/sf_LinuxShare/isochrones/zams.csv','r') as zamsfile:
#    zamsread = csv.reader(zamsfile)
#    next(zamsread)
#    for line in zamsread:
#        zamsdata.append(line)

# create V and V-I columns
#zamsV = []
#zamsVmI = []
#for line in zamsdata:
#    zamsV.append(float(line[1]))
#    zamsVmI.append(float(line[4]))

for i in range(0, len(files)):
    print('Opening:', files[i])
    title = files[i]
    filehandle = open(files[i], 'r')
    poorhandle = open(poorfiles[i], 'r')
    filereader = csv.reader(filehandle)
    poorreader = csv.reader(poorhandle)
    next(filereader)
    next(poorreader)

    # plot V against V-I
    mag_data = []
    poor_data = []
    col_data = []
    poorcol_data = []
    for line in filereader:
        if math.isnan(float(line[2])) or math.isnan(float(line[4])):
            pass
        else:
            mag_data.append(line[2])
            col_data.append(float(line[2]) - float(line[4]))
    for line in poorreader:
        if math.isnan(float(line[2])) or math.isnan(float(line[4])):
            pass
        else:
            poor_data.append(float(line[2]))
            poorcol_data.append(float(line[2]) - float(line[4]))


    fig = plt.figure()

    plt.plot(poorcol_data, poor_data, 'o', color = 'grey')
    plt.plot(col_data, mag_data, '.', color = 'red')

    classes = ['S/N > 10', 'Unrefined']
    colours = ['red', 'grey']
    recs = []
    for i in range(0, len(colours)):
        recs.append(mpat.Patch(color = colours[i], label = classes[i]))
    plt.legend(handles = recs)


    #plt.plot(zamsVmI, zamsV, 'o', color='green')
    plt.gca().invert_yaxis()

    plt.xlabel('V-I')
    plt.ylabel('V')

    title = title.split('_')[-1].split('.')[0]
    print(title)

    plt.title(title)

    plt.show()