Running-Statistics
==================

Function that returns running statistics of the same shape as the input. 
The function ignores NaNs and masked data (from masked arrays): the calculation will apply to all non-NaNs and non-masked numbers in the running window.

This file includes function run_stats(x,n) where x is the data and n is the number of point in the running window.
At the moment, the function returns the running: mean, median, standard deviation and MAD (median absolute deviation). 

This file also includes function medabsdev(x,axis) that calculates the MAD inside run_stats.

The code is slow when the running window is large. Suggestions that would improve the speed are very welcome. All suggestions welcome. Please, use the issues system. 

I am planning to add features to choose the running stats to be performed in the options, to avoid unnecessary calculations. In a foreseeable future.

