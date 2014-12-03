# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 08:06:48 2014

@author: Troutbum
"""

import gc
import numpy as np
import matplotlib.pylab as plt
import matplotlib.pyplot as p
import matplotlib.mlab as m
from copy import deepcopy
from datetime import timedelta
from IPython.html.widgets import interactive
from IPython.display import Audio, display
           
rowname = ['EEG Ch1', 'EEG Ch2', 'EEG Ch8','EEG Ch9',
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

def plot_hist_stages_base_vs_recovery(base_stages, rec_stages, subject):
    """
    histogram comparing sleep stage distribution 
    of baseline versus recovery subject states
    """  
    plt.figure()
    p.hist( [base_stages, rec_stages], histtype='bar', normed=True,
           label=['Baseline', 'Recovery'], color=['black','red'])
    plt.title('Time Spent in Sleep Stages (Test Subject '+str(subject)+')')
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
    plt.figure()
#    ax = plt.subplot(111)    # The big subplot
    
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
    
#    ax.set_ylabel('Observed Sleep Stage')  # common ylabel
#    ax.set_xlabel('Epoch Number')

    # Set common labels
    plt.text(0.5, 0.5, 'common xlabel', ha='center', va='center')
    plt.text(0.5, 0.5, 'common ylabel', ha='center', va='center', rotation='vertical')
    
    plt.show()
    
     
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
    
    data_sub1bsl, srate, stages_sub1bsl = load_sleepdata(CFILES[0][0])
    data_sub1rec, srate, stages_sub1rec = load_sleepdata(CFILES[0][1]) 
    data_sub2bsl, srate, stages_sub2bsl = load_sleepdata(CFILES[1][0])
    data_sub2rec, srate, stages_sub2rec = load_sleepdata(CFILES[1][1]) 
 
    plot_hist_stages_base_vs_recovery(stages_sub1bsl, stages_sub1rec, 1)
    plot_hist_stages_base_vs_recovery(stages_sub2bsl, stages_sub2rec, 2)
    plot_stage_vs_time(stages_sub1bsl, stages_sub1rec, 
                       stages_sub2bsl, stages_sub2rec)
  
#    v = interactive(beat_freq, f1=(200.0,300.0), f2=(200.0,300.0))
#    display(v)

    
#    ##PART 1
#    #Load the example data
#    examples, srate = load_examples('example_stages.npz')
#    #Plot the psds
#    plot_example_psds(examples,srate)
#    #Plot the spectrograms
#    plot_example_spectrograms(examples,srate)
#   
#   #Test the examples   
#    for j in range(0, len(examples)):
#        print('')
#        print('Testing Example : '+rowname[j])
#        print('')
#        for i in range(0, 10):
#            start = i * 3840
#            end = ((i + 1) * 3840)
#            epoch = examples[j][start:end]
#            print('Predicted NREM Stage = ' + str(classify_epoch(epoch,srate)))
#   
#    # supplied tester
#    test_examples(examples, srate)
#    
#    #Load the practice data
#    eeg, srate = load_eeg('practice_eeg.npz')   
#    #Load the practice answers
#    stages = load_stages('practice_answers.npz')
#    
#    #Classify the practice data
#    classifiedEEG = classify_eeg(eeg,srate)  
#    
#    #Check your performance
#    actualEEG = stages
#    classifier_tester(classifiedEEG, actualEEG)
# 
#    #Generate the hypnogram plots
#    #plot_hypnogram(eeg, stages, srate)
#    plot_hypnogram(eeg, classifiedEEG, srate)
#    
#    #Run classifier on another data set "test_eeg" and plot
#    print('')
#    print('Loading "test_eeg" data set')
#    eeg2, srate2 = load_eeg('test_eeg.npz')   
#    print('Analyzing "test_eeg" data set')
#    classifiedEEG2 = classify_eeg(eeg2,srate2)
#    print('Plotting "test_eeg" data set')
#    plot_hypnogram(eeg2, classifiedEEG2, srate2)
#    plt.title('Hypnogram - Test Data')  # override title    