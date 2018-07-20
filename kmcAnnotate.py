#print __doc__
import time

import numpy as np
import pylab as pl

from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.datasets.samples_generator import make_blobs
import sklearn.datasets # this is to create a new data set for acoustic data

#docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy
from scipy.cluster import hierarchy #dendrogram #pick number of clusters
import matplotlib.pyplot as plt #dendrogram

"""
This porgram creates a scatter plot of the first two dimenstions of 
the imputed data matrix.  It then attaches a label to each point.  This 
was done for the purposes of checking the accuracy of the colors assigned 
by k-means clustering.  

Input:  sound = matrix, each row is from a different wav file
        ncl = ngroup = number of groups
        fna = file names as list
        mlLabels = labels/groups 0,1,2 as array/list 
        mlLabelsD = labels/groups as dictionary
        mlLabelsH = labels/groups as horizontal array/list
        
Output: plot
"""

def kmcAnnotate(sound, ncl, fna, mlLabels, mlLabelsD, mlLabelsH):

        X = sound 
        print "labels"
        print mlLabelsH.tolist() 

        y = X[:,0]
        z = X[:,1]
        n = mlLabelsH.tolist() 
        
        ps = 300
        fig, ax = plt.subplots(figsize=(25,14))  
        ax.scatter(z, y, s=ps)
        for i, txt in enumerate(n):
            ax.annotate(txt, (z[i],y[i]), fontsize=24) 

        pl.show()
