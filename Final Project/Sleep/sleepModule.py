# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 19:09:51 2014

@author: Troutbum
"""

import pandas as pd
import matplotlib.pylab as plt
import matplotlib.mlab as m

def compare_psds(data1, data2, rate, subject, condition1, condition2,
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
    Pxx, freqs = m.psd(data1, NFFT=512, Fs=rate)  
    # lowpass filter, cutoff frequency for 60Hz noise!  
    df1 = pd.DataFrame({'freqs' : freqs, 'Pxx' : Pxx})    
    df1 = df1.ix[df1.freqs <= Fcutoff]
    # normalize after lowpass filter    
    df1['normalPxx'] = df1.Pxx/sum(df1.Pxx)  
    # determine max response to scale y-axis 
    maxY = df1.normalPxx.max()

    # FFT for data2
    Pxx, freqs = m.psd(data2, NFFT=512, Fs=rate)
    # lowpass filter, cutoff frequency for 60Hz noise!
    df2 = pd.DataFrame({'freqs' : freqs, 'Pxx' : Pxx})    
    df2 = df2.ix[df2.freqs <= Fcutoff]
    # normalize after lowpass filter    
    df2['normalPxx'] = df2.Pxx/sum(df2.Pxx)  
    # determine max response to scale y-axis 
    if df2.normalPxx.max() > maxY:
        maxY = df2.normalPxx.max()        
   
    # overlay psds for baseline & recovery conditions   
    plt.subplot(2, 1, 1)                    
    plt.bar(df1.freqs, df1.normalPxx, label=condition1, width=0.2,
            edgecolor = 'none') 
    plt.plot(df2.freqs, df2.normalPxx, label=condition2, color='r')
      
    plt.axis([0,Fcutoff,0,maxY])
    plt.legend()      
    plt.title(stage) 

    # plot differential between recovery & baseline conditions
    plt.subplot(2, 1, 2)
    plt.bar(df1.freqs, (df2.normalPxx - df1.normalPxx), 
            label='', width=0.2, color='r',
            edgecolor = 'none')
    plt.axis([0,Fcutoff,min(df2.normalPxx - df1.normalPxx),maxY]) 
    plt.title(str(stage)+' Differential ('+str(condition1)+' - '
              +str(condition2) +' )')   
    plt.show()
    return   
    
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