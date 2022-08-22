# Graphical Representation of numpy.linspace()
import numpy as np
import matplotlib.pyplot as plt

# Start = 0
# End = 2
# Samples to generate = 15
x1 = np.linspace(0, 2, 15, endpoint = True)
y1 = np.linspace(0, 2, 15, endpoint = True)
fig = plt.figure()
x1, y1 = np.meshgrid(x1, y1)
ax = fig.add_subplot(111)
ax.plot(x1, y1, ls="None", marker=".")
plt.show()