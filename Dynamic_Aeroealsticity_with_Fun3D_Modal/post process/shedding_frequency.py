import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('../analysis/aehist_body1_mode1.dat', skiprows=3)

dt = data[3, 0] - data[2, 0]
fs = 1 / dt # Sampling frequency
df = fs / len(data)

# data = data[0:len(data)/2, :]
Dy = np.fft.fft(data[:, 1])
omega = np.linspace(0, fs, len(data[:, 0]))
PSD_Dy = np.abs(Dy)**2.

index = np.argmax(PSD_Dy[0:len(omega)/2])
Sr = omega[index] * 1 / 0.0670842
print Sr

plt.figure()
plt.plot(omega[0:len(data)/2], PSD_Dy[0:len(data)/2])
plt.show()