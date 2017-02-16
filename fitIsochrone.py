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
    for i, thing in enumerate(files):
        print(str(i) + '\t' + thing)
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


def age_pick(priorpick):
    if not priorpick:
        print('log(age) values available are:')
        ages = []
        for i, item in enumerate(temp_isos):
            age = item.split('_')[2][1:4]
            ages.append(age)
        ages.sort()
        for j, item in enumerate(ages):
            print(str(j) + '\t' + str(item))
        agechoice = ages[int(input('Give index of desired age: '))]
    else:
        agechoice = priorpick

    pluschoice = float(agechoice) + 0.1
    minuschoice = float(agechoice) - 0.1
    narrowed_isos = {}
    for ckey in temp_isos:
        if agechoice in ckey:
            narrowed_isos[ckey] = temp_isos[ckey]
        if str(pluschoice) in ckey:
            narrowed_isos[ckey] = temp_isos[ckey]
        if str(minuschoice) in ckey:
            narrowed_isos[ckey] = temp_isos[ckey]

    return narrowed_isos, agechoice


def dist_mod_reddening(prev_offset, prev_reddening):
    if prev_offset and prev_offset:
        print('Previous offset =', prev_offset)
        print('Previous reddening =', reddening)
    d = float(input('\nWhat magnitude offset to add to isochrones? '))
    red = float(input('\nWhat reddening correction to add to isochrones? '))

    return d, red


def plot_clust_isochrones(choice):
    with open(choice, 'r') as clust:
        clust_read = csv.reader(clust)
        next(clust_read)

        # plot V against V-I
        mag_data = []
        col_data = []

        for cline in clust_read:
            if math.isnan(float(cline[1])) or math.isnan(float(cline[3])):
                continue
            mag_data.append(cline[1])
            col_data.append(float(cline[1])-float(cline[3]))

        # calculate distance
        power = float(offset)/5 + 1
        distance = math.pow(10, power)

        print('Showing isochrone at a distance of', distance, 'pc.')

        plt.plot(col_data, mag_data, 'o', color='grey', alpha=0.75)

        keys = []
        for key in used_isos:
            keys.append(key)
        keys.sort()

        for key in keys:
            isodata = used_isos[key]
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
        next(isoread)  # skip headers
        for line in isoread:
            isodict[isoname].append(line)

metallicities = []
for key in isodict:
    newm = key.split('_')[1].split('.')[0][1:]
    if newm not in metallicities:
        metallicities.append(newm)
metallicities.sort()

chosen_age = False

cluster = clust_pick()
temp_isos, metallicity = metal_pick()
used_isos,chosen_age = age_pick(chosen_age)
offset, reddening = dist_mod_reddening(False, False)

actions = ('Quit', 'Choose cluster', 'Set metallicity estimate', 'Set age estimate', 'Set distance modulus and reddening', 'Plot')

print('\nChoose an action:')
for i,item in enumerate(actions):
    print(str(i) + '\t' + item)
option = int(input('Give index of desired action: '))

while option != 0:
    if option == 1:
        cluster = clust_pick()

    elif option == 2:
        temp_isos, metallicity = metal_pick()
        used_isos, chosen_age = age_pick(chosen_age)


    elif option == 3:
        used_isos,chosen_age = age_pick(False)

    elif option == 4:
        offset, reddening = dist_mod_reddening(offset, reddening)

    elif option == 5:
        plot_clust_isochrones(cluster)

    else:
        continue

    print('\nChoose an action:')
    for i,item in enumerate(actions):
        print(str(i) + '\t' + item)
    option = int(input('Give index of desired action: '))