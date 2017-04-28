import numpy as np
import matplotlib.pyplot as plt

with open('../analysis/cylinder_subhist.dat', 'r') as subhist_file:
    line_number = 0
    data = []
    for line in subhist_file:
        line_number = line_number + 1
        if (line_number >= 3) & (line_number % 2 == 1):
            foo = line.split()
            map(float, foo)
            data_line = foo
        if (line_number >= 3) & (line_number % 2 == 0):
            foo = line.split()
            map(float, foo)
            data_line = np.concatenate([data_line, foo], axis=0)
            data = np.concatenate([data, data_line], axis=0)

data = data.reshape(data.size / data_line.size, data_line.size)
print data.shape

plt.figure()
plt.plot(data[:, 0], data[:, 6],
         data[:, 0], data[:, 7])
plt.show()
