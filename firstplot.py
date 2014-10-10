# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 21:58:57 2014

@author: Troutbum
"""

import numpy as np
import matplotlib

x = np.linspace(0, 3*np.pi, 500)
plt.plot(x, np.sin(x))
plt.title('A Sinewave')
plt.show()