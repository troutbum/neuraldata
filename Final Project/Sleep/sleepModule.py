# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 19:09:51 2014

@author: Troutbum
"""
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import pandas as pd
import matplotlib.pylab as plt
import matplotlib.mlab as m
import numpy as np
import matplotlib.pyplot as p

# copy from sleepFinalProject.py  (is there a way to link global constants?)
channel_name = ['EEG Ch1', 'EEG Ch2', 'EEG Ch8','EEG Ch9',
                'EOG Ch3', 'EOG Ch4',
                'EMG Ch5', 'EMG Ch6', 'EMG Ch7'];    

def runFFT(data, rate, Fcutoff):
    """
    FFT analysis, low-pass filtering then normalization
    returns freqs, Pxx, nPxx, nMaxY
    """
    Pxx, freqs = m.psd(data, NFFT=512, Fs=rate)  
    # lowpass filter, trim above cutoff frequency
    df = pd.DataFrame({'freqs' : freqs, 'Pxx' : Pxx})    
    df = df.ix[df.freqs <= Fcutoff]
    # normalize after lowpass filter    
    df['nPxx'] = df.Pxx/sum(df.Pxx)
    #df['nMaxY'] = df.nPxx.max()   does not work right
    return df
        
def compare_psds2(data1, data2, rate, subject, condition1, condition2,
                 channel, stage):
    """
    Plot PSDs of 2 datasets
    implements low-pass filter to eliminate 60 Hz noise
        """
    Fcutoff = 55  # threshold for low-pass filter    
        
    fig = plt.figure()   
      # common title
    fig.suptitle('Frequency Response ('+channel
                +') - Subject #'+subject+' '+condition1+
                ' vs. '+condition2,
                fontsize=14, fontweight='bold')            
    # common ylabel
    fig.text(0.06, 0.5, 'Normalized Power Spectral Density', 
             ha='center', va='center', rotation='vertical',
             fontsize=14, fontweight='bold')
    # common xlabel
    fig.text(0.5, 0.05,'Frequency (Hz)',
             ha='center', va='center',fontsize=14, fontweight='bold')
        
    # FFT for data1
    df1 = runFFT(data1, rate, Fcutoff)
    maxY = df1.nPxx.max() 
    
    # FFT for data2
    df2 = runFFT(data2, rate, Fcutoff)
    if df2.nPxx.max() > maxY:
        maxY = df2.nPxx.max()      
       
    # overlay psds for baseline & recovery conditions   
    plt.subplot(2, 1, 1)                    
    plt.bar(df1.freqs, df1.nPxx, label=condition1, width=0.2,
            edgecolor = 'none') 
    plt.plot(df2.freqs, df2.nPxx, label=condition2, color='r')
          
    plt.axis([0,Fcutoff,0,maxY])
    plt.legend()      
    plt.title(stage) 
    
    # plot differential between recovery & baseline conditions
    plt.subplot(2, 1, 2)
    plt.bar(df1.freqs, (df2.nPxx - df1.nPxx), 
            label='', width=0.2, color='r',
            edgecolor = 'none')
    plt.axis([0,Fcutoff,min(df2.nPxx - df1.nPxx),maxY]) 
    plt.title(str(stage)+' Differential ('+str(condition1)+' - '
                +str(condition2) +' )')   
    plt.show()
    return      
    
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
        plot_hypnogram(dataset[ch], ch, stages, rate, subject, condition)
 
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

def plot_psds(data, rate, subject, condition, label_set, title):
    """
    Plots the frequency response for all 9 channels
    using the entire recording    
    """
    fig = plt.figure()   
   # common title
    fig.suptitle('Frequency Response ('+title
            +') - Subject #'+subject+' '+condition, 
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

    # determine max response to scale y-axis 
    maxY = 0
    for i in range(0, len(data)):
        Pxx, freqs = m.psd(data[i], NFFT=512, Fs=rate)
        normalizedPxx = Pxx/sum(Pxx)
        if normalizedPxx.max() > maxY:
            maxY = normalizedPxx.max()
                 
    # plot all subplots
    for i in range(0, len(data)):
        plt.subplot(4, 3, sub_order[i])  # 4 x 3 layout
        #plt.subplot(9, 1, i + 1)  # vertical 9 x 1 layout
        plt.subplots_adjust(hspace=.6)  # adds space between subplots
        
        Pxx, freqs = m.psd(data[i], NFFT=512, Fs=rate)
        normalizedPxx = Pxx/sum(Pxx)
        #plt.plot(freqs, normalizedPxx, label=label_set[ch])
        plt.bar(freqs, normalizedPxx, label=label_set[i],width=0.2)
        plt.axis([0,70,0,maxY])
        
        plt.title(label_set[i]) 
        #plt.xlabel('Frequency (Hz)')
        #plt.ylabel('Normalized Power Spectral Density')        
      
        ## Inserted into plotting loop
        ## Possible Classifier - calculate average power-weighted frequency    
#        sumPower = 0
#        for j in range(0, len(normalizedPxx)):
#            sumPower = sumPower + (normalizedPxx[j] * freqs[j])
#    
#        avgFreq = sumPower/len(freqs)
#        print(channel_name[i] + " average frequency = " + str(avgFreq))
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
    plt.annotate(mString, xy=(0.75, 0.5), xycoords='axes fraction', 
                 size=6)
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
    

def plot_3Dbar(xpos, ypos, dz):
 
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
 
    #xpos = [1,2,3,4,5,6,7,8,9,10]
    #ypos = [2,3,4,5,1,6,2,1,7,2]
    num_elements = len(xpos)
    zpos = np.zeros(num_elements)
    dx = np.ones(num_elements)*0.2
    dy = np.ones(num_elements)*0.2
    #dz = [1,2,3,4,5,6,7,8,9,10]
 
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='#00ceaa')
    ax.set_xlabel('Channel')
    ax.set_ylabel('Sleep Stage')
    ax.set_zlabel('Score')  
    
    plt.show() 
    return

def plot_3Dscatter(xpos, ypos, dz):
 
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
 
    num_elements = len(xpos)
    zpos = np.zeros(num_elements)
    dx = np.ones(num_elements)*0.2
    dy = np.ones(num_elements)*0.2
 
    ax.scatter(xpos, ypos, zpos, dx, dy, dz, color='#00ceaa')
    ax.set_xlabel('Channel')
    ax.set_ylabel('Sleep Stage')
    ax.set_zlabel('Score')  
    
    plt.show() 
    return


def plot_3Dwireframe(X, Y, Z):  
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.plot_wireframe(X, Y, Z, rstride=100, cstride=100)
    ax.set_xlabel('Channel')
    ax.set_ylabel('Sleep Stage')
    ax.set_zlabel('Score')  
    return
 
#def plot_3Dsurface(X, Y, Z):  
#    fig = plt.figure(figsize=(14,6))
#    
#    # `ax` is a 3D-aware axis instance because of the projection='3d' keyword argument to add_subplot
#    ax = fig.add_subplot(1, 2, 1, projection='3d')
#    
#    p = ax.plot_surface(X, Y, Z, rstride=4, cstride=4, linewidth=0)
#    
#    # surface_plot with color grading and color bar
#    ax = fig.add_subplot(1, 2, 2, projection='3d')
#    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, 
#                    linewidth=0, antialiased=False)
#    fig.colorbar(p, shrink=0.5) 
#    return
    
def plot_3Dsurface(x, y, Z):      
    X, Y = np.meshgrid(x, y)    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.3)
    cset = ax.contourf(X, Y, Z, zdir='z', offset=0, cmap=cm.coolwarm)
    cset = ax.contourf(X, Y, Z, zdir='x', offset=0, cmap=cm.coolwarm)
    cset = ax.contourf(X, Y, Z, zdir='y', offset=0, cmap=cm.coolwarm)
    
    ax.set_xlabel('Channel')
    ax.set_ylabel('Sleep Stage')
    ax.set_zlabel('Score')  
    
    plt.show()
    return