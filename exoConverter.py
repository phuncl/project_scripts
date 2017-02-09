"""
This program will convert the output .txt file from process and analyse
to a format readable by exonailer.
Analyse outputs:
JD-MID      HJD-MID     BJD_TBD-MID     FLUX    FLUX_ERR    MAG     MAG_ERR
Exonailer requires:
Time        Data        Error       Instrument Name
"""

import os
import csv
import glob as g


INSTRUMENT = 'NITES-40CM'
CWD = os.getcwd()

# Select file to convert for exonailer
trans_files = g.glob('*.txt')
trans_data = 'empty'
confirm = 'n'
while confirm != 'y':
    print('\nThe following .txt files are available in this directory:\n')
    for i, item in enumerate(trans_files):
        print(str(i+1) + '\t' + trans_files[i])

    choice = int(input("\nInput the index of the desired file: "))-1

    try:
        trans_data = trans_files[choice]
        confirm = input('\nYou have chosen {} to convert.\nIs this correct? (y/n) '.format(trans_data))
    except IndexError:
        print('Invalid selection!\n')

# write data to memory
print('Reading transit data ...')
data_frame = []
with open(trans_data, 'r') as inf:
    inf.readline()
    for line in inf:
        data_frame.append(line[:-1].split())

# Need to take BJD time, data, error from data
output_frame = []
for line in data_frame:
    time = float(line[2])
    flux = float(line[3])
    flux_err = float(line[4])

    output_frame.append([time, flux, flux_err])
print('Done!\n')

# write to new file in exonailer/transit_data
os.chdir('/media/sf_LinuxShare/pythonscripts/exonailer/transit_data/')
print('Writing data to file in', os.getcwd(), '...')
out_name = trans_data.split('_')[1] + '_lc.dat'
with open(out_name, 'w') as outf:
    outw = csv.writer(outf, delimiter=' ')
    outw.writerows(output_frame)

print('Done!\n')
print('Data converted to format readable by exonailer, and saved', out_name, 'in exonailer/transit_data/')