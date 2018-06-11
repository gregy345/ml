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

"""
Input:  sound = matrix, each row is from a different wav file
        ncls = number of groups
        labelsn = names of the wav files (abreviated)
        columns = number of colums 
        clusterLabels = correct group for each row
		clusterLabelsD = labels dictionary
Output: dendrogram branches colored by group
		lables colored by truth
		% correct
Note: all input files must be the same lengths
"""
def ddg2(sound, ncls, labelsn, clusterLabels, clusterLabelsD): #, clulbb, clulbbb): 
		
	dimentions = sound.shape

	row = dimentions[0] #996
	col = dimentions[1] #308
	dim = row*col

	print 'ddg2  dimentions, col, dim'
	print dimentions
	print col
	print dim

	# creates the data frame
	colum = list(range(1, (col+1)))  
	df = pd.DataFrame(data=sound, index=labelsn, columns=colum)  
	#print 'df'
	#print df

	Z = linkage(df, 'ward')	 

	# Create Plot
	np.set_printoptions(precision=4) 
	plt.figure(figsize=(25,14)) 	 

	# single decimate 600 to cluster by pipes and 110/120 cluster by microphones
	#dendrogram(Z, labels=df.index, color_threshold=600, leaf_rotation=90., orientation="top", leaf_font_size=15., show_contracted=True)
	dendrogram(Z, labels=df.index, color_threshold=110, leaf_rotation=90., orientation="top", leaf_font_size=15., show_contracted=True)
	# double decimate 400 to cluster by pipes and 80 cluster by microphones
	#dendrogram(Z, labels=df.index, color_threshold=400, leaf_rotation=90., orientation="top", leaf_font_size=15., show_contracted=True)
	#dendrogram(Z, labels=df.index, color_threshold=80, leaf_rotation=90., orientation="top", leaf_font_size=15., show_contracted=True)
	
	my_palette = plt.cm.get_cmap("jet", ncls) 
	ax = plt.gca()  
	xlbls = ax.get_xticklabels() 
	
	# set color to label based on labels dictionary
	for lbl in xlbls:
		labeltxt = lbl.get_text()
		labelcol=clusterLabelsD[labeltxt] #
		lbl.set_color(my_palette(labelcol))	
	
	plt.show()

	# selects algorithum
	Hclustering = AgglomerativeClustering(n_clusters = ncls, affinity='euclidean',linkage='ward')
	
	# applys the specified algorithum to the data
	Hclustering.fit(df)
	#print 'labels'
	#print Hclustering.labels_
	#print clusterLabels

	score = sm.accuracy_score(clusterLabels, Hclustering.labels_) #this line scores the model
	print "the score is: {0}".format(score)



