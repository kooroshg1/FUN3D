import numpy as np
import matplotlib.pyplot as plt

t0 = 0.0
tf = 60.0
nt = 200
dt = tf / nt
simulation_time = 0
xcg = 0.
ycg = 0.
zcg = 0.

def transformMatrix(t):
    transform_matrix = np.eye(4)
    xcg, ycg, zcg = centerOfGragity(simulation_time)
    transform_matrix[0, 3] = xcg
    transform_matrix[1, 3] = ycg
    transform_matrix[2, 3] = zcg
    return transform_matrix

def centerOfGragity(t):
    xcg = 3 * (1 - np.exp(-0.1 * t)) * np.cos(0.25 * t)
    ycg = 0.
    zcg = 3 * (1 - np.exp(-0.1 * t)) * np.sin(0.25 * t)
    return xcg, ycg, zcg

with open('cylinder_motion.hst', 'w') as motion_file:
    for i in range(0, 9):
        motion_file.write("This line is written due to FUN3D's requirement!\n")
    while (simulation_time <= tf):
        motion_file.write("{:<6.4E}\n".format(simulation_time))
        if simulation_time == 0:
            xcg, ycg, zcg = centerOfGragity(simulation_time)
        else:
            xcg, ycg, zcg = centerOfGragity(simulation_time - dt)
        motion_file.write("{:<6.4E} {:<6.4E} {:<6.4E}\n".format(xcg, ycg, zcg))
        transform_matrix = transformMatrix(simulation_time)
        # Write transform matrix
        motion_file.write(
            "{:<6.4E} {:<6.4E} {:<6.4E} {:<6.4E}\n".format(transform_matrix[0, 0], transform_matrix[0, 1],
                                                               transform_matrix[0, 2], transform_matrix[0, 3]))
        motion_file.write(
            "{:<6.4E} {:<6.4E} {:<6.4E} {:<6.4E}\n".format(transform_matrix[1, 0], transform_matrix[1, 1],
                                                               transform_matrix[1, 2], transform_matrix[1, 3]))
        motion_file.write(
            "{:<6.4E} {:<6.4E} {:<6.4E} {:<6.4E}\n".format(transform_matrix[2, 0], transform_matrix[2, 1],
                                                               transform_matrix[2, 2], transform_matrix[2, 3]))
        motion_file.write(
            "{:<6.4E} {:<6.4E} {:<6.4E} {:<6.4E}\n".format(transform_matrix[3, 0], transform_matrix[3, 1],
                                                               transform_matrix[3, 2], transform_matrix[3, 3]))
        simulation_time = simulation_time + dt

t = np.linspace(0, tf, nt)
x, y, z = centerOfGragity(t)

plt.figure()
plt.plot(x, z)
plt.show()
