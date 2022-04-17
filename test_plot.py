import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0.0, 10.0, 1000)
y = np.sin(x)

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(18, 5))

ax[0,0].plot(x, y, label='a')
ax[0,1].plot(x, y, label='b')
ax[1,0].plot(x, y, label='c')
ax[1,1].plot(x, y, label='d')

plt.show()