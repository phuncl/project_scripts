import os
import glob as g
from photometry.ds9 import (
    setUpDs9,
    ds9Display
    )

ds9_name = 'my_ds9'
setUpDs9(ds9_name)
image_list = g.glob('**/*.fts', recursive=True)

if not os.path.exists('junk'):
    os.mkdir('junk/')

for image in image_list:
    # display the image, print name and path within 'data' directory
    ds9Display(ds9_name, image)
    print(image)
    temp = os.path.dirname(os.path.realpath(image))
    parent = temp.split('data')
    print(parent[1])
    # take a verdict, while loop checks for correct input
    response_check = 0
    
    while response_check == 0:
        response = input('Is this image ok? (y/n): ')
        if response.lower() == 'y':
            response_check = 1
        elif response.lower() == 'n':
            response_check = 1
        else:
            response_check = 0
            print('Incorrect input')
	
    # bad images moved to junk folder
    if response.lower() == 'n':
        os.system('mv {}* junk/'.format(image.split('.f')[0]))
        print('Image moved to junk')
    else:
        print('Hurray!')

print('All images have been checked, GG')
