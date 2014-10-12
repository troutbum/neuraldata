#
#  NAME
#    problem_set1.py
#
#  DESCRIPTION
#    Open, view, and analyze raw extracellular data
#    In Problem Set 1, you will write create and test your own spike detector.
#

import numpy as np
import matplotlib.pylab as plt

def load_data(filename):
    """
    load_data takes the file name and reads in the data.  It returns two 
    arrays of data, the first containing the time stamps for when they data
    were recorded (in units of seconds), and the second containing the 
    corresponding voltages recorded (in units of microvolts - uV)
    """
    data = np.load(filename)[()];
    return np.array(data['time']), np.array(data['voltage'])
    
def bad_AP_finder(time,voltage):
    """
    This function takes the following input:
        time - vector where each element is a time in seconds
        voltage - vector where each element is a voltage at a different time
        
        We are assuming that the two vectors are in correspondance (meaning
        that at a given index, the time in one corresponds to the voltage in
        the other). The vectors must be the same size or the code
        won't run
    
    This function returns the following output:
        APTimes - all the times where a spike (action potential) was detected
         
    This function is bad at detecting spikes!!! 
        But it's formated to get you started!
    """
    
    #Let's make sure the input looks at least reasonable
    if (len(voltage) != len(time)):
        print "Can't run - the vectors aren't the same length!"
        APTimes = []
        return APTimes
    
    numAPs = np.random.randint(0,len(time))//10000 #and this is why it's bad!!
 
    # Now just pick 'numAPs' random indices between 0 and len(time)
    APindices = np.random.randint(0,len(time),numAPs)
    
    # By indexing the time array with these indices, we select those times
    APTimes = time[APindices]
    
    # Sort the times
    APTimes = np.sort(APTimes)
    
    return APTimes
    
def OLDgood_AP_finder(time,voltage):
    """
    This function takes the following input:
        time - vector where each element is a time in seconds
        voltage - vector where each element is a voltage at a different time
        
        We are assuming that the two vectors are in correspondance (meaning
        that at a given index, the time in one corresponds to the voltage in
        the other). The vectors must be the same size or the code
        won't run
    
    This function returns the following output:
        APTimes - all the times where a spike (action potential) was detected
    """
 
    APTimes = []
       
    #Let's make sure the input looks at least reasonable
    if (len(voltage) != len(time)):
        print "Can't run - the vectors aren't the same length!"
        return APTimes
    
    ##Your Code Here!
    # Set a threshold:  minimum voltage to be considered spike
#    threshold = 450                 # spikes_example
#    threshold = 250                 # spikes_easy_practice   
    threshold = 39                   # spikes_hard_practice   
    threshedTimes = time[voltage>threshold] 
    
    # filter results using minimum delay between spikes
    filteredTimes = []

#    minDelay = 0.0000344   # TrueSpikes= 100% FalseSpikeRate= 0.86 spikes/s
    # used for example and spikes_easy_practice set
    
    minDelay = 0.0000444   # TrueSpikes= 92% FalseSpikeRate= -0.34 spikes/s
    # used for spikes_hard_practice
        
    i = 0          
    for i in range(len(threshedTimes) - 1):  
        if i == 0:
            filteredTimes.append(threshedTimes[i])
        else:
            if threshedTimes[i+1] - threshedTimes[i] > minDelay:
                filteredTimes.append(threshedTimes[i])
#DEBUG           else:
#DEBUG             print('Filtered spike at time = ' + str(threshedTimes[i])) 
    
    APTimes = np.array(filteredTimes)                       
    return APTimes

def threshold_data(time,voltage,threshold):
    """
    This function takes the following input:
        time - vector where each element is a time in seconds
        voltage - vector where each element is a voltage at a different time                
        threshold - a value above which indicates a detected spike
        
        This function is a simple threshold test.  If the value of
        the voltage array is above the threshold the boolean result is stored
        in a mask.  The mask is then used to select corresponding values
        from the time array.
    
    This function returns the following output:
        threshedTimes - an array of time values in seconds
    """
    mask = voltage > threshold       # boolean mask
    threshedTimes = time[mask]       # threshold detected spikes                          
       
    return threshedTimes  
    
def filter_data(times, spacing):  
    """
    This function takes the following input:
        times - an array of times in seconds where spikes detected
        spacing - a minimum time separation between detected spikes
        
        This function filters the input by using a minimum
        time separation between thresholded spikes using
        np.diff() to find differences between n+1 and n elements
        of the input array.
    
    This function returns the following output:
        filteredTimes - a filtered subset of the input array
    """
    t0 = times[0]                   # keep the first detected spike
    tt = times[1:]                  # everything but the first detected spike 

    mask2 = np.diff(times) > spacing      
    ttt = tt[mask2]                         # filter spikes  
    filteredTimes = np.insert(ttt, 0, t0)   # assemble results 
 
    return filteredTimes  

