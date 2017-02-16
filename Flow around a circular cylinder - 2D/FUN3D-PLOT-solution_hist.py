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
with open("cylinder_subhist copy.dat") as history_file:
    total_line_number = 0
    for lines in history_file:
        total_line_number = total_line_number + 1
total_line_number = total_line_number - 2
data = np.zeros([total_line_number/2, 13])
with open("cylinder_subhist copy.dat") as history_file:
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

print "Solution final time = ", data[-1, 0]
# plt.figure()
# plt.semilogy(data[:, 0], data[:, 1], 'k',
#              data[:, 0], data[:, 2], 'r',
#              data[:, 0], data[:, 3], 'g',
#              data[:, 0], data[:, 4], 'b')
# plt.xlabel('Time step')
# plt.ylabel('Magnitude')
# plt.legend(['mass', 'x-momentum', 'y-momentum', 'z-momentum'])
# plt.title('Residual Information')

plt.figure()
plt.plot(data[:, 0], data[:, -1], 'k')
plt.xlabel('Time')
plt.ylabel('Force')
plt.title(r'$C_D$')

plt.figure()
plt.plot(data[:, 0], data[:, -2], 'k')
plt.xlabel('Time')
plt.ylabel('Force')
plt.title(r'$C_L$')
plt.show()

# # Residual plotting
# plt.figure()
# plt.semilogy(data[:, 0], data[:, 1], 'k',
#              data[:, 0], data[:, 2], 'r',
#              data[:, 0], data[:, 3], 'g',
#              data[:, 0], data[:, 4], 'b')
# plt.xlabel('Time step')
# plt.ylabel('Magnitude')
# plt.legend(['mass', 'x-momentum', 'y-momentum', 'z-momentum'])
# plt.title('Residual Information')
# plt.show()
#
# # Force plot
# plt.figure()
# plt.plot(data[:, 0], data[:, -1], 'k',
#          data[:, 0], data[:, -2], 'k--')
# plt.xlabel('Time step')
# plt.ylabel('Magnitude')
# plt.legend(['C_D', 'C_L'])
# plt.title('Forces on boundaries')
# plt.show()
