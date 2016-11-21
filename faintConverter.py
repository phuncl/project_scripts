import numpy as np
import time

datafile = open('ing_standards.txt', 'r')
std_raw = np.loadtxt(datafile, dtype='str', skiprows=2)

dimensions = std_raw.shape
std_table = np.zeros(dimensions, dtype='<U14')

for row in range(0,dimensions[0]):
    for column in range(0,dimensions[1]):
        entry = std_raw[row][column]
        value = entry[2:-1]
        print(entry,value)
        #time.sleep(1)
        std_table[row][column] = value

print(std_table)

np.savetxt('ing_standards.csv', std_table, delimiter='  ', fmt='%s')