#    Previous Trial and Error results:
#
#    Vthreshold = 250                 # spikes_easy_practice  
#    Spacing = 0.0000344 
#    TrueSpikes= 100% 
#    FalseSpikeRate= 0.86 spikes/s

#    Vthreshold = 39                   # spikes_hard_practice   
#    Tspacing = 0.0000444  
#    Percent True Spikes = 93.6708860759
#    False Spike Rate = -0.341566742834 spikes/s
   
    
def good_AP_finder(time,voltage):
    """
    This function takes the following input:
        time - vector where each element is a time in seconds
        voltage - vector where each element is a voltage at a different time
        
        We are assuming that the two vectors are in correspondance (meaning
        that at a given index, the time in one corresponds to the voltage in
        the other). The vectors must be the same size or the code
        won't run
    
    This function returns the following output:
        APTimes - all the times where a spike (action potential) was detected
    """
    APTimes = []
       
    #Let's make sure the input looks at least reasonable
    if (len(voltage) != len(time)):
        print "Can't run - the vectors aren't the same length!"
        return APTimes
       
    Vthreshold = 4.65* np.average(np.absolute(voltage))  
    threshedTs = threshold_data(time,voltage,Vthreshold)

    Tspacing = 0.004
    APTimes = filter_data(threshedTs, Tspacing)
                      
    return APTimes    

def get_actual_times(dataset):
    """
    Load answers from dataset
    This function takes the following input:
        dataset - name of the dataset to get answers for

    This function returns the following output:
        APTimes - spike times
    """    
    return np.load(dataset)
    
def detector_tester(APTimes, actualTimes):
    """
    returns percentTrueSpikes (% correct detected) and falseSpikeRate
    (extra APs per second of data)
    compares actual spikes times with detected spike times
    This only works if we give you the answers!
    """
    
    JITTER = 0.025 #2 ms of jitter allowed
    
    #first match the two sets of spike times. Anything within JITTER_MS
    #is considered a match (but only one per time frame!)
    
    #order the lists
    detected = np.sort(APTimes)
    actual = np.sort(actualTimes)
    
    #remove spikes with the same times (these are false APs)
    temp = np.append(detected, -1)
    detected = detected[plt.find(plt.diff(temp) != 0)]
 
    #find matching action potentials and mark as matched (trueDetects)
    trueDetects = [];
    for sp in actual:
        z = plt.find((detected >= sp-JITTER) & (detected <= sp+JITTER))
        if len(z)>0:
            for i in z:
                zz = plt.find(trueDetects == detected[i])
                if len(zz) == 0:
                    trueDetects = np.append(trueDetects, detected[i])
                    break;
    percentTrueSpikes = 100.0*len(trueDetects)/len(actualTimes)
    
    #everything else is a false alarm
    totalTime = (actual[len(actual)-1]-actual[0])
    falseSpikeRate = (len(APTimes) - len(actualTimes))/totalTime
    
    print 'Action Potential Detector Performance performance: '
    print '     Correct number of action potentials = ' + str(len(actualTimes))
    print '     Percent True Spikes = ' + str(percentTrueSpikes)
    print '     False Spike Rate = ' + str(falseSpikeRate) + ' spikes/s'
    print 
    return {'Percent True Spikes':percentTrueSpikes, 'False Spike Rate':falseSpikeRate}
    
    
def plot_spikes(time,voltage,APTimes,titlestr):
    """
    plot_spikes takes four arguments - the recording time array, the voltage
    array, the time of the detected action potentials, and the title of your
    plot.  The function creates a labeled plot showing the raw voltage signal
    and indicating the location of detected spikes with red tick marks (|)
    """
    plt.figure()   
    # Make and label plot
    plt.plot(time,voltage, hold=True)
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (uV)')
    plt.title(titlestr)
    
    # create y-coordinates for spike tick marks
    tickY_bottom = max(v) + 10
    tickY_top = tickY_bottom + 50
    for val in APTimes:
        # draw vertical tick marks; using convention of [x0, x1] [y0, y1]
        plt.plot([val, val], [tickY_bottom, tickY_top], 'k-', color='r')
    plt.show()

