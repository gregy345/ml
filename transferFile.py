import numpy as np
import os # for opeining files in loop #change working diectory, count files in directory
import os.path
import shutil
"""
Input:  datafile = the name of the original file to be moved
         location = the original location of the file
Output: datafile = identical file in new location
               also deletes original file
"""
def transfer(datafile, location):
        print "  "
        print "starting transfer of {0}".format(datafile)

        #basepath = '/media/TerraSAR-X/Acoustics/data/DataCluster'
        folderPath = 'C:/Users/Greg/Documents/AcWrFi/StAc/Main/ml/TextFile'
        #folderPath = '/media/TerraSAR-X/Acoustics/data/TextFile' # destination

        # copies the cropped file to a new folder
        shutil.copy(os.path.join(location, datafile), folderPath)

        # removes the file that has just been coppied
        os.remove(os.path.join(location, datafile))

        print "the file has been transfered "