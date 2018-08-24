
import numpy as np

"""
import wav file to: 
Input:  fftE = matrix from synthetic aperture program (use non fourier transform matrix)
Output: fftLHdv = array to put into row of matrix 
         
"""
def hdv(fftE): 
        # the frequency will always be 44100 when using wave files

        dimen = fftE.shape 
        row = dimen[0] #996
        col = dimen[1] #51
        dim = row*col # length of vector
        
        hdv = np.zeros((dim, 1), dtype=complex) # creats empty vector

        for j in range(0, row): # number of rows
                for i in range(0, col): # number of columns
                        hdv[i+(j*col)][0] = fftE[j,i] 

        fftHdv = (np.rot90(np.absolute(hdv)))[0] 
        fftLHdv = np.array(np.log10(fftHdv), dtype = complex)

        return fftLHdv 