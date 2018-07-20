import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import wave
import sys
from scipy.io.wavfile import read
from scipy import fftpack, ndimage
import math  #fabs
import re

"""
import wav file to: trim, fast fourier transform, decimate
        Input:  fast = the fast time of the sinal (1xP seconds)
                fftE = matrix from synthetic aperture program (use non fourier transform matrix)
                srr = SampleRateRedux = factor by which to reduce size
                dim = 
                clulbb = cluster number associated with a specific row
Output: array to put into row of matrix 
                fftt = ith row in new matrix 
                fftlog = log transform of ith row in new matrix 

"""
def hdv(trim, fftE, srr, start, end, slow, fast):#, decimate): #def mdv(trim, sound, srr, start, end, slow, fast, decimate, clulbb): #
        # the frequency will always be 44100 when using wave files

        dimen = fftE.shape 
        row = dimen[0] #996
        col = dimen[1] #308
        """
        print 'mdv dimenstions'
        print dimen
        print row
        print col
        print decimate
        """
        #columns = int(math.ceil(44100*fast)) #rows = int(math.ceil(44100*((end-start)/slow)))

        dim = row*col 
        #print dim
        
        hdv = np.zeros((dim, 1), dtype=complex) #mdv = np.zeros(dim, dtype=complex)
        """
        print 'mdv'
        print mdv
        """

        for j in range(0, row): # number of rows
                for i in range(0, col): # number of columns
                        hdv[i+(j*col)][0] = fftE[j,i] #

        #bbb= np.rot90(np.absolute(mdv))  #bb = np.absolute(mdv) #bb = abs(mdv) #bb = math.fabs(mdv) #bb = np.fabs(mdv) ##bbb= np.rot90(bb) # transpose of bb array matrix rows=1 columns=xx (horizontal)#bbbb = bbb[0] # array rows=1 columns=nbr (horizontal, removed outer set of brackets)
        fftHdv = (np.rot90(np.absolute(hdv)))[0] # array rows=1 columns=nbr (horizontal, removed outer set of brackets)
        fftLHdv = np.array(np.log10(fftHdv), dtype = complex)

        return fftLHdv # fftHdv, fftLHdv #