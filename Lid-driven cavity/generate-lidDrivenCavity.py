import numpy as np
import matplotlib.pyplot as plt


def write_coordinate(f, x):
    n = len(x)
    print "number of nodes written = " + str(len(x))
    for i in range(n):
        # c = '\n' if i % 5 == 0 or i + 1 == n else '  '
        c = '\n' if i + 1 == n else '  '
        f.write('{:18.11E}{}'.format(x[i], c))

lx = 1.0
ly = 1.0
lz = 0.1

nx = 100
ny = 100
nz = 2

x = np.linspace(-lx/2.0, lx/2.0, nx)
y = np.linspace(-ly/2.0, ly/2.0, ny)
z = np.linspace(0, lz, nz)

X = np.zeros(nx * ny * nz)
Y = np.zeros(nx * ny * nz)
Z = np.zeros(nx * ny * nz)
index = 0
for iz in range(0, nz):
    for iy in range(0, ny):
        for ix in range(0, nx):
            X[index] = x[ix]
            Y[index] = y[iy]
            Z[index] = z[iz]
            index = index + 1


mesh_file = open("lidDrivenCavity.p3d", "w")
shape = (nx, ny, nz)
mesh_file.write('1\n')
mesh_file.write('{} {} {}\n'.format(*shape))
write_coordinate(mesh_file, X)
write_coordinate(mesh_file, Y)
write_coordinate(mesh_file, Z)
mesh_file.close()
