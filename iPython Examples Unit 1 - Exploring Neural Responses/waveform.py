# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 22:20:56 2014

@author: Troutbum
"""

import numpy as np
import matplotlib.pyplot as plt

def create_waveform(times, data):
    plt.plot(times,data, 'g-')
    plt.title('Waveform')
    return plt
    
def add_line(yval):
    """Add horizontal line at particular y location"""
    plt.axhline(y=yval)
    