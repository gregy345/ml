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
This porgram creates a tree plot (dendrogram) based on the 
heirarchal clustering algorithum from the imputed data matrix.  It then
attaches the file names as leaves and colors then by label.  The branches 
are colored based on the distance (color threshold) for the purposes of 
readability.

Input:  sound = matrix, each row is from a different wav file
        ncls = number of groups
        labelsn = names of the wav files (abreviated)
        columns = number of colums 
        mlLabels = correct group for each row
		mlLabelsD = labels dictionary
Output: dendrogram branches colored by group
		lables colored by truth
		% correct
Note: all input files must be the same lengths
"""
def ddg2(sound, ncls, labelsn, mlLabels, mlLabelsD):  
		
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

	lnx = 'ward' #lnx = 'complete' #lnx = 'average' 
	afx = 'euclidean' #afx = 'l1' #afx = 'l2' #afx = 'manhattan' #afx = 'cosine' #afx = 'precomputed'

	Z = linkage(df, lnx)  

	# Create Plot 
	# ward euclidean pipes use 250 # ward euclidean mic use 58
	cth = 250 
	np.set_printoptions(precision=4) 
	plt.figure(figsize=(25,14)) ##		 
	plt.title('{0} linkage, {1} affinity, {2} ngroup, {3} distance'.format(lnx, afx, ncls, cth), fontsize=30)
	dendrogram(Z, labels=df.index, color_threshold=cth, leaf_rotation=90., orientation="top", leaf_font_size=15., show_contracted=True)

	my_palette = plt.cm.get_cmap("jet", ncls) 
	ax = plt.gca()  
	xlbls = ax.get_xticklabels() 
	
	# set color to label based on labels dictionary
	for lbl in xlbls:
		labeltxt = lbl.get_text()
		labelcol=mlLabelsD[labeltxt] #
		lbl.set_color(my_palette(labelcol))	
	
	plt.show()

	# selects algorithum
	Hclustering = AgglomerativeClustering(n_clusters = ncls, affinity = afx ,linkage = lnx)

	# applys the specified algorithum to the data
	Hclustering.fit(df)

	score = sm.accuracy_score(mlLabels, Hclustering.labels_) #this line scores the model
	print "the score is: {0}".format(score)



