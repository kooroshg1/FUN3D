import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('../analysis/aehist_body1_mode1.dat', skiprows=3)

plt.figure()
plt.plot(data[:, 0], data[:, 1])
plt.xlabel('Time')
plt.ylabel('Displacement')
plt.show()