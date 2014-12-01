# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 17:33:19 2014

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

CDIR = '/Users/Gene/Development/SleepEEGData/'

def load_eeg(filename, dirname=CDIR):
    """
    load_eeg takes the file name and reads in the data.  It returns an
    array containing EEG data and the sampling rate for
    the data in Hz (samples per second).
    """
    gc.collect()
    data = np.load(dirname + filename)
    return data['DATA'], data['srate'], data['stages']

def pull_stage(filename):
    """
    just stage data
    """
    dat = load_eeg(filename)
    return dat[2]

def pull_subject34_stages():
    """
    just stages from subjects 3 and 4
    """
    st0 = pull_stage(CFILES[2, 0])
    st1 = pull_stage(CFILES[2, 1])
    st2 = pull_stage(CFILES[3, 0])
    st3 = pull_stage(CFILES[3, 1])
    return np.array([[st0, st1], [st2, st3]]), np.array([[len(st0), len(st1)],
                                                         [len(st2), len(st3)]])

def subject34_stage4_list():
    """
    list of indices for stage 4s
    """
    stage4_indices = [[[], []], [[], []]]
    stages, stagelengths = pull_subject34_stages()
    for sidx in range(2):
        for bridx in range(2):
            stage4_indices[sidx][bridx] = plt.find(stages[sidx, bridx] == 4)
    gc.collect()
    return np.array(stage4_indices), stagelengths

def pull_lead1_epoch(subject, study, epoch_number):
    """
    just one epoch of lead 1 data
    """
    data, srate, _ = load_eeg(CFILES[subject][study])
    elength = srate * 30.0
    startpos = epoch_number * elength
    endpos = startpos + elength
    eegdata = deepcopy(data[0][startpos:endpos])
    return eegdata, srate

def plot_stage4_epoch(s4list, subject, study, choice, s4s, slens):
    """
    plot the eeg that should be stage 4
    plots data as given on top in blue,
    data as swapped from 3 to 4 as red on bottom
    """
    choices = s4list[subject - 2, study]
    if choice >= len(choices):
        choice = len(choices) - 1
    if choice < 0:
        choice = 0
    epoch_number = choices[choice]
    ydata, srate = pull_lead1_epoch(subject, study, epoch_number)
    if subject == 3:
        if(epoch_number >= slens[0, study]):
            epoch_number = slens[0, study] - 1
        altstage = s4s[0, study][epoch_number]
        swapsubject = 2
    else:
        if(epoch_number >= slens[1, study]):
            epoch_number = slens[1, study] - 1
        altstage = s4s[1, study][epoch_number]
        swapsubject = 3
    swapped_ydata, srate = pull_lead1_epoch(swapsubject, study, epoch_number)
    xdata = np.arange(0.0, 30.0, 1.0/srate)
    etime = epoch_number / 2.0
    if study == 0:
        condition = 'Baseline'
    else:
        condition = 'Recovery'
    dur = timedelta(minutes=etime)
    gc.collect()
    fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(24, 6))
    ax1.set_title('Subject ' + str(subject + 1) + ' at ' + condition +
                  ' at Stage 4 Epoch ' + str(epoch_number) + ' of ' +
                  str(slens[subject - 2, study]) + " (Time " + str(dur) + ','
                  + " Alternate Stage Was Labelled " + str(altstage) +')')
    fig.subplots_adjust(hspace=0)
    ax1.set_ylabel('Unswapped Voltage (microvolts)', fontsize=10)
    ax1.set_ylim(-400, 400)
    ax1.plot(xdata, ydata, 'b')
    ax1.set_xticks(np.arange(0, 30.0, 1.0))
    ax1.xaxis.grid(True)
    ax2.plot(xdata, swapped_ydata, 'r')
    ax2.set_ylabel('Swapped Voltage (microvolts)', fontsize=10)
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylim(-400, 400)
    ax2.set_xticks(np.arange(0, 30.0, 1.0))
    ax2.xaxis.grid(True)
    plt.show()

def input_for_plotting(s4list, s4s, slens):
    """
    new plots each time
    """
    while True:
        snum = input("Enter subject as 3 or 4 or negative to exit: ")
        if snum < 0:
            return
        if snum != 3 and snum != 4:
            print "Please enter 3 or 4."
            continue
        cond = input("Enter 0 for baseline, 1 for recovery: ")
        if cond != 0 and cond != 1:
            print "Please enter 0 or 1."
            continue
        numchoices = len(s4list[snum - 3, cond])
        epnum = input('Enter Nth stage 4 epoch from 0 to ' +
                      str(numchoices) + ': ')
        plot_stage4_epoch(s4list, snum - 1, cond, epnum, s4s, slens)
        gc.collect()
        return


if __name__ == "__main__":

    S4S, SLENGTHS = pull_subject34_stages()
    S4L, SLENGTHS = subject34_stage4_list()
    input_for_plotting(S4L, S4S, SLENGTHS)