# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 08:06:48 2014

@author: Troutbum
"""

import sleepModule as s
import gc
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from IPython.html.widgets import interactive
from IPython.display import Audio, display

# directory location of data files
CDIR = '/Users/Troutbum/Development/SleepEEGData/'
#CDIR = '/Users/Gene/Development/SleepEEGData/'

CFILES = np.array([['S1_BSL.npz', 'S1_REC.npz'],
                   ['S2_BSL.npz', 'S2_REC.npz'],
                   ['S3_BSL.npz', 'S3_REC.npz'],
                   ['S4_BSL.npz', 'S4_REC.npz']])

# labels
subject_name = ['1', '2']
condition_name = ['Baseline', 'Recovery']          
channel_name = ['EEG Ch1', 'EEG Ch2', 'EEG Ch8','EEG Ch9',
                'EOG Ch3', 'EOG Ch4',
                'EMG Ch5', 'EMG Ch6', 'EMG Ch7'];            
stage_name = ['Awake', 'NREM Stage 1', 'NREM Stage 2', 'NREM Stage 3',
              'NREM Stage 4', 'REM Sleep', 'Movement Time', 'Unscored']           
# shorthands
BASELINE = 0
BSL = 'Baseline'
RECOVERY = 1
REC = 'Recovery'
SUBJECT1 = 0
SUB1 = 'Subject1'
SUBJECT2 = 1
SUB2 = 'Subject2'

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

def sort_by_stage(data, stages):
    """
    Sorts time series electrical data measurements (EEG, EOG, EMG)
    by observed sleep stage (0 - 7)
    """
    # expand stage observations from         
    xstage = np.zeros(len(data))        
    index = 0
    for epoch in range(0, len(stages)):
        for j in range(0,30):            
            xstage[index] = stages[epoch]
            index = index + 1   
    # join with df        
    df = pd.DataFrame({'edata' : data, 'stage' : xstage}) 

    # create list
    sdata= []
    for i in range(0,6):
        sdata.append(df.ix[df.stage==i]['edata'])     
    """    
    Pandas dataframe slicing techniques:
    df2 = df.ix[df.stage==5]           # slice df by row (sleep stage= 5)
    df3 = df2['edata']                 # slice df by column (just the edata)
    df4 = df.ix[df.stage==5]['edata']  # slice by row and column  
    """
    return sdata

    
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

def load_data():
    """
    Creates a multi-dimension list for the original
    time series datasets (4 sets for 2 subjects, 2 conditions)
    
    usage:  data[subject][condition][channel][stage]
    
    then sort by observed sleep stage:
    
            sdata[subject][condition][channel][stage]
    """     
    
    # load datasets for Subject 1 & 2 (baseline & recovery)    
    data_sub1bsl, srate, stages_sub1bsl = load_sleepdata(CFILES[0][0])
    data_sub1rec, srate, stages_sub1rec = load_sleepdata(CFILES[0][1]) 
    data_sub2bsl, srate, stages_sub2bsl = load_sleepdata(CFILES[1][0])
    data_sub2rec, srate, stages_sub2rec = load_sleepdata(CFILES[1][1]) 
 
    # Create lists of lists 
    # for time series measurements: EEG, EOG, EMG  
    #
    # data[subject][condition][channel][stage]  
    # 
    data_sub1 = []  # list by condition
    data_sub1.append(data_sub1bsl) 
    data_sub1.append(data_sub1rec)

    data_sub2 = []  # list by condition
    data_sub2.append(data_sub2bsl) 
    data_sub2.append(data_sub2rec)   

    data = []  # list by subject
    data.append(data_sub1)
    data.append(data_sub2)
    
    # now organize the Observed Sleep Stages
    #
    # stages[subject][condition][channel][stage]  
    # 
    stages_sub1 = []  # list by condition
    stages_sub1.append(stages_sub1bsl) 
    stages_sub1.append(stages_sub1rec)

    stages_sub2 = []  # list by condition
    stages_sub2.append(stages_sub2bsl) 
    stages_sub2.append(stages_sub2rec)   

    stages = []  # list by subject
    stages.append(stages_sub1)
    stages.append(stages_sub2)

    # now sort using the observed sleep stage
    # using sort_by_stage()
    #
    sdata_sub1bsl = []  # list by stage
    sdata_sub1rec = []
    sdata_sub2bsl = []
    sdata_sub2rec = []

    # list by channel (method call returns list by stage)
    for channel in range(0,9):
        sdata_sub1bsl.append(sort_by_stage(data_sub1bsl[channel],
                                      stages_sub1rec))
        sdata_sub1rec.append(sort_by_stage(data_sub1rec[channel], 
                                      stages_sub1rec))
        sdata_sub2bsl.append(sort_by_stage(data_sub2bsl[channel], 
                                      stages_sub1rec))
        sdata_sub2rec.append(sort_by_stage(data_sub2rec[channel], 
                                      stages_sub1rec))
      
    # Create lists of lists
    #  
    # sdata[subject][condition][channel][stage] 
                            
    sdata_sub1 = [] # list by condition
    sdata_sub1.append(sdata_sub1bsl) 
    sdata_sub1.append(sdata_sub1rec)

    sdata_sub2 = []  # list by condition
    sdata_sub2.append(sdata_sub2bsl) 
    sdata_sub2.append(sdata_sub2rec)   

    sdata = []  # list by subject
    sdata.append(sdata_sub1)
    sdata.append(sdata_sub2)
    
    return data, sdata, stages, srate

    
##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
    
    plt.close('all') #Closes old plots.      
    data, sdata, stages, srate = load_data()  
   
    # checks number of observed stages vs calculated epochs
    #    verify_datasets()  
   
    # plot time series of sleep stage states
    """
    s.plot_stage_vs_time(stages[SUBJECT1][BASELINE], stages[SUBJECT1][RECOVERY], 
                   stages[SUBJECT2][BASELINE], stages[SUBJECT2][RECOVERY])    
    """
    
    # plot histogram of sleep stage states 
    """
    s.plot_hist_stages_base_vs_recovery(stages[SUBJECT1][BASELINE], 
                                      stages[SUBJECT1][RECOVERY], 
                                      subject_name[SUBJECT1])
    s.plot_hist_stages_base_vs_recovery(stages[SUBJECT2][BASELINE], 
                                      stages[SUBJECT2][RECOVERY],
                                      subject_name[SUBJECT2])            
    """
    
    # plot frequency response of complete datasets  
    """
    s.plot_psds(data[SUBJECT1][BASELINE], srate, SUB1, BSL,
             channel_name,'by Channel over All Stages')
    s.plot_psds(data[SUBJECT1][RECOVERY], srate, SUB1, REC,
             channel_name,'by Channel over All Stages')
    s.plot_psds(data[SUBJECT2][BASELINE], srate, SUB2, BSL,
             channel_name,'by Channel over All Stages')
    s.plot_psds(data[SUBJECT2][RECOVERY], srate, SUB2, REC,
             channel_name,'by Channel over All Stages')   
    """
         
    # plot spectrograms of datasets
    
    """    
    s.plot_spectrograms(data[SUBJECT1][BASELINE], srate, SUB1, BSL)  
    """    
    
    # plot one hypnogram (spectrogram and sleep stage)
    #"""
    channel = 0 
    s.plot_hypnogram(data[SUBJECT1][BASELINE][channel], channel, 
                   stages[SUBJECT1][BASELINE], srate, SUB1, BSL) 
    #"""
    
    # plot all hypnograms for all 9 channels in dataset  
    """
    s.plotall_hypnograms(data[SUBJECT1][BASELINE], stages[SUBJECT1][BASELINE], 
                       srate, SUB1, BSL)  
    s.plotall_hypnograms(data[SUBJECT1][RECOVERY], stages[SUBJECT1][RECOVERY], 
                       srate, SUB1, REC)
    s.plotall_hypnograms(data[SUBJECT2][BASELINE], stages[SUBJECT2][BASELINE], 
                       srate, SUB2, BSL)  
    s.plotall_hypnograms(data[SUBJECT2][RECOVERY], stages[SUBJECT2][RECOVERY], 
                       srate, SUB2, REC) 
    """
    
#    v = interactive(beat_freq, f1=(200.0,300.0), f2=(200.0,300.0))
#    display(v)
     
    # plot FFT for All Stages, for a Single Channel
    """ 
    channel = 0 
    s.plot_psds(sdata[SUBJECT1][BASELINE][channel], srate, SUB1, BSL,
              stage_name, 'by Stage for '+str(channel_name[channel]))
    """

    # Plot Comparison of Baseline vs Recovery
    # for each observed sleep stage
    channel = 0
    for stage in range(0,6):
        s.compare_psds2(sdata[SUBJECT2][0][channel][stage], 
                        sdata[SUBJECT2][1][channel][stage], 
                        srate, SUB2, BSL, REC, 
                        channel_name[channel], stage_name[stage])

    
    
    
    
    