import numpy as np

# ------------------------------------------
# User input
lx = 1.0 # length of the domain in x
ly = 1.0 # length of the domain in y
lz = 0.1 # length of the domain in z

nx = 100 # Number of nodes in x direction
ny = 100 # Number of nodes in y direction
nz = 2 # Number of nodes in z direction
# ------------------------------------------
def write_coordinate(f, x):
    n = len(x)
    print "number of nodes written = " + str(len(x))
    for i in range(n):
        # c = '\n' if i % 5 == 0 or i + 1 == n else '  '
        c = '\n' if i + 1 == n else '  '
        f.write('{:18.11E}{}'.format(x[i], c))

def write_nmf(filename, nx, ny, nz):
    with open(filename, 'w') as f:
        contents = """# ===== Neutral Map File ===========================================================
# ==================================================================================
# Block#   IDIM   JDIM   KDIM
# ----------------------------------------------------------------------------------
1

1   {0:4d}   {1:4d}   {2:4d}

# ==================================================================================
# Type               B1  F1    S1   E1   S2   E2   B2  F2   S1   E1   S2   E2   Swap
# ----------------------------------------------------------------------------------
'symmetry_z_strong'   1   1     1 {0:4d}    1 {1:4d}
'symmetry_z_strong'   1   2     1 {0:4d}    1 {1:4d}
'viscous_solid'       1   3     1 {1:4d}    1 {2:4d}
'viscous_solid'       1   4     1 {1:4d}    1 {2:4d}
'viscous_solid'       1   5     1 {2:4d}    1 {0:4d}
'viscous_solid'       1   6     1 {2:4d}    1 {0:4d}
"""
        shape = (nx, ny, nz)
        f.write(contents.format(*shape))

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


with open("lidDrivenCavity.p3d", "w") as mesh_file:
    shape = (nx, ny, nz)
    mesh_file.write('1\n')
    mesh_file.write('{} {} {}\n'.format(*shape))
    write_coordinate(mesh_file, X)
    write_coordinate(mesh_file, Y)
    write_coordinate(mesh_file, Z)

write_nmf("lidDrivenCavity.nmf", nx, ny, nz)
