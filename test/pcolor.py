# Implementation of matplotlib function
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

Z = np.random.rand(16, 30)

fig, (ax0, ax1) = plt.subplots(2, 1)

c = ax0.pcolor(Z)

c = ax1.pcolor(Z, edgecolors ='k', linewidths = 1)
ax1.set_title('2.Example with edges')

ax0.set_title('matplotlib.axes.Axes.pcolor() \
Examples\n1.Example with no edges')
plt.show()
