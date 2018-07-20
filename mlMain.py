import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from scipy.io.wavfile import read  # reading wav files
import os # open files in loop #change working diectory #count files in directory 
import glob # looping throught all files in folder # to read file names into list
import csv # for combining the two csv files
import re # for converting string into list

from slidingWindow import slidingWindow
from hdv import hdv  
from labels import labels 
from labelsH import labelsH 
from transferFile import transfer
from ddg2 import ddg2
from pca22 import pca22
from kmcpca import kmcpca
from kmcAnnotate import kmcAnnotate
from kmcAll import kmcAll

"""
Input:  start = start time
        end = amout of file to look at
        slow = shift in aperture
        fast = width of aperture
        trim = to make each row same length 
        SampleRateRedux = desimate, based on nyquist sampling theorm
        n_clusters = number of clusters 
        basepath = location of data
Output: selected ml algorithum

Note: all input files must be the same lengths
"""

def main():
        
        # start time 
        start = 1 
        # end time 
        end = 3   
        # slow time 
        slow = 0.002 
        # fast time 
        fast = 0.007 
        # trimmed length
        trim = 88200 
        # sample rate redux 
        SampleRateRedux = 6 
        # number of target groups #3 for pipes, 6 for microphones 
        ngroup = 3 #6 
        # location of data
        basepath = 'C:/.../ml/DataCluster'
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
        print 'number of groups: {0}'.format(ngroup)

        print 'the data is taken from: {0}'.format(basepath)
        print 'the number of files in the full directory is: {0}'.format(nbr)


        ####################################################################
        ###### creates dictionary of the wave files with file name as key ##

        lfile1 = {}
        for k in range(0, nbr): 
                lfile1['log{0}'.format(k)] = read(fillist[k], mmap=False) 


        #################################################################
        ##### modifies row names for readability ########################
        
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



        #############################################
        ###### creates sliding window matrix ########
        
        fftL = {} # log of fourier transform  
        
        for q in range (0, nbr):  # loops through files in folder  
                fftL['fftlMel{0}'.format(q)] = slidingWindow(start, end, slow, fast, lfile1['log{0}'.format(q)], SampleRateRedux) # fftE['fftMel{0}'.format(q)], fftL['fftlMel{0}'.format(q)] = slidingWindow(start, end, slow, fast, lfile1['log{0}'.format(q)], SampleRateRedux)
 
        matdim = fftL['fftlMel0'].shape
        print "each windowed matrix is {0} rows by {1} columns".format(matdim[0],matdim[1]) 


        ########################################################################
        # creates row in data frame for each wav file in fillist then fills ####
        # each row with hdv program that concatinates rows of windowed matrix ##
        
        dfcol = matdim[0]*matdim[1] 

        fftLarray = np.zeros((nbr, dfcol), dtype=complex) # 

        for r in range (0, nbr):   #loops through elemnts in dictionary  
                fftLarray[r,:] = hdv(trim, fftL['fftlMel{0}'.format(r)], SampleRateRedux, start, end, slow, fast) 
                 
        rffttL = np.real(fftLarray) # real component of the fft log
        print 'each of the {0} vectors is {1} long'.format(nbr, dfcol)


        #################################################################
        ##### csv file to use in R  #####################################

        np.savetxt("cluster{0}.txt".format(dfcol), rffttL, delimiter=",") #np.savetxt("cluster{0}.txt".format(dfcol), rfftt, delimiter=",") #

        transfer("cluster{0}.txt".format(dfcol), basepath) #

        with open("names{0}.txt".format(dfcol), "w") as text_file: #
                text_file.write(str(nameListtt))
        
        transfer("names{0}.txt".format(dfcol), basepath) #


        #################################################################
        # creates list of cluster labels from wav file names and ########
        ## creates dictionary of names with true cluster labels as key ##
        
        mlLabels = labels(ngroup, nbr, fillist) # creat vertical array
        mlLabelsH = labelsH(ngroup, nbr, fillist) # creat horizontal array

        mlLabelsD = {} 
        for u in range (0, nbr):  
            mlLabelsD[fillistAbv[u]] = mlLabels[u][0] 

        ##########################################################
        ##### Machine Learning Algorithums #######################
            
        #ddg2(rffttL, ngroup, fillistAbv, mlLabels, mlLabelsD) #  drodendrogram heirarchal clustering
        #pca22(rffttL, ngroup, fillistAbv, mlLabels, mlLabelsD) #  pca colored by truth  
        #kmcpca(rffttL, ngroup, fillistAbv, mlLabels, mlLabelsD, mlLabelsH) # colored by cluster, pca for dim reduction  
        #kmcAnnotate(rffttL, ngroup, fillistAbv, mlLabels, mlLabelsD, mlLabelsH) # kmeans labeled points (scatter plot of first 2 dimensions)    
        kmcAll(rffttL, ngroup, fillistAbv, mlLabels, mlLabelsD, mlLabelsH) # color by kmeans on all dimensions (scatter plot first two dimensions)    
        
if __name__ == '__main__':
        main() 
