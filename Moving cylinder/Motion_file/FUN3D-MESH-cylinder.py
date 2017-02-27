import math
import argparse
import scipy.optimize

class RadialDistribution:
    def __init__(self, n = 101, x0 = 0.0, x1 = 1.0, dx = None):
        t = lambda i: float(i) / float(n - 1)
        s = lambda i, d: 1.0 + math.tanh(d * (t(i) - 1.0)) / math.tanh(d)
        f = lambda d: s(1, d) - dx / (x1 - x0)
        result = scipy.optimize.root(f, 1.0)
        if result.success:
            delta = result.x[0]
            self.values = [x0 + (x1 - x0) * s(i, delta) for i in range(n)]
        else:
            self.values = []

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __iter__(self):
        return iter(self.values)



class AxialDistribution:
    def __init__(self, n = 101):
        t = lambda i: float(i) / float(n - 1)
        a = lambda i: 2.0 * math.pi * t(i)
        self.values = [a(i) for i in range(n)]
        self.values[-1] = self.values[0]

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __iter__(self):
        return iter(self.values)



class CylinderMesh:
    def __init__(self, dims = (81, 41), ri = 1.0, ro = 10.0, dr = 0.01):
        x = lambda rho, phi: rho * math.cos(phi)
        y = lambda rho, phi: rho * math.sin(phi)
        self.rho = RadialDistribution(dims[1], ri, ro, dr)
        self.phi = AxialDistribution(dims[0])
        self.zed = [-0.5, 0.5]
        self.x = [x(r, a) for z in self.zed for r in self.rho for a in self.phi]
        self.y = [z       for z in self.zed for r in self.rho for a in self.phi]
        self.z = [y(r, a) for z in self.zed for r in self.rho for a in self.phi]

    def write(self, base):
        self.write_p3d(base + '.p3d')
        self.write_nmf(base + '.nmf')
        # self.write_tec(base + '.dat')

    def write_p3d(self, filename):
        with open(filename, 'w') as f:
            shape = (len(self.phi), len(self.rho), len(self.zed))
            f.write('1\n')
            f.write('{} {} {}\n'.format(*shape))
            self.write_coordinate(f, self.x)
            self.write_coordinate(f, self.y)
            self.write_coordinate(f, self.z)

    def write_coordinate(self, f, x):
        n = len(x)
        for i in range(n):
            c = '\n' if i % 5 == 0 or i + 1 == n else '  '
            f.write('{:18.11E}{}'.format(x[i], c))

    def write_nmf(self, filename):
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
'symmetry_y_strong'   1   1     1 {0:4d}    1 {1:4d}
'symmetry_y_strong'   1   2     1 {0:4d}    1 {1:4d}
'one-to-one'          1   3     1 {1:4d}    1 {2:4d}    1   4    1 {1:4d}    1 {2:4d}  FALSE
'viscous_solid'       1   5     1 {2:4d}    1 {0:4d}
'farfield_riem'       1   6     1 {2:4d}    1 {0:4d}
"""
            shape = (len(self.phi), len(self.rho), len(self.zed))
            f.write(contents.format(*shape))

    def write_tec(self, filename):
        with open(filename, 'w') as f:
            shape = (len(self.phi), len(self.rho), len(self.zed))
            nodeCount = (shape[0] - 1) * shape[2]
            faceCount = (shape[0] - 1) * (shape[2] - 1)
            f.write('TITLE = "Mode Shape"\n')
            f.write('VARIABLES = "X" "Y" "Z" "ID" "DX" "DY" "DZ"\n')
            f.write('ZONE T="Cylinder" I={} J={} F=FEPOINT\n'.format(nodeCount, faceCount))
            for k in range(shape[2]):
                for i in range(shape[0] - 1):
                    n = i + shape[0] * shape[1] * k
                    x = self.x[n]
                    y = self.y[n]
                    z = self.z[n]
                    dx = 0.0
                    dy = 0.0
                    dz = 1.0
                    nid = 1 + k + shape[1] * shape[2] * i
                    f.write('{:18.11E} {:18.11E} {:18.11E} {:6d} {:18.11E} {:18.11E} {:18.11E}\n'.format(x, y, z, nid, dx, dy, dz))
            for i in range(shape[0] - 1):
                for k in range(shape[2] - 1):
                    a = i + shape[0] * k + 1
                    b = a + shape[0] - 1
                    c = b + 1
                    d = a + 1
                    if i == shape[0] - 2:
                        c -= shape[0] - 1
                        d -= shape[0] - 1
                    f.write('  {:8d}  {:8d}  {:8d}  {:8d}\n'.format(a, b, c, d))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Generate a 2D mesh around a cylinder.')
    parser.add_argument('--i', metavar = 'IDIM',
                        default = 81, type = int,
                        help = 'number of grid points around the cylinder')
    parser.add_argument('--j', metavar = 'JDIM',
                        default = 41, type = int,
                        help = 'number of grid points in the radial direction')
    parser.add_argument('--radius', metavar = 'R',
                        default = 0.5, type = float,
                        help = 'radius of the cylinder')
    parser.add_argument('--farfield', metavar = 'R',
                        default = 125.0, type = float,
                        help = 'distance of the farfield from the center of the cylinder')
    parser.add_argument('--spacing', metavar = 'DR',
                        default = 0.01, type = float,
                        help = 'grid point spacing at the cylinder')
    parser.add_argument('name',
                        help = 'base name for the Plot3D and neutral map output files')
    args = parser.parse_args()

    mesh = CylinderMesh(dims = (args.i, args.j),
                        ri = args.radius,
                        ro = args.farfield,
                        dr = args.spacing)
    mesh.write(args.name)
