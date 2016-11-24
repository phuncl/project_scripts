import csv
import os
import glob as g

FILTERS = ['B','V','R','I']
CWD = os.getcwd()

os.chdir('/media/sf_LinuxShare/standards_catalogue')
standardfile = open('ing_standards.csv','r')
STANDARD_DICT = {}
for line in standardfile:
    line.split(',')
    STANDARD_DICT[line[0]]=line[1:4]
standardfile.close()
os.chdir(CWD)

###########################################################
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
    datafile = open("science_targets.txt", 'r')
    for line in datafile:
        if line != '':
            science_targets.append(line[:-1])
    datafile.close()
    return science_targets

###########################################################
###########################################################

SCIENCE_TARGETS = get_sciencetargets()
STANDARDS = get_standards()

if not os.path.exists('ExposureMetre'):
    os.mkdir('ExposureMetre')

filter_index = -1
for filter in FILTERS:
    filter_index += 1
    mag_exp_list = []

    os.chdir(filter)
    for target in STANDARDS:
        os.chdir(target+'/')
        filelist = g.glob('sorted*')
        for filename in filelist:
            datafile = open(filename, 'r')
            for line in datafile:
                newline = line.split('  ')

                objectname = str(newline[1])
                max_counts = float(newline[10])
                exposure = int(newline[11])
                print(objectname)

                if max_counts < 30000:
                    max_flux = max_counts/exposure
                    max_exposure = 30000/max_flux
                else:
                    max_exposure = 0

                try:
                    mag = STANDARD_DICT[objectname[2:]][filter_index]
                except:
                    print('Star not simply found in database. Skipping...')
                    mag = 0

                if max_exposure and mag:
                    writeline = [max_exposure, mag]
                    print(writeline)
                    mag_exp_list.append(writeline)
        os.chdir('..')

    fileoutname = filter+'_'+'exposureData.csv'
    os.chdir(CWD+'/ExposureMetre/')
    fileout = open(fileoutname,'w')

    datawriter = csv.writer(fileout, delimiter=',')
    for set in mag_exp_list:
        datawriter.writerow(set)
    fileout.close()
    os.chdir(CWD)