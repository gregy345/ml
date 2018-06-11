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
from hdv import hdv
import os # open files in loop #change working diectory #count files in directory
import glob # looping throught all files in folder
from SyntheticAperture import syntheticAperture
from SyntheticAperture2 import syntheticAperture2
from labels import labels 
from transferFile import transfer
from ddg2 import ddg2
from pca22 import pca22
import glob # to read file names into list
import csv # for combining the two csv files
import re # for converting string into list

############################################################################
# scipy.io.wavfile.read comand gives Warning b/c meta data added by Audacity
# to remove warning use 'python -W ignore clusterMain.py' in comand line
# or else uncomment next two lines to use filter
#import warnings 
#warnings.filterwarnings("ignore") 
############################################################################


"""

Input:  start = start time
        end = amout of file to look at
        slow = shift in aperture
        fast = width of aperture
        trim = to make each row same length 
        SampleRateRedux = to make it run faster
        decimate = only take every mth row of aperture when creating vector (not working yet)
        n_clusters = number of clusters 
        basepath = location of data
Output: ml
Note: all input files must be the same lengths
"""

def main():
        # start time? 
        start = 0
        # end time? 
        end = 2  
        # slow time? 
        slow = 0.002 
        # fast time? 
        fast = 0.007 
        # what is trimmed length ?"
        trim = 88200 #44100 
        # sample rate redux? # this is based on nyquist sampling theorm
        SampleRateRedux = 6 #1 
        # what is the number of target groups? #3 for pipes, 6 for microphones 
        ngroup = 3 #6 #3 
        # location of data? 
        basepath = '...../ml/DataCluster'

        # changes working directory to folder that has been specified
        os.chdir(basepath) 
        # next line counts the number of files in the folder
        nbr=len([name for name in os.listdir(basepath) if os.path.isfile(os.path.join(basepath,name))])

        # creates list of files in folder
        fillist = os.listdir(basepath) 
        # puts files in correct order
        fillist.sort() 
 
        print '  '
        print 'start time: {0}'.format(start)
        print 'end time: {0}'.format(end)
        print 'slow time (step in window): {0}'.format(slow)
        print 'fast time (width of window): {0}'.format(fast)

        print 'trim: {0}'.format(trim)
        print 'sample rate redux: {0}'.format(SampleRateRedux)
        #print 'decimate: {0}'.format(decimate)
        print 'number of groups: {0}'.format(ngroup)#print 'number of clusters: {0}'.format(n_clusters)#

        print 'the data is taken from: {0}'.format(basepath)
        print 'the number of files in the full directory is: {0}'.format(nbr)
        print 'the first file : {0}'.format(fillist[0])

        print 'path to file name list:'
        #print fnames # location of the data
        print basepath # location of the data
        print 'file name list:'
        lenName = len(fillist[0])
        print 'name length: {0}'.format(lenName) ##print lenName

        # creates dictionary of the wave files with file name as key
        # scipy.io.wavfile.read comand gives error b/c meta data added by Audacity
        lfile1 = {}
        for k in range(0, nbr): #nbr = 132
                lfile1['log{0}'.format(k)] = read(fillist[k], mmap=False)
                #lfile1['log{0}'.format(k)] = read(fillist[k])
        
        #print 'dictionary rounds'#print rounds#print 'dictionary lfile1'#print lfile1

        #############################################
        ###### creates sliding window matrix ########
        #############################################
        fftE = {} # fouirer transfomr of sliding window matrix  
        fftL = {} # log of fourier transform  
        
        for q in range (0, nbr):  # loops through files in folder  #nbr = 132
                #fftE['fftMel{0}'.format(q)], fftL['fftlMel{0}'.format(q)] = syntheticAperture2(start, end, slow, fast, lfile1['log{0}'.format(q)], SampleRateRedux)#, decimate)
                fftE['fftMel{0}'.format(q)], fftL['fftlMel{0}'.format(q)] = syntheticAperture(start, end, slow, fast, lfile1['log{0}'.format(q)], SampleRateRedux)#, decimate)

        print "the length of which is:{0}".format(len(fftE['fftMel0']))

        # correct size of empty vector for hdv to fill 
        matdat = fftE['fftMel0'] #fftE['fftMel{0}'.format(q)] #
        dimen = matdat.shape #print 'dimen'#print dimen
        row = dimen[0] #row = (dimen[0])/decimate #996
        col = dimen[1] #308
        dfcol = row*col
        columns = dfcol # quick fix for consistency, fix later
        print 'clusterMain line 139 columns aka dfcol'
        print columns
        
        ###########################################################
        # creates list of cluster labels from wav file names ######
        ###########################################################
        
        clusterLabels = labels(ngroup, nbr, fillist)

        #################################################################
        ##### modifies row names for readability ########################
        #################################################################

        fillistST = map(lambda each:each.strip(".wav"), fillist) # removes .wav

        nameList = ( ",".join( repr(e) for e in fillistST)) # list into string (remove brackets)

        nameListnoc = ( " ".join( repr(e) for e in fillistST)) # list into string (remove brackets)

        for s in range (0, nbr):  # loop to remove underscore
                nameListt = nameList.replace("_", "")

        for t in range (0, nbr):  # loop to remove unused variables
                nameListtt = nameListt.replace("MaHH", "")

        for w in range (0, nbr):  # loop to remove quotes
                nameListttt = nameListtt.replace("'", "")

        fillistAbv = re.sub("[^\w]", " ", nameListtt).split() #import re #strint back to list

        fillistAbvnoc = re.sub("[^\w]", " ", nameListnoc).split() #import re #strint back to list

        fillistAbvTex = re.sub("[^\w]", " ", nameListttt).split()
    
        ###########################################################
        # creates row in data frame for each wav file in fillist ##
        # hdv #####################################################
        ###########################################################

        fftEarray = np.zeros((nbr, dfcol), dtype=complex) # 
        fftLarray = np.zeros((nbr, dfcol), dtype=complex) # 

        for r in range (0, nbr):   #loops through elemnts in dictionary 
                fftEarray[r,:], fftLarray[r,:] = hdv(trim, fftE['fftMel{0}'.format(r)], SampleRateRedux, start, end, slow, fast) #, decimate) #
                #fftEarray[r,:], fftLarray[r,:] = mdv(trim, fftL['fftlMel{0}'.format(r)], SampleRateRedux, start, end, slow, fast, decimate) #

        rfftt = np.real(fftEarray) # real component of the fft
        rffttL = np.real(fftLarray) # real component of the fft log

        #################################################################
        ##### csv file to use in R  #####################################
        #################################################################

        np.savetxt("cluster{0}.txt".format(columns), rfftt, delimiter=",")

        transfer("cluster{0}.txt".format(columns), basepath)

        with open("names{0}.txt".format(columns), "w") as text_file:
                text_file.write(str(nameListtt))
        
        transfer("names{0}.txt".format(columns), basepath)

        ############################################################################
        ## creates dictionary of names with true cluster labels as key #############
        ############################################################################

        clusterLabelsD = {} 
        for u in range (0, nbr):  
            clusterLabelsD[fillistAbv[u]] = clusterLabels[u][0] 

        ##########################################################
        ##### clustering analysis of data frame just created #####
        ##########################################################

        #ddg2(rffttL, ngroup, fillistAbv, clusterLabels, clusterLabelsD) #  drodendrogram 
        pca22(rffttL, ngroup, fillistAbv, clusterLabels, clusterLabelsD) #  principal components analysis 
        
if __name__ == '__main__':
        main()