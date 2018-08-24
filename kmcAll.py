
import numpy as np
import pylab as pl

from sklearn.cluster import KMeans

import matplotlib.pyplot as plt 

"""
This porgram creates a scatter plot of the first two dimenstions of 
the imputed data matrix.  It then colors each point based on the 
cluster assigned by running k-means clustering algorithum on all the 
dimensions in the imputed data matrix.  

Input:  sound = matrix, each row is from a different wav file
        ncl = number of clusters / centroids
        fna = file names as list
        mlLabels = labels/groups 0,1,2 as array/list 
        mlLabelsD = labels/groups as dictionary
        mlLabelsH = labels/groups as horizontal array/list
        
Output: plot
"""

def kmcAll(sound, ncl, fna, mlLabels, mlLabelsD, mlLabelsH):

        inivar = 'k-means++' # initialization of centroids
        ninivar = 10 # number of iterations
        k_means = KMeans(init=inivar, n_clusters=ncl, n_init=ninivar) 

        k_means.fit(sound) # applies the algorithum to full data set
        k_means_labels = k_means.labels_

        ps = 300
        mlLab = mlLabels.tolist() 
        fig, ax = plt.subplots(figsize=(25,14)) 
        plt.title('{0} = init, {1} = n_clusters, {2} = n_init'.format(inivar, ncl, ninivar), fontsize=30) 

        for i, txt in enumerate(fna): 
                my_members = k_means_labels == i 
                ax.scatter(sound[my_members, 1], sound[my_members,0], s=ps)
        
        #plt.colorbar()
        pl.show()
