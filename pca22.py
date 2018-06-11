import scipy
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import fcluster
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist

from pylab import rcParams
import seaborn as sb 
import matplotlib.pyplot as plt

import sklearn
from sklearn.cluster import AgglomerativeClustering
import sklearn.metrics as sm
import sklearn.decomposition.pca as princomp

import scipy.cluster.hierarchy as sc 

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing
import sklearn.datasets # this is to create a new data set for acoustic data
#%matplotlib inline
import matplotlib.pyplot as plt
#import seaborn as sns; sns.set()

"""
Input:  sound = matrix, each row is from a different wav file
        ngroup = number of groups
        labelsn = names of the wav files (abreviated)
        columns = number of colums 
        clusterLabels = correct labels for each row
		clusterLabelsD =  labels dictionary
Output: pca scatter plot colored by truth 
		lables colored by truth
Note: all input files must be the same lengths
"""
def pca22(sound, ngroup, labelsn, clusterLabels, clusterLabelsD): #, clulbb, clulbbb): 

	# puts data in standard normal dist
	Xscale = preprocessing.scale(sound)  #Xscale = sound

	# creats sklearn data set
	pcaDS = sklearn.datasets.base.Bunch(data=Xscale, target=clusterLabels) 
	
	# run pca analysis
	pca = PCA(3)  
	projected = pca.fit_transform(pcaDS.data) #

	# Create plots
	plt.figure(figsize=(25,14)) 
	plt.scatter(projected[:, 0], projected[:, 1], c=pcaDS.target, edgecolor='none', alpha=0.5, cmap=plt.cm.get_cmap('spectral', ngroup))
	plt.xlabel('component 1', fontsize=30)
	plt.ylabel('component 2', fontsize=30)
	plt.show()

	plt.figure(figsize=(25,14)) 
	plt.scatter(projected[:, 1], projected[:, 2], c=pcaDS.target, edgecolor='none', alpha=0.5, cmap=plt.cm.get_cmap('spectral', ngroup))
	plt.xlabel('component 2', fontsize=30)
	plt.ylabel('component 3', fontsize=30)
	plt.show()

	plt.figure(figsize=(25,14)) 
	plt.scatter(projected[:, 0], projected[:, 2], c=pcaDS.target, edgecolor='none', alpha=0.5, cmap=plt.cm.get_cmap('spectral', ngroup))
	plt.xlabel('component 1', fontsize=30)
	plt.ylabel('component 3', fontsize=30)
	plt.show()

	