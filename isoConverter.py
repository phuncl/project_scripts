"""
Convert downlaoded isochrone data to readable format
"""

import csv
import matplotlib.pyplot as plt
import glob as g

flist = g.glob('*.dat')
for i, entry in enumerate(flist):
    print(str(i) + '\t' + entry)
index = int(input('Give index of desired file: '))
fname = flist[index]

dict = {}

colours = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown', 'grey', 'black']

with open(fname, 'r') as fiso:
    for line in fiso:
        if line[0] == '#':
            continue
        else:
            details = line.split()
            age = float(details[0])
            Vmag = float(details[9])
            col = float(details[9]) - float(details[11])

        if not age in dict:
            dict[age] = []
        if Vmag < 20 and col < 20:
            dict[age].append([Vmag, col])


colourcount = 0
fig = plt.figure()
for key in dict:
    mag = []
    col = []
    for pair in dict[key]:
        mag.append(pair[0])
        col.append(pair[1])

    plt.plot(col, mag, '.', color=colours[colourcount], label=key)
    colourcount += 1

    outname = 'z0230/iso_t{}.dat'.format(key)
    with open(outname, 'w') as fout:
        fwrite = csv.writer(fout, delimiter = ' ')
        fwrite.writerow(['#Vmag', 'V-I'])
        fwrite.writerows(dict[key])

plt.gca().invert_yaxis()
plt.xlabel('V-I')
plt.ylabel('V')
plt.title('CMDs for z=0.0230')
plt.legend(title = 'log(age)')
plt.show()
