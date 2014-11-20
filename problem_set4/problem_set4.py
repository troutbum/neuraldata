#
#  NAME
#    problem_set4.py
#
#  DESCRIPTION
#    In Problem Set 4, you will classify EEG data into NREM sleep stages and
#    create spectrograms and hypnograms.
#
from __future__ import division
import numpy as np
import matplotlib.pylab as plt
import matplotlib.mlab as m

rowname = ['REM sleep', 'Stage 1 NREM sleep', 
             'Stage 2 NREM sleep', 'Stage 3 and 4 NREM sleep'];

def load_examples(filename):
    """
    load_examples takes the file name and reads in the data.  It returns an
    array containing the 4 examples of the 4 stages in its rows (row 0 = REM;
    1 = stage 1 NREM; 2 = stage 2; 3 = stage 3 and 4) and the sampling rate for
    the data in Hz (samples per second).
    """
    data = np.load(filename)
    return data['examples'], int(data['srate'])

def load_eeg(filename):
    """
    load_eeg takes the file name and reads in the data.  It returns an
    array containing EEG data and the sampling rate for
    the data in Hz (samples per second).
    """
    data = np.load(filename)
    return data['eeg'], int(data['srate'])

def load_stages(filename):
    """
    load_stages takes the file name and reads in the stages data.  It returns an
    array containing the correct stages (one for each 30s epoch)
    """
    data = np.load(filename)
    return data['stages']

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
                
#    Working code for plotting PSD for 4 example data sets    
#    for i in range(0, len(example)):
#        Pxx, freqs = m.psd(example[i], NFFT=512, Fs=rate)
#        normalizedPxx = Pxx/sum(Pxx)
#        plt.plot(freqs, normalizedPxx, label=rowname[i])
#        plt.xlabel('Frequency (Hz)')
#        plt.ylabel('Normalized Power Spectral Density')
#       
#    plt.xlim(0,20)
#    plt.legend(loc=0)
    
    return

def plot_example_spectrograms(example,rate):
    """
    This function creates a figure with spectrogram sublpots to of the four
    sleep examples. (Recall row 0 is REM, rows 1-3 are NREM stages 1,
    2 and 3/4)
    """
    plt.figure()
    
    ###YOUR CODE HERE
    for i in range(0, len(example)):
        plt.subplot(2,2,i+1)
        plt.title(rowname[i])    
        Pxx, freqs, bins, im = plt.specgram(example[i],NFFT=512,Fs=rate)       
        plt.ylim(0,70)
        plt.xlabel('Time (Seconds)')
        plt.ylabel('Frequency (Hz)')
      
    return
      
            
def classify_epoch(epoch,rate):
    """
    This function returns a sleep stage classification (integers: 1 for NREM
    stage 1, 2 for NREM stage 2, and 3 for NREM stage 3/4) given an epoch of 
    EEG and a sampling rate.
    """

    ###YOUR CODE HERE

    ## Better Classifier - Cummulative Power Distribution
    ## find where cummulative power exceeds threshold %
    threshold = 0.966
    #print('Cumulative Power - Threshold set to ' + str(threshold*100)+'%')
   
    # iterate over each example data set
    Pxx, freqs = m.psd(epoch, NFFT=512, Fs=rate)
    
    # normalize PSD
    normalizedPxx = Pxx/sum(Pxx)
  
    # determine cummulative power distribution 
    sumPxx = 0    
    j = 0        
    while sumPxx <= threshold:
        sumPxx = sumPxx + normalizedPxx[j]
        j = j + 1    
 
    # stop when cummulative power exceeds threshold %
    #print('Threshold Met at Frequency = '+str(freqs[j])+' Hz')
    threshFreq = freqs[j]
    
#    RESULTS CALCULATED FROM EXAMPLES[]
#    
#    REM sleep average frequency = 0.012304058983
#    Stage 1 NREM sleep average frequency = 0.0135085018377
#    Stage 2 NREM sleep average frequency = 0.0118527042459
#    Stage 3 and 4 NREM sleep average frequency = 0.00554269228828
#     
#    Threshold set to 95.0%
#    REM sleep - Threshold Met at Frequency = 10.25 Hz
#    Stage 1 NREM sleep - Threshold Met at Frequency = 10.75 Hz
#    Stage 2 NREM sleep - Threshold Met at Frequency = 13.0 Hz
#    Stage 3 and 4 NREM sleep - Threshold Met at Frequency = 3.75 Hz
 
    lowClassifier = 6
    hiClassifier = 11
 
    ## if most of the power is very low, then Stage 3/4 NREM
    if threshFreq <= lowClassifier:
        stage = 3
     
    ## Stage 2 NREM contains significant "sleep spindles"
    ## at 11-15 Hz 
    elif threshFreq >= hiClassifier:
        stage = 2

    ## Stage 1 NREM otherwise (similar to REM)
    else:
        stage =1
    
    return stage

