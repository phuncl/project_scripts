"""
To be run on a single cluster at a time.
Allows iterative improvement of distance modulus value
and outputs corresponding distance
"""


import matplotlib.pyplot as plt
import csv
import math
import glob as g
def clust_pick():
    files = g.glob('true_mags_*')
    for i, entry in enumerate(files):
        print(str(i) + '\t' + entry)
    index = int(input('Give index of desired cluster file: '))
    choice = files[index]

    return choice


def metal_pick():
    for i, item in enumerate(metallicities):
        print(str(i) + '\t0.' + item)
    pick = int(input('Give index of desired metallicity: '))
    mpick = metallicities[pick]

    current_isos = {}
    for key in isodict:
        if mpick in key:
            current_isos[key] = isodict[key]

    return current_isos, mpick


def dist_mod_reddening():
    d = float(input('What magnitude offset to add to isochrones? '))
    red = float(input('What reddening correction to add to isochrones? '))

    return d, red


def plot_clust_isochrones(choice):
    with open(choice, 'r') as clust:
        clust_read = csv.reader(clust)
        next(clust_read)

        # plot V against V-I
        mag_data = []
        col_data = []

        for line in clust_read:
            if math.isnan(float(line[1])) or math.isnan(float(line[3])):
                continue
            mag_data.append(line[1])
            col_data.append(float(line[1])-float(line[3]))

        # calculate distance
        power = float(offset)/5 + 1
        distance = math.pow(10, power) + 10

        print('Showing isochrone at a distance of', distance, 'pc.')

        plt.plot(col_data, mag_data, 'o', color='grey', alpha=0.75)

        keys = []
        for key in temp_isos:
            keys.append(key)
        keys.sort()

        for key in keys:
            isodata = temp_isos[key]
            # create V and V-I columns
            isomag = []
            isocol = []
            for line in isodata:
                isomag.append(float(line[0]) + offset)
                isocol.append(float(line[1]) + reddening)
            plt.plot(isocol, isomag, label=key)

        #plt.gca().invert_yaxis()
        plt.xlabel('V-I')
        plt.ylabel('V')
        plt.legend(title='log(age)', loc=2)
        plt.title(choice.split("_")[-1].split(".")[0] + ' for z=0.{}'.format(metallicity))
        plt.axis([-1,2,17,9])
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())
        plt.show()
        plt.clf()


################################################################

# Get all isochrone data
print('Acquiring isochrone data...')
isos = g.glob('/media/sf_LinuxShare/isochrones/files/*')
isodict = {}
for i, entry in enumerate(isos):
    isoname = entry.split('/')[-1]
    isodict[isoname] = []
    with open(entry, 'r') as isofile:
        isoread = csv.reader(isofile, delimiter = ' ')
        next(isoread)
        for line in isoread:
            isodict[isoname].append(line)

metallicities = []
for key in isodict:
    newm = key.split('_')[2].split('.')[0][1:]
    if newm not in metallicities:
        metallicities.append(newm)
metallicities.sort()

cluster = clust_pick()
temp_isos, metallicity = metal_pick()
offset, reddening = dist_mod_reddening()

actions = ('Quit', 'Choose cluster', 'Set metallicity', 'Set distance modulus and reddening', 'Plot')

print('\nChoose an action:')
for i,item in enumerate(actions):
    print(str(i) + '\t' + item)
option = int(input('Give index of desired action: '))

while option != 0:
    if option == 1:
        cluster = clust_pick()

    elif option == 2:
        zchoice, metallicity = metal_pick()

    elif option == 3:
        offset, reddening = dist_mod_reddening()

    elif option == 4:
        plot_clust_isochrones(cluster)


    print('\nChoose an action:')
    for i,item in enumerate(actions):
        print(str(i) + '\t' + item)
    option = int(input('Give index of desired action: '))