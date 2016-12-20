'''
Collect calibrated data for standard stars and plot vs database
'''

import os
import csv
import glob as g
from scipy import stats
import matplotlib.pyplot as plt


def linreg(xlist, ylist):
    """Hand 2 lists to plot"""
    slope, intercept, r_value, p_value, std_err = stats.linregress(xlist, ylist)
    return [slope, intercept, r_value, p_value, std_err]

os.chdir('/media/sf_LinuxShare/CSVcheck/CombinedData/Standards')

std_file = open('ing_standards.csv', 'r')
std_reader = csv.reader(std_file, dialect='excel')
next(std_reader)

FILTERS = {'B': 0,
           'V': 1,
           'R': 2,
           'I': 3}

STANDARDS = {}
for line in std_reader:
    STANDARDS[line[-1]] = line[1:-1]
std_file.close()

x_dummy = [10, 15, 19]
y_dummy = [10, 15, 19]

x_B = []
y_B = []

x_V = []
y_V = []

x_R = []
y_R = []

x_I = []
y_I = []

output = []

cal_list = g.glob('truemag*')
for item in cal_list:
    cal_file = open(item, 'r')
    cal_reader = csv.reader(cal_file)

    for line in cal_reader:
        starname = line[0]
        filt = line[1]
        cal_mag = line[2]

        try:
            known_mag = STANDARDS[starname][FILTERS[filt]]

            if filt == 'B':
                x_B.append(known_mag)
                y_B.append(cal_mag)

            elif filt == 'V':
                x_V.append(known_mag)
                y_V.append(cal_mag)

            elif filt == 'R':
                x_R.append(known_mag)
                y_R.append(cal_mag)

            elif filt == 'I':
                x_I.append(known_mag)
                y_I.append(cal_mag)

            else:
                print('Unknown filter.')

            output.append([known_mag, cal_mag])
        except:
            pass

# dataplot = plt.figure()

x_data = [x_B, x_V, x_R, x_I]
y_data = [y_B, y_V, y_R, y_I]

again = 'y'
while again == 'y':
    pick_filt = input('Please choose a filter to view:\nB, V, R, I\n').upper()

    x = x_data[FILTERS[pick_filt]]
    y = y_data[FILTERS[pick_filt]]
    plt.plot(x_dummy, y_dummy)
    plt.plot(x, y, 'o')
    plt.xlabel('Known Magnitude')
    plt.ylabel('Calibrated Magnitude')
    plt.title(pick_filt + ' data')
    plt.show()

    file_name = pick_filt + '_calibrated_plot.csv'
    file_var = open(file_name, 'w')
    file_writer = csv.writer(file_var)

    for i in range(0, len(x)):
        file_writer.writerow([x[i], y[i]])

    file_var.close()

    # fit_data = linreg(x_data[FILTERS[pick_filt]],y_data[FILTERS[pick_filt]])
    # print('Slope =', fit_data[0], '\n',
    #      'Intercept =', fit_data[1], '\n',
    #      'std_err =', fit_data[4], '\n',
    #      'correlation coefficient = ', fit_data[2], '\n')

    again = input('View another plot? y/n\n').lower()

print('Exiting...')
