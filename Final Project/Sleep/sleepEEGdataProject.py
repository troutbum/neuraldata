# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 17:19:28 2014

@author: Gene
"""

from __future__ import division
import numpy as np
import matplotlib.pylab as plt
import matplotlib.mlab as m

rowname = ['REM sleep', 'Stage 1 NREM sleep', 
             'Stage 2 NREM sleep', 'Stage 3 and 4 NREM sleep'];

def load_sleepdata(filename):
    """
    load_examples takes the file name and reads in the data.  It returns an
    array containing the 4 examples of the 4 stages in its rows (row 0 = REM;
    1 = stage 1 NREM; 2 = stage 2; 3 = stage 3 and 4) and the sampling rate for
    the data in Hz (samples per second).
    
    For each data set, there are 3 keys:  
    
    DATA, srate, and stages 
    
    (To load each .npz file, look at the loading code provided 
    in Problem Set 4. Notice that 
    srate needs to be converted to an integer.)
    """
    data = np.load(filename)
    return data['DATA'], int(data['srate']), data['stages']
    
    
##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
    #YOUR CODE HERE
    
    plt.close('all') #Closes old plots.    
    
    ##PART 1
    #Load the example data
    DATA, srate, stages = load_sleepdata('S2_BSL.npz')

    #examples, srate = load_examples('example_stages.npz')
    #Plot the psds
    #plot_example_psds(examples,srate)
    #Plot the spectrograms
    #plot_example_spectrograms(examples,srate)
   
