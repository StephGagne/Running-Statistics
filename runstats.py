#################################################################################
##    Copyright 2010-2014 Stephanie Gagne                                      ##
##                                                                             ##
##    Licensed under the Apache License, Version 2.0 (the "License");          ## 
##    you may not use this file except in compliance with the License.         ## 
##    You may obtain a copy of the License at                                  ## 
##                                                                             ## 
##      http://www.apache.org/licenses/LICENSE-2.0                             ## 
##                                                                             ##
##    Unless required by applicable law or agreed to in writing, software      ## 
##    distributed under the License is distributed on an "AS IS" BASIS,        ##
##    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. ##
##    See the License for the specific language governing permissions and      ##
##    limitations under the License.                                           ##
#################################################################################


from pylab import *
import numpy as np
import scipy.stats.stats as st
import copy


def medabsdev(x,axis=0):
    """medabsdev(x,axis=0). Calculates and returns the median absolute deviation (MAD) based on https://en.wikipedia.org/wiki/Median_absolute_deviation (last visited June 2014). This function handles NaNs and masked values (masked arrays) by ignoring them.
    x (input) is the array on which the MAD is calculated.
    axis is the axis along which the MAD is calculated. Default is 0."""
    x=copy.deepcopy(x)
    if 'array' not in str(type(x)).lower(): raise TypeError("x must be an array.")
    if 'ma' in str(type(x)).lower():
        try: x[x.mask]=nan
        except: raise TypeError("Tried to translate masks into NaNs but failed.")
    if axis==0:
        med=st.nanmedian(x)
        mad=st.nanmedian(abs(x-med))
    elif axis==1:
        med=st.nanmedian(x.transpose())
        mad=st.nanmedian(abs(x.transpose()-med))
    return mad


def run_stats(x,n):
    """runstats(x,n). Calculates and returns the running mean, median, standard deviation, and median absolute deviation (MAD). This function handles NaNs and masked values (masked arrays) by ignoring them.
    x (input) is the array on which the running statistics are calculated (only one dimension, 1D array).
    n is the number of points taken in the running statistics window."""
    x=copy.deepcopy(x)
    try: x.mask
    except: 
        x=np.ma.array(x,mask=False)

    if len(np.shape(x))>2: raise ValueError("The array provided has more than 2 dimensions, at most 1 or 2 dimensions can be handled.")
    try: [ro,co]=np.shape(x)
    except: ro=np.shape(x)[0]; co=1
    if ro==1 or co==1: 
        ro=max(ro,co)
        x=x.reshape(ro,)
    else: raise ValueError("The array must be a vector (one column or row)")
    # initializing matrix
    M=ones([ro,n])*NaN;
    M=ma.asanyarray(M)
    
    # building matrix
    if n%2==1:       # if n is odd
        for j in range(int(n/2),0,-1):
            posi=int(n/2)-j       # current position
            M[0:ro-j,posi]=x[j:]
        for j in range(1,2+int(n/2),1):
            posi=int(n/2)+j-1;
            M[j-1:,posi]=x[0:(ro+1)-j]
    elif n%2==0:        # if n is even
        for j in range(n/2,0,-1):
            posi=n/2-j
            M[0:ro-j,posi]=x[j:]
        for j in range(1,n/2+1):
            posi=n/2+j-1;
            M[j-1:,posi]=x[0:(ro+1)-j]
    else: print("Well, that's pretty weird. Are you sure n is an integer?")  
    
    M.data[M.mask]=nan
    ave=st.nanmean(M, axis=1);
    med=st.nanmedian(M, axis=1);
    stde=st.nanstd(M, axis=1);
    mad=medabsdev(M,axis=1)
    return [ave, med, stde, mad]
