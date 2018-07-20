import time

import numpy as np
import pylab as pl

from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.datasets.samples_generator import make_blobs
import sklearn.datasets # this is to create a new data set for acoustic data

from scipy.cluster import hierarchy #dendrogram #pick number of clusters
import matplotlib.pyplot as plt #dendrogram

"""
This porgram creates a scatter plot of the first two dimenstions of 
the imputed data matrix.  It then colors each point based on the 
cluster assigned by running k-means clustering algorithum on all the 
dimensions in the imputed data matrix.  

Input:  sound = matrix, each row is from a different wav file
        ncl = ngroup = number of groups
        fna = file names as list
        mlLabels = labels/groups 0,1,2 as array/list 
        mlLabelsD = labels/groups as dictionary
        mlLabelsH = labels/groups as horizontal array/list
        
Output: plot
"""

def kmcAll(sound, ncl, fna, mlLabels, mlLabelsD, mlLabelsH):

        X = sound 
        print 'data:'

        inivar = 'k-means++'
        ninivar = 10
        k_means = KMeans(init=inivar, n_clusters=ncl, n_init=ninivar) 

        t0 = time.time() 
        k_means.fit(X)
        t_batch = time.time() - t0
        k_means_labels = k_means.labels_

        ps = 300
        mlLab = mlLabels.tolist() 
        fig, ax = plt.subplots(figsize=(25,14)) 
        plt.title('{0} = init, {1} = ngroup, {2} = n_init'.format(inivar, ncl, ninivar), fontsize=30) 

        for i, txt in enumerate(fna): 
                my_members = k_means_labels == i 
                ax.scatter(X[my_members, 1], X[my_members,0], s=ps)
        
        pl.show()
