import numpy as np

"""
Create list of groups 
Input:  ngroup = number of groups to color
        nbr = number of files in folder
        fillist = np array of labels
Output: mlLabels = np array of labels

"""

def labels(ngroup, nbr, fillist):

    mlLabels = np.zeros((nbr, 1), dtype=int)

    # clustering by pipes    
    if ngroup == 3:
        for t in range (0, nbr):  
                if 'PC' in fillist[t]: 
                    mlLabels[t] =  0 #1 #0
                elif 'PL' in fillist[t]: 
                    mlLabels[t] =  2 #2 #1
                elif 'PS' in fillist[t]: 
                    mlLabels[t] =  1 #0 #2

    # clustering by mic    
    elif ngroup == 6:
        for t in range (0, nbr):  
                if 'Mi01' in fillist[t]: 
                    mlLabels[t] =  0
                elif 'Mi02' in fillist[t]: 
                    mlLabels[t] =  1
                elif 'Mi03' in fillist[t]: 
                    mlLabels[t] =  2
                elif 'Mi04' in fillist[t]: 
                    mlLabels[t] =  3
                elif 'Mi05' in fillist[t]: 
                    mlLabels[t] =  4
                elif 'Mi06' in fillist[t]: 
                    mlLabels[t] =  5
    else:
        print 'need labels for option ngroup = {0}'.format(ngroup)

    return mlLabels