def plot_hypnogram(eeg, stages, srate):
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
    ax2.plot(times, stages, drawstyle='steps')
    
    #Label your right y-axis and change the text color to match your plot
    ax2.set_ylabel('NREM Stage',color='b')


    #Set the limits for the y-axis 
    plt.ylim(0.5,3.5)
 
    #Only display the possible values for the stages
    ax2.set_yticks(np.arange(1,4))
    
    #Change the left axis tick color to match your plot
    for t1 in ax2.get_yticklabels():
        t1.set_color('b')
    
    #Title your plot    
    plt.title('Hypnogram - Practice Data') 

        
def classifier_tester(classifiedEEG, actualEEG):
    """
    returns percent of 30s epochs correctly classified
    """
    epochs = len(classifiedEEG)
    incorrect = np.nonzero(classifiedEEG-actualEEG)[0]
    percorrect = (epochs - len(incorrect))/epochs*100
    
    print 'EEG Classifier Performance: '
    print '     Correct Epochs = ' + str(epochs-len(incorrect))
    print '     Incorrect Epochs = ' + str(len(incorrect))
    print '     Percent Correct= ' + str(percorrect) 
    print 
    return percorrect
  
    
def test_examples(examples, srate):
    """
    This is one example of how you might write the code to test the provided 
    examples.
    """
    i = 0
    bin_size = 30*srate
    c = np.zeros((4,len(examples[1,:])/bin_size))
    while i + bin_size < len(examples[1,:]):
        for j in range(1,4):
            c[j,i/bin_size] = classify_epoch(examples[j,range(i,i+bin_size)],srate)
        i = i + bin_size
    
    totalcorrect = 0
    num_examples = 0
    for j in range(1,4):
        canswers = np.ones(len(c[j,:]))*j
        correct = classifier_tester(c[j,:],canswers)
        totalcorrect = totalcorrect + correct
        num_examples = num_examples + 1
    
    average_percent_correct = totalcorrect/num_examples
    print 'Average Percent Correct= ' + str(average_percent_correct) 
    return average_percent_correct

def classify_eeg(eeg,srate):
    """
    DO NOT MODIFY THIS FUNCTION
    classify_eeg takes an array of eeg amplitude values and a sampling rate and 
    breaks it into 30s epochs for classification with the classify_epoch function.
    It returns an array of the classified stages.
    """
    bin_size_sec = 30
    bin_size_samp = bin_size_sec*srate
    t = 0
    classified = np.zeros(len(eeg)/bin_size_samp)
    while t + bin_size_samp < len(eeg):
       classified[t/bin_size_samp] = classify_epoch(eeg[range(t,t+bin_size_samp)],srate)
       t = t + bin_size_samp
    return classified
        
##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
    #YOUR CODE HERE
    
    plt.close('all') #Closes old plots.    
    
    ##PART 1
    #Load the example data
    examples, srate = load_examples('example_stages.npz')
    #Plot the psds
    plot_example_psds(examples,srate)
    #Plot the spectrograms
    plot_example_spectrograms(examples,srate)
   
   #Test the examples   
    for j in range(0, len(examples)):
        print('')
        print('Testing Example : '+rowname[j])
        print('')
        for i in range(0, 10):
            start = i * 3840
            end = ((i + 1) * 3840)
            epoch = examples[j][start:end]
            print('Predicted NREM Stage = ' + str(classify_epoch(epoch,srate)))
   
    # supplied tester
    test_examples(examples, srate)
    
    #Load the practice data
    eeg, srate = load_eeg('practice_eeg.npz')   
    #Load the practice answers
    stages = load_stages('practice_answers.npz')
    
    #Classify the practice data
    classifiedEEG = classify_eeg(eeg,srate)  
    
    #Check your performance
    actualEEG = stages
    classifier_tester(classifiedEEG, actualEEG)
 
    #Generate the hypnogram plots
    #plot_hypnogram(eeg, stages, srate)
    plot_hypnogram(eeg, classifiedEEG, srate)
    
    #Run classifier on another data set "test_eeg" and plot
    print('')
    print('Loading "test_eeg" data set')
    eeg2, srate2 = load_eeg('test_eeg.npz')   
    print('Analyzing "test_eeg" data set')
    classifiedEEG2 = classify_eeg(eeg2,srate2)
    print('Plotting "test_eeg" data set')
    plot_hypnogram(eeg2, classifiedEEG2, srate2)
    plt.title('Hypnogram - Test Data')  # override title


