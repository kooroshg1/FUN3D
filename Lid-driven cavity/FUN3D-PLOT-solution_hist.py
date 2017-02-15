import numpy as np
import matplotlib.pyplot as plt
import os
# Define font size for plot
font = {'family' : 'serif',
        'style' : 'normal',
        'weight' : 'medium',
        'size'   : 22}
plt.rc('font', **font)

# Find the name of the history file that will be plotted
current_path = os.path.dirname(os.path.realpath(__file__))
for fileName in os.listdir(current_path):
    if fileName.endswith(".dat"):
        file_name = fileName

# Read information
data = np.loadtxt(file_name, skiprows=3)

# Plotting
plt.figure()
plt.semilogy(data[:, 0], data[:, 1], 'k',
             data[:, 0], data[:, 2], 'r',
             data[:, 0], data[:, 3], 'g',
             data[:, 0], data[:, 4], 'b')
plt.legend(['mass', 'x-momentum', 'y-momentum', 'z-momentum'])
plt.title('Residual Information')
plt.show()