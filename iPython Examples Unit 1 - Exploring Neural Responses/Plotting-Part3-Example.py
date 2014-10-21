# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 22:34:59 2014

@author: Troutbum
"""

# create random data
y = np.random.randn(100)

# create x-axis, 100 ticks from 0 to 1
x = np.linspace(0,1,100)

# run plot function and then add horizontal line
create_waveform(x,y)
add_line(2)