def plot_spikes_actuals(time,voltage,APTimes,actualTimes, titlestr):
    """
    plot_spikes takes five arguments - the recording time array, the voltage
    array, the time of the detected action potentials, the time of the
    actual action potentials, and the title of your
    plot.  The function creates a labeled plot showing the raw voltage signal
    and indicating the location of detected spikes with red tick marks (|)
    and the actual spikes with green tick marks (|)
    """
    plt.figure()   
    # Make and label plot
    plt.plot(time,voltage, hold=True)
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (uV)')
    plt.title(titlestr)
    
    # create y-coordinates for spike tick marks
    tickY_bottom = max(v) + 10
    tickY_top = tickY_bottom + 50
    for val in APTimes:
        # draw vertical tick marks; using convention of [x0, x1] [y0, y1]
        plt.plot([val, val], [tickY_bottom, tickY_top], 'k-', color='r')
        
    tickY_bottom = max(v) + 60
    tickY_top = tickY_bottom + 100
    for val in actualTimes:
        # draw vertical tick marks; using convention of [x0, x1] [y0, y1]
        plt.plot([val, val], [tickY_bottom, tickY_top], 'k-', color='g')
    
    plt.show()    
    
def plot_waveforms(time,voltage,APTimes,titlestr):
    """
    plot_waveforms takes four arguments - the recording time array, the voltage
    array, the time of the detected action potentials, and the title of your
    plot.  The function creates a labeled plot showing the waveforms for each
    detected action potential
    """  
    plt.figure()  
    
    # calculate number of measurements ("bins") to capture for each AP
    sideWidth = 0.003   # +/- 3 milliseconds
    timeStep = t[1]-t[0]
    sideBins = int(sideWidth / timeStep)
    bins = sideBins * 2
        
    # re-scale x-axis (time) with AP spike centered at zero 
    subsetT = np.linspace(-sideWidth, sideWidth, bins)  
    subsetV = np.zeros(bins)
   
    for val in range(len(APTimes)):  
        # find index of action potential (AP) in t data array
        spikeTime = APTimes[val]
        tIndex = plt.find(t == spikeTime)
#DEBUG        print('Detected Action Potential at time = ' + str(spikeTime), tIndex)
        
        ## obtain indices for the data interval near a given AP        
        startIndex = tIndex - sideBins
        if startIndex < 0:  # make sure index is never less than zero
            startIndex = 0    
        endIndex = tIndex + sideBins
        indices = range(startIndex, endIndex)
    
        # subset dataset around given AP
        # Warning:  if AP too close to zero the dataset is too small
        # and needs to be zero-filled
        if len(indices) == bins:   # complete data available
            # subsetT = t[indices]
            subsetV = v[indices]
        else:                       # close to zero, special handling
            missing = bins - len(indices)
            for i in range(missing):
                subsetV[i] = 0      # zero-fill unavailable values         
            i = missing
            j = 1
            while i < bins:         # get actual voltage measurement
                subsetV[i] = v[indices[j]]   
                
        # plot waveform of zoomed in view of action potential       
        plt.plot(subsetT, subsetV, hold=True)
#        print('time endpoints =', subsetT[0], subsetT[-1],
#              'voltage endpoints = ', subsetV[0], subsetV[-1])  

    # Make and label plot  
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (uV)')
    plt.title(titlestr)               
    plt.show()
    

        
##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
#    t,v = load_data('spikes_example.npy')
#    actualTimes = get_actual_times('spikes_example_answers.npy')
#    # APTimes = bad_AP_finder(t,v)
#    APTimes = good_AP_finder(t,v)
#    plot_spikes(t,v,APTimes,'Action Potentials in Raw Signal')
#    plot_waveforms(t,v,APTimes,'Waveforms')
#    detector_tester(APTimes,actualTimes)
#    # plot_spikes_actuals(t,v,APTimes,actualTimes, 'Predicted vs Actual Spikes')
    
    t,v = load_data('spikes_easy_practice.npy')
    actualTimes = get_actual_times('spikes_easy_practice_answers.npy')
    APTimes = good_AP_finder(t,v)
    plot_spikes(t,v,APTimes,'Action Potentials in Raw Signal in Easy Dataset')
    plot_waveforms(t,v,APTimes,'Waveforms from Easy Dataset')
    detector_tester(APTimes,actualTimes)

    t,v = load_data('spikes_hard_practice.npy')
    actualTimes = get_actual_times('spikes_hard_practice_answers.npy')
    APTimes = good_AP_finder(t,v)
    plot_spikes(t,v,APTimes,'Action Potentials in Raw Signal in Hard Dataset')
    plot_waveforms(t,v,APTimes,'Waveforms from Hard Dataset')
    detector_tester(APTimes,actualTimes)
 