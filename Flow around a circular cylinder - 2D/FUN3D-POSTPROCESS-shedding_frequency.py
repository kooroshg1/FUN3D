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
with open(file_name) as history_file:
    total_line_number = 0
    for lines in history_file:
        total_line_number = total_line_number + 1
total_line_number = total_line_number - 2
data = np.zeros([total_line_number/2, 13])

with open(file_name) as history_file:
    file_line_number = 0
    data_line_number = 0
    for lines in history_file:
        file_line_number = file_line_number + 1
        if file_line_number < 3:
            continue
        current_line = lines.split()
        current_line = map(float, current_line)
        if file_line_number % 2 == 1:
            data[data_line_number, 0:11] = current_line
        else:
            data[data_line_number, 11:13] = current_line
            data_line_number = data_line_number + 1

data[:, 0] = data[:, 0] / 10
# Calculate the shedding frequency
print data.shape
start_index = 150000
dt = data[3, 0] - data[2, 0]
fs = 1 / dt # Sampling frequency
df = fs / len(data[start_index:, 0])
Fy = np.fft.fft(data[start_index:, -2])
omega = np.linspace(0, fs, len(data[start_index:, 0]))
PSD_Fy = np.abs(Fy)**2.

index = np.argmax(PSD_Fy[0:len(omega)/2])
Sr = omega[index] * 1 / 1
print Sr

plt.figure()
plt.semilogy(omega[0:len(omega)/2], PSD_Fy[0:len(omega)/2], 'k')
plt.xlim([0, 0.5])
plt.xlabel('Frequency')
plt.ylabel('PSD')
plt.title('Power spectral density function')

plt.figure()
plt.plot(data[:, 0], data[:, -2], 'k')
plt.xlabel('Time')
plt.ylabel('Force')
plt.title('Drag force time history')

plt.show()