import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import wave
import sys
from scipy.io.wavfile import read  # reading wav files
from scipy import fftpack, ndimage # fast fourier transform
import math
import cmath
import pylab
import re # for converting string into list

"""
Create list of groups 
Input:  ngroup = number of groups to color
        nbr = number of files in folder
        fillist = np array of labels
Output: mlLabels = np array of labels

"""

def labelsH(ngroup, nbr, fillist):

    mlLabels = np.zeros(nbr, dtype=int) 

    # clustering by pipes    
    if ngroup == 3:
        for t in range (0, nbr):  
                if 'PC' in fillist[t]: 
                    mlLabels[t] =  0 
                elif 'PL' in fillist[t]: 
                    mlLabels[t] =  2 
                elif 'PS' in fillist[t]: 
                    mlLabels[t] =  1 

    # clustering by mic    
    elif ngroup == 6:
        for t in range (0, nbr):  
                if 'Mi01' in fillist[t]: 
                    mlLabels[t] =  0
                elif 'Mi02' in fillist[t]: 
                    mlLabels[t] =  1
                elif 'Mi03' in fillist[t]: 
                    mlLabels[t] =  2
                elif 'Mi04' in fillist[t]: 
                    mlLabels[t] =  3
                elif 'Mi05' in fillist[t]: 
                    mlLabels[t] =  4
                elif 'Mi06' in fillist[t]: 
                    mlLabels[t] =  5
    else:
        print 'need labels for option ngroup = {0}'.format(ngroup)

    return mlLabels