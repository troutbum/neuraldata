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
    
    ##Your Code Here!
    # Set a threshold:  minimum voltage to be considered spike
    threshold = 450
    threshedTimes = t[v>threshold] 
    

    # filter results using minimum delay between spikes
    filteredTimes = []
    minDelay = 0.0000344   # TrueSpikes= 100% FalseSpikeRate= 0.86 spikes/s

        
    i = 0          
    for i in range(len(threshedTimes) - 1):  
        if i == 0:
            filteredTimes.append(threshedTimes[i])
        else:
            if threshedTimes[i+1] - threshedTimes[i] > minDelay:
                filteredTimes.append(threshedTimes[i])
            else:
                print('Filtered spike at time = ' + str(threshedTimes[i])) 
    
    APTimes = np.array(filteredTimes)                       
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
        print('Detected Action Potential at time = ' + str(spikeTime), tIndex)
        
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
#if __name__ == "__main__":
#    t,v = load_data('spikes_example.npy')    
#    actualTimes = get_actual_times('spikes_example_answers.npy')
#    APTime = bad_AP_finder(t,v)
#    plot_spikes(t,v,APTime,'Your Code Here ')
#    plot_waveforms(t,v,APTime,'Your Code Here')
#    detector_tester(APTime,actualTimes)

t,v = load_data('spikes_example.npy')
actualTimes = get_actual_times('spikes_example_answers.npy')
# APTimes = bad_AP_finder(t,v)
APTimes = good_AP_finder(t,v)
plot_spikes(t,v,APTimes,'Action Potentials in Raw Signal')
plot_waveforms(t,v,APTimes,'Waveforms')
detector_tester(APTimes,actualTimes)
plot_spikes_actuals(t,v,APTimes,actualTimes, 'Predicted vs Actual Spikes')
  