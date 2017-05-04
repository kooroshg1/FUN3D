import numpy as np
import matplotlib.pyplot as plt
import os
import time
import pyFun3d as fun3d

m = 1.0
c = 0.0
k = 1.0
nt = 40000

dt = 0.1
A = np.matrix([[0, 1], [-k/m, -c/m]])
X = np.zeros([2, nt])
X[1, 0] = 0.0

def load_ready():
    while not os.path.exists('new_airloads_are_ready'):
        time.sleep(0.1)
    current_time = np.loadtxt('new_airloads_are_ready')
    os.remove('new_airloads_are_ready')
    return current_time

def update_load():
    current_time = load_ready()
    data = fun3d.read_ddfdrive()
    Fz = np.sum(data['fz'])
    return np.array([0., Fz / m]).reshape(-1, 1), current_time, Fz


Fn = 0.
un = 0.
udotn = 0.2
dddotn = 0.
with open('solution.txt', 'w') as solution_file:
    for it in range(0, nt - 1):
        if os.path.exists('new_surface_is_ready'):
            os.remove('new_surface_is_ready')
        t = it * dt
        F, current_time, Fnp1 = update_load()
        # Forward Euler
        # foo = (A.dot(X[:, it].reshape(-1, 1)) + (Fn + Fnp1) / 2.0) * dt + X[:, it].reshape(-1, 1)
        # fun3d.update_surface(dispz=foo[0, 0])
        # Fn = Fnp1
        # X[0, it + 1] = foo[0, 0]
        # X[1, it + 1] = foo[1, 0]
        # print "Time = ", current_time, ", disp = ", foo[0, 0], ", vel = ", foo[1, 0], ", Fz = ", Fn

        # Newmark beta
        beta = 1. / 4.
        gamma = 1. / 2.
        uddotn = (Fn - k * un) / m
        Kprime = k + 1. / (beta * dt ** 2.) * m
        Fprimenp1 = Fnp1 + m / (beta * dt ** 2.0) * (un + dt * udotn + (1. / 2. - beta) * dt ** 2.0 * uddotn)
        unp1 = Fprimenp1 / Kprime
        uddotnp1 = 1. / (beta * dt ** 2.0) * (unp1 - un - dt * udotn - dt ** 2.0 * (1. / 2. - beta) * uddotn)
        udotnp1 = udotn + dt * ((1 - gamma) * uddotn + gamma * uddotnp1)
        Fn = Fnp1
        un = unp1
        udotn = udotnp1
        uddotn = uddotnp1
        fun3d.update_surface(dispz=unp1)
        print "Time = ", current_time, ", disp = ", unp1, ", vel = ", udotnp1, ", Fz = ", Fnp1
        X[0, it + 1] = unp1
        X[1, it + 1] = udotnp1
        solution_file.write("{:<8.6f} {:<8.6f} {:<8.6f} {:<8.6f}".format(float(current_time), unp1, udotnp1, Fnp1))

        surface_file = open('fea_finished', 'w')
        surface_file.write(current_time)
        surface_file.close()
