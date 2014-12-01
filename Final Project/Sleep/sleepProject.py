# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 17:19:28 2014

@author: Gene
"""

import gc
import numpy as np
import matplotlib.pylab as plt
from copy import deepcopy
from datetime import timedelta

CFILES = np.array([['S1_BSL.npz', 'S1_REC.npz'],
                   ['S2_BSL.npz', 'S2_REC.npz'],
                   ['S3_BSL.npz', 'S3_REC.npz'],
                   ['S4_BSL.npz', 'S4_REC.npz']])

CDIR = '/Users/Troutbum/Development/SleepEEGData/'

def load_eeg(filename, dirname=CDIR):
    """
    load_eeg takes the file name and reads in the data.  It returns an
    array containing EEG data and the sampling rate for
    the data in Hz (samples per second).
    """
    gc.collect()
    data = np.load(dirname + filename)
    return data['DATA'], data['srate'], data['stages']
    
#def pull_lead1_epoch(subject, study, epoch_number):
#    """
#    just one epoch of lead 1 data
#    """
#    data, srate, _ = load_eeg(CFILES[subject][study])
#    elength = srate * 30.0
#    startpos = epoch_number * elength
#    endpos = startpos + elength
#    eegdata = deepcopy(data[0][startpos:endpos])
#    return eegdata, srate    
    
def pull_stage(filename):
    """
    just stage data
    """
    dat = load_eeg(filename)
    return dat[2]

def pull_lead1_epoch(subject, study, epoch_number):
    """
    just one epoch of lead 1 data
    """
    data, srate, stages = load_eeg(CFILES[subject][study])
    elength = srate * 30.0
    startpos = epoch_number * elength
    endpos = startpos + elength
    eegdata = deepcopy(data[0][startpos:endpos])
    return eegdata, srate, stages


#from __future__ import division
#import numpy as np
#import matplotlib.pylab as plt
#import matplotlib.mlab as m
#
#rowname = ['REM sleep', 'Stage 1 NREM sleep', 
#             'Stage 2 NREM sleep', 'Stage 3 and 4 NREM sleep'];
#
#def load_sleepdata(filename):
#    """
#    load_examples takes the file name and reads in the data.  It returns an
#    array containing the 4 examples of the 4 stages in its rows (row 0 = REM;
#    1 = stage 1 NREM; 2 = stage 2; 3 = stage 3 and 4) and the sampling rate for
#    the data in Hz (samples per second).
#    
#    For each data set, there are 3 keys:  
#    
#    DATA, srate, and stages 
#    
#    (To load each .npz file, look at the loading code provided 
#    in Problem Set 4. Notice that 
#    srate needs to be converted to an integer.)
#    """
#    data = np.load(filename)
#    return data['DATA'], int(data['srate']), data['stages']
    
    
##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
    
#    plt.close('all') #Closes old plots.    
    
    #Load the example data
    eeg1, srate, stage1 = pull_lead1_epoch(0, 0, 5)
    plt.figure()
    
    fig,ax1 = plt.subplots()  #Needed for the multiple y-axes    
    
    times = np.arange(0,len(eeg1),1)
    plt.plot(times,eeg1)
    #plt.plot(times,stage1)
    
    ax2 = ax1.twinx() #Necessary for multiple y-axes       
    times = np.arange(0,len(stage1)*3, 3) 
    ax2.plot(times, stage1, drawstyle='steps', color='red')

    #examples, srate = load_examples('example_stages.npz')
    #Plot the psds
    #plot_example_psds(examples,srate)
    #Plot the spectrograms
    #plot_example_spectrograms(examples,srate)
   
   
   
