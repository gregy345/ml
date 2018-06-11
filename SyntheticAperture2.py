import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import wave
import sys
from scipy.io.wavfile import read
from scipy import fftpack, ndimage
import math 
import re
 
"""
Compute the synthetic appeture matrix
	Input:  start = the starting time of the sinal (seconds) 
		end = the end time of the sinal (seconds)  
		slow = the slow time of the sinal (seconds)  
		fast = the fast time of the sinal (1xP seconds)  
		sound = wave file 
Output: matrix of pressures (NxP)
		matrix of fast fourier transform in both directions of pressures (NxP)
		matrix of log of fast fourier transform in both directions of pressures (NxP)
		dim = 
"""
def syntheticAperture2(start, end, slow, fast, sound, decimateS): #SampleRateRedux): #, decimate):
	# the frequency will always be 44100 when using wave files 
	#hz = 44100 
	samplerate = 44100/decimateS # samplerate = 44100/SampleRateRedux #
	# convert varibles from seconds to indices in file
	iterations = int(float((end-start-fast)*(1/slow)))    
	StStart = int(float(start*samplerate))
	StSlow = int(float(slow*samplerate))
	StFast = int(float(fast*samplerate))

	# imports the wave file
	l = np.array(sound[1],dtype=float)
	b = l[0::decimateS] # b = l[0::SampleRateRedux] #
	ttMat = np.zeros((iterations, StFast), dtype=complex)
	for j in range(0, iterations): # number of rows?
		for i in range(0, StFast): # number of columns?
			ttMat[j,i] = b[i+(j*StSlow)] 
	
	# the following leads to differnt clusters
	# look into it to see if it works better for pipes
	
	# decimate by ratio of fast to slow, rounded down to intiger, to remove repeat data 
	# is this kosher?  the hole purpose of sliding window is to normalize different frequencies 
	# from different windows in the sound
	decimate = int(fast/slow) #decimate = math.floor(fast/slow) #
	#ttMat = ttMat[0::decimate]  # decimate before fft

	#fftt = fftpack.fft2(ttMat) # 2 way fourier, better for energy difference 
	fftt = fftpack.fft(ttMat) # 1 way fourier, better for normalizing data, helps with decay
	fftlog = np.array(np.log10(np.abs(fftt)), dtype=complex) # log and absulute value

	dimen = fftt.shape #dimen = sound.shape #print 'dimen'#print dimen
	row = dimen[0] #row = (dimen[0])/decimate #996
	col = dimen[1] #308
	dim = row*col 
	
	#print 'before SyntheticAperture row, col, dim'
	#print row
	#print col
	#print dim
	
	fftt =  fftt[0::decimate] # decimate after fft
	fftlog = fftlog[0::decimate] 

	dimen = fftt.shape #dimen = sound.shape #print 'dimen'#print dimen
	row = dimen[0] #row = (dimen[0])/decimate #996
	col = dimen[1] #308
	dim = row*col 
	
	#print 'after SyntheticAperture row, col, dim'
	#print row
	#print col
	#print dim
	
	return fftt, fftlog #

