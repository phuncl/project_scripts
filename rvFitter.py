"""
Fit a sin curve to radial velocity data
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import leastsq
import glob as g

flist = g.glob('*')
for i, entry in enumerate(flist):
    print(str(i) + '\t' + entry)
index = int(input('Give index of desired file: '))
fname = flist[index]

d_phase = []
d_rv = []
err = []

with open(fname, 'r') as fin:
    fin.readline()
    for line in fin:
        newline = line.split()

        d_phase.append(float(newline[0]))
        d_rv.append(float(newline[1]))
        err.append(float(newline[2]))

phase = np.asarray(d_phase)
rv = np.asarray(d_rv)

N = len(phase)
purephase = np.arange(-0.5, 0.5, 0.01)

guess_mean = 0
guess_semiamp = 20
guess_offset = np.pi

guess_plot = guess_semiamp*np.sin(purephase*np.pi + guess_offset)

optimize_func = lambda x: x[0]*np.sin(phase*np.pi + x[1]) + x[2] - rv

cal_std, cal_offset, cal_mean = leastsq(optimize_func,
                                       [guess_semiamp, guess_offset, guess_mean])[0]

cal_plot = cal_std*np.sin(phase*np.pi + cal_offset) + cal_mean

print('Least squares fit parameters')
print('Mean =', cal_mean)
print('Semi-amplitude =', cal_std)
print('Phase offset =', cal_offset)

plt.plot(phase, rv, '.', color = 'grey')
plt.plot(purephase, guess_plot, 'o', label='parameters from exonailer')
plt.plot(phase, cal_plot, 'o', label='optimised parameters')
plt.legend()
plt.show()
