
import numpy as np

from scipy import fftpack, ndimage
 
"""
Compute the synthetic appeture matrix
	Input:  start = the starting time of the sinal (seconds) 
		end = the end time of the sinal (seconds)  
		slow = the slow time of the sinal (seconds)  
		fast = the fast time of the sinal (1xP seconds)  
		sound = wave file 
		decimatS = factor by which signal is downsampled
Output: fftlog = matrix of log of fast fourier transform in both directions of pressures (NxP)
"""
def slidingWindow(start, end, slow, fast, sound, decimateS): 
	
	# the frequency will always be 44100 when using wave files 
	samplerate = 44100/decimateS 

	# convert varibles from seconds to indices in file
	iterations = int(float((end-start-fast)*(1/slow)))    
	StStart = int(float(start*samplerate))
	StSlow = int(float(slow*samplerate))
	StFast = int(float(fast*samplerate))

	# imports the wave file
	l = np.array(sound[1],dtype=float)
	b = l[0::decimateS] 
	ttMat = np.zeros((iterations, StFast), dtype=complex)
	for j in range(0, iterations): # number of rows
		for i in range(0, StFast): # number of columns
			ttMat[j,i] = b[i+(j*StSlow)] 


	fftt = fftpack.fft(ttMat) # takes fft of matrix along horizontal axis
	fftlog = np.array(np.log10(np.abs(fftt)), dtype=complex) #takes absulute value and log
 
	return fftlog 

