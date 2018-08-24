import numpy as np
import pylab as pl


from sklearn.cluster import KMeans
import sklearn.datasets # to create a new data set 
from sklearn.decomposition import PCA
from sklearn import preprocessing

import matplotlib.pyplot as plt 

"""
This porgram runs principal components analysis on the imputed data matrix
for the purpose of dimension reduction.  The program then runs the K-means
algorithum on the reduced data.  A scatter plot of the first two principal
components is created and colors each point based on the cluster assigned 
by the K-means algorithum.


Input:  sound = matrix, each row is from a different wav file
        ncl = ngroup = number of groups
        fna = file names as list
        mlLabels = groups 0,1,2 as list 
        mlLabelsD = labels/groups as dictionary
Output: plot
"""
def kmcpca(sound, ncl, fna, mlLabels, mlLabelsD, mlLabelsH):
        
        # puts data in standard normal dist
        Xscale = preprocessing.scale(sound)  #Xscale = sound
        # creats sklearn data set
        pcaDS = sklearn.datasets.base.Bunch(data=Xscale, target=mlLabels) 
        # run pca analysis
        pca = PCA(2) 
        X = pca.fit_transform(pcaDS.data) 
        
        ##############################################################################
        
        print 'data:'
        print X #print projected #
        print sound

        ##############################################################################
        # Compute clustering with Means

        inivar = 'k-means++'
        ninivar = 10
        k_means = KMeans(init=inivar, n_clusters=ncl, n_init=ninivar) 
        k_means.fit(X) # applies the algorithum to the reduced data set
        k_means_labels = k_means.labels_
        print "k_means_labels"
        print k_means_labels
        #print k_means_labels.tolist()


        ms = 40
        ps = 300 #80
        plt.figure(figsize=(25,14))
        plt.title('{0} = init, {1} = n_clusters, {2} = n_init'.format(inivar, ncl, ninivar), fontsize=30)
        plt.rc('xtick', labelsize=ms) 
        plt.rc('ytick', labelsize=ms)   
        for i, txt in enumerate(fna): 
                my_members = k_means_labels == i 
                plt.scatter(X[my_members, 0], X[my_members,1], s=ps)
                
        plt.xlabel('component 1', fontsize=ms)
        plt.ylabel('component 2', fontsize=ms)
        
        pl.show()
