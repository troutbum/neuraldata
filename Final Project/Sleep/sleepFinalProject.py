# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 08:06:48 2014

@author: Troutbum
"""

import gc
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import matplotlib.pyplot as p
import matplotlib.mlab as m
from copy import deepcopy
from datetime import timedelta
from IPython.html.widgets import interactive
from IPython.display import Audio, display
           
channel_name = ['EEG Ch1', 'EEG Ch2', 'EEG Ch8','EEG Ch9',
           'EOG Ch3', 'EOG Ch4',
           'EMG Ch5', 'EMG Ch6', 'EMG Ch7'];            

CFILES = np.array([['S1_BSL.npz', 'S1_REC.npz'],
                   ['S2_BSL.npz', 'S2_REC.npz'],
                   ['S3_BSL.npz', 'S3_REC.npz'],
                   ['S4_BSL.npz', 'S4_REC.npz']])

CDIR = '/Users/Troutbum/Development/SleepEEGData/'
#CDIR = '/Users/Gene/Development/SleepEEGData/'

def load_sleepdata(filename, dirname=CDIR):
    """
    For each data set, there are 3 keys:  
    
        DATA, srate, and stages 
    
    (To load each .npz file, look at the loading code provided 
    in Problem Set 4. Notice that 
    srate needs to be converted to an integer.)
    
    There are 9 channels in DATA: 
        EEG Channels: 1, 2, 8, 9
        EOG Channels: 3, 4
        EMG Channels: 5, 6, 7

    With these 9 channels you can use EOG and EMG
    to identify REM sleep and periods ofwakefulness.

    DATA is a (channel x samples) 2-dimensional array. 
    (So 9 x the number of samples).
    
    "srate" is the sampling rate.
    
    "stages" are the researcher classified stages for 
    each 30s epoch
         
        0 - Awake
        1 - NREM Stage 1
        2 - NREM Stage 2
        3 - NREM Stage 3 
        4 - NREM Stage 4 
        5 - REM Sleep
        6 - Movement Time    
        7 - Unscored
    """
    gc.collect()
    data = np.load(dirname + filename)
    return data['DATA'], int(data['srate']), data['stages']

def convert_to_df(data, stages):
    # expand stage observations from         
    xstage = np.zeros(len(data))        
    index = 0
    for epoch in range(0, len(stages)):
        for j in range(0,30):            
            xstage[index] = stages[epoch]
            index = index + 1           
    df = pd.DataFrame({'edata' : data, 'stage' : xstage})     
    return df

def plot_spectrograms(data, rate, subject, condition):
    """
    Creates spectrogram subplots for all 9 channels
    """
    fig = plt.figure()   
   # common title
    fname = 'Spectrogram - '+'Subject #'+subject+' '+condition+' Dataset'
    fig.suptitle(fname, fontsize=14, fontweight='bold')            
    # common ylabel
    fig.text(0.06, 0.5, 'ylabel', 
             ha='center', va='center', rotation='vertical',
             fontsize=14, fontweight='bold')
    # use this to stack EEG, EOG, EMG on top of each other         
    sub_order = [1,4,7,10,2,5,3,6,9]          
    
    for ch in range(0, len(data)):
        plt.subplot(4, 3, sub_order[ch])
        plt.subplots_adjust(hspace=.6)  # adds space between subplots
        plt.title(channel_name[ch])    
        Pxx, freqs, bins, im = plt.specgram(data[ch],NFFT=512,Fs=rate)       
        plt.ylim(0,70)
        plt.xlabel('Time (Seconds)')
        plt.ylabel('Frequency (Hz)')
    
    #fig.savefig(fname+'.pdf', format='pdf')  buggy resolution problem
    return
    
def plotall_hypnograms(dataset, stages, rate, subject, condition):
    """
    Creates a hypnogram subplot for all 9 channels
    This function takes the eeg, the stages and sampling rate and draws a 
    hypnogram over the spectrogram of the data.
    """
    for ch in range(0, len(dataset)):
        plot_hypnogram(dataset[ch], ch, stages, srate, subject, condition)
 
    return    
    
def plot_hypnogram(eeg, channel, stages, srate, subject, condition):
    """
    This function takes the eeg, the stages and sampling rate and draws a 
    hypnogram over the spectrogram of the data.
    """ 
    fig,ax1 = plt.subplots()  #Needed for the multiple y-axes 
    #Use the specgram function to draw the spectrogram as usual    
    Pxx, freqs, bins, im = plt.specgram(eeg,NFFT=512,Fs=srate)            
    #Label your x and y axes and set the y limits for the spectrogram
    plt.ylim(0,30)
    plt.xlabel('Time (Seconds)')
    plt.ylabel('Frequency (Hz)')  
    ax2 = ax1.twinx() #Necessary for multiple y-axes  
    #Use ax2.plot to draw the hypnogram.  Be sure your x values are in seconds
    #HINT: Use drawstyle='steps' to allow step functions in your plot 
    times = np.arange(0,len(stages)*30, 30)   
    ax2.plot(times, stages, drawstyle='steps', color='blue')   
    #Label your right y-axis and change the text color to match your plot
    ax2.set_ylabel('NREM Stage',color='b')
    #Set the limits for the y-axis 
    plt.ylim(0.0,7.0)
    #Only display the possible values for the stages
    ax2.set_yticks(np.arange(1,7))   
    #Change the left axis tick color to match your plot
    for t1 in ax2.get_yticklabels():
        t1.set_color('b')    
    #Title your plot  
    fname = ('Hypnogram - '+ 'Subject #'
        +subject+' '+condition+' - '+str(channel_name[channel]))
    plt.title(fname, fontsize=14, fontweight='bold')
#    plt.title('Hypnogram - '+ 'Subject #'+subject+' '+condition+' - '
#            +str(channel_name[channel]), 
#            fontsize=14, fontweight='bold')        
    fig.savefig(fname+'.png', format='png')        
    return

def plot_psds(data, rate, subject, condition):
    """
    Plots the frequency response for all 9 channels
    using the entire recording    
    """
    fig = plt.figure()   
   # common title
    fig.suptitle('Frequency Response for Complete Recording - '+ 
            'Subject #'+subject+' '+condition+' Dataset', 
            fontsize=14, fontweight='bold')            
    # common ylabel
    fig.text(0.06, 0.5, 'Normalized Power Spectral Density', 
             ha='center', va='center', rotation='vertical',
             fontsize=14, fontweight='bold')
    # common xlabel
    fig.text(0.5, 0.05,'Frequency (Hz)',
             ha='center', va='center',fontsize=14, fontweight='bold')


    # use this to stack EEG, EOG, EMG on top of each other
    sub_order = [1,4,7,10,2,5,3,6,9]    

    for ch in range(0, len(data)):
        #plt.subplot(4, 3, sub_order[ch])  # 4 x 3 layout
        plt.subplot(9, 1, ch + 1)  # vertical 9 x 1 layout
        plt.subplots_adjust(hspace=.6)  # adds space between subplots
        
        Pxx, freqs = m.psd(data[ch], NFFT=512, Fs=rate)
        normalizedPxx = Pxx/sum(Pxx)
        plt.plot(freqs, normalizedPxx, label=channel_name[ch])
        
        plt.title(channel_name[ch]) 
        #plt.xlabel('Frequency (Hz)')
        #plt.ylabel('Normalized Power Spectral Density')        
      
        ## Inserted into plotting loop
        ## Possible Classifier - calculate average power-weighted frequency    
        sumPower = 0
        for j in range(0, len(normalizedPxx)):
            sumPower = sumPower + (normalizedPxx[j] * freqs[j])
    
        avgFreq = sumPower/len(freqs)
        print(channel_name[ch] + " average frequency = " + str(avgFreq))
    return     
    

def plot_hist_stages_base_vs_recovery(base_stages, rec_stages, subject):
    """
    histogram comparing sleep stage distribution 
    of baseline versus recovery subject states
    """  

    plt.figure()
    p.hist( [base_stages, rec_stages], histtype='bar', normed=True,
           label=['Baseline', 'Recovery'], color=['black','red'])
    plt.title('Proportion of Time Spent in Sleep Stages (Test Subject '
            +str(subject)+')')
    plt.xlabel('Observed Sleep Stage')
    plt.ylabel('Normalized Time')
    plt.legend()
    mString1 ='0 - Awake\n1 - NREM Stage 1\n2 - NREM Stage 2'
    mString2 = '\n3 - NREM Stage 3\n4 - NREM Stage 4\n5 - REM Sleep'
    mString3 = '\n6 - Movement Time\n7 - Unscored'
    mString = mString1 + mString2 + mString3
    plt.annotate(mString, xy=(0.75, 0.45), xycoords='axes fraction')
    return
     
def plot_stage_vs_time(stages_sub1bsl, stages_sub1rec, 
                       stages_sub2bsl, stages_sub2rec):
    """
    time series plot of sleep stage
    baseline versus recovery subject states
    """  
                      
    fig = plt.figure()   
    # common title
    fig.suptitle('Observed Sleep Stages vs Time', fontsize=14, 
                 fontweight='bold')       
    # common xlabel
    fig.text(0.5, 0.05,'Epoch (30 second intervals)',
             ha='center', va='center',fontsize=14, fontweight='bold')
    # common ylabel
    fig.text(0.06, 0.5, 'Sleep Stage', 
             ha='center', va='center', rotation='vertical',
             fontsize=14, fontweight='bold')                      
    
    ax4 = plt.subplot(414) # creates second axis
    ax4.plot(stages_sub2rec, 'red')
    ax4.set_xlim([0, len(stages_sub2rec)])
    
    ax1 = plt.subplot(411, sharex=ax4) # creates first axis
    ax1.plot(stages_sub1bsl, color='black')
    
    ax2 = plt.subplot(412, sharex=ax4) # creates second axis
    ax2.plot(stages_sub1rec, 'red')
 
    ax3 = plt.subplot(413, sharex=ax4) # creates first axis
    ax3.plot(stages_sub2bsl, color='black')

    ax1.set_title('Subject 1 Baseline')
    ax2.set_title('Subject 1 Recovery')    
    ax3.set_title('Subject 2 Baseline')
    ax4.set_title('Subject 2 Recovery')
    return    
    
def verify_datasets():
    """
    checks numbers of stages in file vs calculated epochs
    """
    channel = 0 # assume all 9 channels have same number of samples
    for subject in range(0,4) : 
        for study in range(0,2):
            data, srate, stages = load_sleepdata(CFILES[subject][study])
            epoch_length = srate * 30   # each epoch is 30 seconds
            epochs = len(data[channel])/epoch_length
            print 'Subject '+str(subject) +' Study '+str(study)
            print 'Stages in file = ' + str(len(stages)) 
            print 'Calculated number of epochs = ' + str(epochs) 
            print '  '
    return        
    """"
    Discovered inconsistencies in datasets for Subject 3 & 4
    -->> number of stages in files does not match length of recording
    Subject 1 & 2 datasets are OK
    
    'S3_BSL.npz', 
    Stages in file = 2219
    Calculated number of epochs = 1688
    
    'S3_REC.npz'
    Stages in file = 1263
    Calculated number of epochs = 1268

    'S4_BSL.npz'
    Stages in file = 1263
    Calculated number of epochs = 1268
 
    'S4_REC.npz'
    Stages in file = 1715
    Calculated number of epochs = 2218
    """   
    
##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
    #YOUR CODE HERE
    
    plt.close('all') #Closes old plots.   
    #    verify_datasets()  # checks # of stages vs calculated epochs
    
    # load datasets for Subject 1 & 2 (baseline & recovery)
    data_sub1bsl, srate, stages_sub1bsl = load_sleepdata(CFILES[0][0])
    data_sub1rec, srate, stages_sub1rec = load_sleepdata(CFILES[0][1]) 
    data_sub2bsl, srate, stages_sub2bsl = load_sleepdata(CFILES[1][0])
    data_sub2rec, srate, stages_sub2rec = load_sleepdata(CFILES[1][1]) 
 
    # plot histogram of sleep stage states
    """
    plot_hist_stages_base_vs_recovery(stages_sub1bsl, stages_sub1rec, 1)
    plot_hist_stages_base_vs_recovery(stages_sub2bsl, stages_sub2rec, 2)
    """    
    
    # plot time series of sleep stage states
    """
    plot_stage_vs_time(stages_sub1bsl, stages_sub1rec, 
                       stages_sub2bsl, stages_sub2rec)
    """                   
  
    # plot frequency response of complete datasets  
    """    
    plot_psds(data_sub1bsl, srate, '1', 'Baseline')
    plot_psds(data_sub1rec, srate, '1', 'Recovery')
    plot_psds(data_sub2bsl, srate, '2', 'Baseline')
    plot_psds(data_sub2rec, srate, '2', 'Recovery')
    """
  
    # plot spectrograms of datasets
    """
    plot_spectrograms(data_sub1bsl, srate, '1', 'Baseline')  
    """    
    
    # plot one hypnogram (spectrogram and sleep stage)
    """
    plot_hypnogram(data_sub1bsl[0], 0, stages_sub1bsl, srate, '1', 'Baseline' )
    """
    
    # plot all hypnograms for all 9 channels in dataset 
    """      
    plotall_hypnograms(data_sub1bsl, stages_sub1bsl, srate, '1', 'Baseline')
    plotall_hypnograms(data_sub1rec, stages_sub1rec, srate, '1', 'Recovery')
    plotall_hypnograms(data_sub2bsl, stages_sub2bsl, srate, '2', 'Baseline')
    plotall_hypnograms(data_sub2rec, stages_sub2rec, srate, '2', 'Recovery')
     """
#    v = interactive(beat_freq, f1=(200.0,300.0), f2=(200.0,300.0))
#    display(v)
  
    # df = pd.DataFrame({'edata' : data_sub1bsl[0], 'stage' : stages_sub1bsl})
      
    
    df = convert_to_df(data_sub1bsl[0], stages_sub1bsl)
   
    """   
    # slice dataframe by row (i.e. sleep stage = 5)
    df2 = df.ix[df.stage==5]
    # slice datframe by column (just the edata)
    df3 = df2['edata']
    """
    
    # slice by row and column at the same time    
    df4 = df.ix[df.stage==5]['edata']

    plt.figure()
    Pxx, freqs = m.psd(df4, NFFT=512, Fs=srate)
    normalizedPxx = Pxx/sum(Pxx)
    plt.plot(freqs, normalizedPxx)


