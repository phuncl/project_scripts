"""
Lite version of exposure metre program
Opens combined proc file and reads in fit params for all filters
Then exposure calculation
"""

import numpy as np

# FUNCTIONS


def calc_exposurerec():
    # open desired filter and allow calculation of exposure for a given magnitude
    req_filter = input('Which filter do you require?\nPlease enter either B, V, R, or I:\n').upper()

    fit_data = all_vals[FILTERS.index(req_filter)]
    slope = fit_data[0]
    intercept = fit_data[1]

    input_mag = float(input('Enter the magnitude of the object:\n'))
    output_max_exposure = np.power(10, (slope * input_mag + intercept))

    print('Object of magnitude', input_mag, 'has recommended exposure of',
          float('{0:.2f}'.format(output_max_exposure)), 'seconds.')

    return 0


# MAIN FUNCTION

FILTERS = ['B', 'V', 'R', 'I']

# create holders for slope and intercept
B_vals = [0.38612, -2.14841]
V_vals = [0.30761, -1.73925]
R_vals = [0.36680, -2.44566]
I_vals = [0.37485, -2.56855]
all_vals = [B_vals, V_vals, R_vals, I_vals]

exit_request = 0
while exit_request == 0:
    calc_exposurerec()
    exit_check = input('Would you like to check another object? (y/n) ')

    if exit_check.lower() == 'y':
        pass
    else:
        print('Exiting program...')
        exit_request += 1
# program ends
