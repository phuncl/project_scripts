# project_scripts

This repository contains the programs written for our final year project, along with some other vital files
The programs should be run in the following order on a data set, following from `process_colours`:

> viewImages.py         from central data folder
    remove blurred images from data before further processing
    
> groupdata.py          from central data folder
    arranges data from all viewings of an object
    creates 'sorted' files for all objects
    
> dataReader.py         from central data folder
    creates 'CombinedData' Directory structure
    arrages 'sorted' files into CombinedData directory
    
> instrumentMags.py     from central data folder
    calculates median above atmosphere magnitudes of everything
    creates 'zero_magnitude_data.csv' and 'median_aamags.csv' for Standards
    applies airmass correction to produce aa_mag values

> zeroPoints.py          from central data folder
    calculate zero point magnitdue for each filter
    applies zero point correction to Science objects
    creates 'true_mags_CLUSTERNAME.csv' for clusters in Science

> cmdMaker.py            from central data folder
    plots CMD in V vs V-I
...
