# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 17:19:28 2014

@author: Gene
"""

import gc
import numpy as np
import matplotlib.pylab as plt
import matplotlib.pyplot as p
import matplotlib.mlab as m
from copy import deepcopy
from datetime import timedelta

rowname = ['REM sleep', 'Stage 1 NREM sleep', 
             'Stage 2 NREM sleep', 'Stage 3 and 4 NREM sleep'];

CFILES = np.array([['S1_BSL.npz', 'S1_REC.npz'],
                   ['S2_BSL.npz', 'S2_REC.npz'],
                   ['S3_BSL.npz', 'S3_REC.npz'],
                   ['S4_BSL.npz', 'S4_REC.npz']])

# CDIR = '/Users/Troutbum/Development/SleepEEGData/'
CDIR = '/Users/Gene/Development/SleepEEGData/'

def load_eeg(filename, dirname=CDIR):
    """
    load_eeg takes the file name and reads in the data.  It returns an
    array containing EEG data and the sampling rate for
    the data in Hz (samples per second).
    """
    gc.collect()
    data = np.load(dirname + filename)
    return data['DATA'], int(data['srate']), data['stages']
    
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

def plot_example_spectrograms(example,rate):
    """
    This function creates a figure with spectrogram sublpots to of the four
    sleep examples. (Recall row 0 is REM, rows 1-3 are NREM stages 1,
    2 and 3/4)
    """
    plt.figure()
    
    ###YOUR CODE HERE
#    for i in range(0, len(example)):
#        plt.subplot(2,2,i+1)
#        plt.title(rowname[i])    
#        Pxx, freqs, bins, im = plt.specgram(example[i],NFFT=256,Fs=rate)       
#        plt.ylim(0,70)
#        plt.xlabel('Time (Seconds)')
#        plt.ylabel('Frequency (Hz)')
#      
#    return
    
#    for i in range(0, len(example)):
#        plt.subplot(2,2,i+1)
    plt.title(rowname[i])    
    Pxx, freqs, bins, im = plt.specgram(example,NFFT=512,Fs=rate)       
    plt.ylim(0,70)
    plt.xlabel('Time (Seconds)')
    plt.ylabel('Frequency (Hz)')
      
    return    

def plot_example_psds(example,rate):
    """
    This function creates a figure with 4 lines to show the overall psd for 
    the four sleep examples. (Recall row 0 is REM, rows 1-3 are NREM stages 1,
    2 and 3/4)
    """
    plt.figure()

    ##YOUR CODE HERE   
   
    for i in range(0, len(example)):
        Pxx, freqs = m.psd(example[i], NFFT=512, Fs=rate)
        normalizedPxx = Pxx/sum(Pxx)
        plt.plot(freqs, normalizedPxx, label=rowname[i])
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Normalized Power Spectral Density')        
    
        ## Inserted into plotting loop
        ## Possible Classifier - calculate average power-weighted frequency    
        sumPower = 0
        for j in range(0, len(normalizedPxx)):
            sumPower = sumPower + (normalizedPxx[j] * freqs[j])
    
        avgFreq = sumPower/len(freqs)
        print(rowname[i] + " average frequency = " + str(avgFreq))
        ##
        ##    

    plt.xlim(0,20)
    plt.legend(loc=0)
    
    ## Better Classifier - Cummulative Power Distribution
    ## find where cummulative power exceeds threshold %
    threshold = 0.95
    print(' ')
    print('Threshold set to ' + str(threshold*100)+'%')
   
    # iterate over each example data set
    for i in range(0, len(example)):
        Pxx, freqs = m.psd(example[i], NFFT=512, Fs=rate)
        
        # normalize PSD
        normalizedPxx = Pxx/sum(Pxx)
  
        # determine cummulative power distribution 
        sumPxx = 0    
        j = 0        
        while sumPxx <= threshold:
            sumPxx = sumPxx + normalizedPxx[j]
            j = j + 1    
     
        # stop when cummulative power exceeds threshold %
        print(rowname[i]+' - Threshold Met at Frequency = '+str(freqs[j])+' Hz')
                   
    return

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

    # plot frequency response    
    plt.figure()
    Pxx, freqs = p.psd(eeg1,NFFT=512,Fs=srate)  # tighter versus default NFFT=256    
    
    # plot power spectral  density
    plt.figure()
    Pxx, freqs, bins, im = plt.specgram(eeg1,NFFT=256,Fs=srate)

    
    #plot_example_psds(eeg1,srate)    
    

#    plot raw EEG time series and observed stages
#    
#    plt.figure()
#    
#    fig,ax1 = plt.subplots()  #Needed for the multiple y-axes    
#    
#    times = np.arange(0,len(eeg1),1)
#    plt.plot(times,eeg1)
#    #plt.plot(times,stage1)
#    
#    ax2 = ax1.twinx() #Necessary for multiple y-axes       
#    times = np.arange(0,len(stage1)*3, 3) 
#    ax2.plot(times, stage1, drawstyle='steps', color='red')

    #examples, srate = load_examples('example_stages.npz')
    #Plot the psds
    #plot_example_psds(examples,srate)
    #Plot the spectrograms
    #plot_example_spectrograms(examples,srate)
   
   
   
