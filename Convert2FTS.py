"""Convert each photometry file into a FTS"""

import glob as g
import numpy as np
from astropy.io import fits

def photinput(filename):
    datafile = open(filename, "r")

    dataarray = np.genfromtxt(filename, delimiter="  ", dtype=None)
    print(dataarray)
    headersarray = ['BJD','OBJECT_ID','X','Y', 'RSI', 'RSO', 'FLUX', 'FLUX_ERR', 'AIRMASS', 'FLAG', 'FLUX_MAX']
    datafile.close()

    return dataarray, headersarray


def fitsoutput(arrayname, headersname, outputname):
    outputcols = fits.ColDefs([])

    datacolumn = fits.Column(name=headersname[1],format="A", array=arrayname[:,1] )
    outputcols.add_col(datacolumn)

    datacolumn = fits.Column(name=headersname[0], format="D", array=arrayname[:, 0])
    outputcols.add_col(datacolumn)

    for column in range(2, len(headersname)):
        datacolumn = fits.Column(name=headersname[column], format="D", array=arrayname[:, [column]])
        outputcols.add_col(datacolumn)

    anything = fits.BinTableHDU.from_columns(outputcols)
    anything.writeto(outputname, clobber=True)

    del outputcols

#Create a list of all files, including those in subdirectories
print('Converting the following photometry files to FTS format...')
EVERY_FILE = g.glob('**/*.phot', recursive=True)         #Change this to .phot 'MEMBER

print(EVERY_FILE)

#Convert each phot file found into fts
for file in EVERY_FILE:
    arrayname, headersname = photinput(file)
    outputname = file + '_processed.fts'

    #fitsoutput(arrayname, headersname, outputname)
    #print(file + ' successfully converted')

print('All photometry files successfully converted into FTS')
