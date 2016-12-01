import csv
import os
import glob as g
import numpy as np
from scipy import stats

###########################################################
#####################   CONSTANTS   #######################
###########################################################

FILTERS = ['B','V','R','I']
CWD = os.getcwd()

os.chdir('/media/sf_LinuxShare/standards_catalogue')
standardfile = open('ing_standards.csv','r')
STANDARD_DICT = {}
catalogue = csv.reader(standardfile, dialect='excel')
for row in catalogue:
    STANDARD_DICT[row[5]]=row[1:-1]
standardfile.close()
os.chdir(CWD)

###########################################################
#####################   FUNCTIONS   #######################
###########################################################

def get_standards():
    """Retrieve standard stars using R filter as reference"""
    os.chdir('R/')
    subdirectories = os.listdir('.') #list dirs in cwd
    standards = []
    for entry in subdirectories:
        if '.' not in entry:
            if entry not in SCIENCE_TARGETS:
                standards.append(entry)
    os.chdir(CWD)
    return standards

def get_sciencetargets():
    """Obtain science targets from text file
    useful once own data obtained"""
    science_targets = []
    datafile = open('science_targets.txt', 'r')
    for line in datafile:
        if line != '':
            science_targets.append(line[:-1])
    datafile.close()
    return science_targets

def mk_exposuredata(filter):
    '''Cycle through all filters'''
    os.chdir(filter + '/')
    mag_expo_list = []

    for target in STANDARDS:
        os.chdir(target + '/')
        filelist = g.glob('sorted*')
        for filename in filelist:
            datafile = open(filename, 'r')
            for temp_line in datafile:
                line = temp_line.split('  ')
                std_name = line[1]

                # edit to csv format
                # fileinfo = csv.reader(datafile, delimiter='  ')

                # for line in fileinfo:
                max_counts = float(line[-2])
                exposure = float(line[-1])

                if 300 < max_counts < 30000:
                    max_flux = max_counts / exposure
                    max_expo = 30000 / max_flux
                    # '3' indexing will need to change with filter
                    try:
                        x = FILTERS.index(filter)
                        mag = float(STANDARD_DICT[std_name][x])
                    except KeyError:
                        print('An error occurred.\n', std_name, 'was not found in the standards star catalogue.')
                        mag = None

                    if mag:
                        mag_expo_list.append([mag, max_expo, std_name])
        os.chdir('..')

    os.chdir('../ExposureMetre')
    # need to change filename with filter
    output_name = str(filter) + 'expo_metre_RAW.csv'

    fileout = open(output_name, 'w')
    filewriter = csv.writer(fileout, delimiter=',')
    filewriter.writerow(['#mag', 'max_expo', 'std_name', ])

    for entry in mag_expo_list:
        filewriter.writerow(entry)

    fileout.close()
    os.chdir('..')

def proc_exposuredata(filter, proc_filename):
    raw_name = filter + 'expo_metre_RAW.csv'
    raw_file = open(raw_name, 'r')
    raw_reader = csv.reader(raw_file, dialect='excel')
    # skip file header
    next(raw_reader, None)
    x_data = []         # magnitude
    y_data = []         # max_expo
    for line in raw_reader:
        x_data.append(float(line[0]))
        y_data.append(np.log10(float(line[1])))
    raw_file.close()

    plot_output = stats.linregress(x_data,y_data)

    proc_file = open(proc_filename, 'w')
    proc_writer = csv.writer(proc_file, dialect='excel')
    proc_writer.writerow(['#slope','intercept','rvalue','pvalue','stderr'])
    proc_writer.writerow(plot_output)
    proc_file.close()

    print(plot_output)

def read_exposuredata(proc_filename):
    proc_file = open(proc_filename, 'r')
    proc_reader = csv.reader(proc_file, dialect='excel')
    next(proc_reader, None)
    plot_data = []
    for line in proc_reader:
        for entry in line:
            plot_data.append(entry)
    proc_file.close()

    return plot_data

def calc_exposurerec():
    # next stage - open desired filter and allow calculation of exposure for a given magnitude
    req_filter = input('Which filter do you require?\nPlease enter either B, V, R, or I:\n')
    # check if processed file already exists - if not, create it
    os.chdir('ExposureMetre')
    proc_filename = req_filter.upper() + 'expo_metre_PROC.csv'
    if not os.path.exists(proc_filename):
        # here create PROC file
        print('Data not yet processed for this filter!\nProcessing data...')
        proc_exposuredata(req_filter, proc_filename)
    else:
        # here read from PROC file
        print('Data already processed, Opening file...')
    fit_data = read_exposuredata(proc_filename)
    slope = float(fit_data[0])
    intercept = float(fit_data[1])

    input_mag = float(input('Enter the magnitude of the object:\n'))
    output_max_exposure = np.power(10, (slope * input_mag + intercept))

    os.chdir(CWD)

    print('Object of magnitude', input_mag, 'has recommended exposure of', float('{0:.2f}'.format(output_max_exposure)), 'seconds.')

    return(0)

###########################################################
#####################     MAIN      #######################
###########################################################

# obtain lists of standard and science target objects

SCIENCE_TARGETS = get_sciencetargets()
STANDARDS = get_standards()

# create subdirectory if needed
if not os.path.exists('ExposureMetre'):
    os.mkdir('ExposureMetre')

# create RAW data files if they do not exist
for filter in FILTERS:
    os.chdir('ExposureMetre/')
    fname = filter + 'expo_metre_RAW.csv'
    if not os.path.isfile(fname):
        os.chdir('..')
        mk_exposuredata(filter)
        print(filter, 'data file created')
    else:
        print(filter, 'file already exists.')
        os.chdir('..')

exit_request = 0
while exit_request == 0:
    calc_exposurerec()
    exit_check = input('Would you like to check another object? (y/n) ')

    if exit_check.lower() ==  'y':
        pass
    else:
        print('Exiting program...')
        exit_request += 1

# program ends