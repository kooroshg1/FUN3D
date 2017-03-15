import numpy as np
import matplotlib.pyplot as plt

def calculate_load(filename="cylinder_ddfdrive_body1.dat", rho=1.0, U=1.0, plot_surface_loads=False):
    print "Calculating aerodynamic load ..."
    with open(filename) as load_file:
        line = load_file.readline()
        line = load_file.readline()
        line = load_file.readline()
        start = line.find("i=")
        end = line[start:].find(",")
        number_of_points_on_surface =  int(line[start+2:start+end])
        data = np.zeros([number_of_points_on_surface, 10])
        for i in range(0, number_of_points_on_surface):
            data[i, :] = load_file.readline().split()

    Xc = np.mean(data[:, 0])
    Yc = np.mean(data[:, 1])
    Zc = np.mean(data[:, 2])
    theta = np.arctan2(data[:, 2] - Zc, data[:, 0] - Xc)
    R = (np.max(data[:, 0]) - np.min(data[:, 0])) / 2.
    # dA = 2 * np.pi * R / len(theta)
    dA = 1.0
    Fx = np.sum(0.5 * rho * U**2.0 * dA * data[:, 5])
    Fy = np.sum(0.5 * rho * U**2.0 * dA * data[:, 6])
    Fz = np.sum(0.5 * rho * U**2.0 * dA * data[:, 7])

    if plot_surface_loads:
        plt.figure()
        plt.plot(theta * 180 / np.pi, data[:, 4], '.')
        plt.xlabel(r'$\theta$')
        plt.title(r'$C_p$')

        plt.figure()
        plt.plot(theta * 180 / np.pi, data[:, 5], '.')
        plt.xlabel(r'$\theta$')
        plt.title(r'$C_d$')

        plt.figure()
        plt.plot(theta * 180 / np.pi, data[:, 7], '.')
        plt.xlabel(r'$\theta$')
        plt.title(r'$C_l$')
        plt.show()

    return Xc, Yc, Zc, Fx, Fy, Fz

def calculate_displacement(F, dt=1.0):
    print "Calculating structural displacement ..."
    Fnp1 = F
    try:
        Fn = np.loadtxt("last_step_loads.txt")[6]
    except:
        Fn = 0
    m = 10.
    c = 0.
    k = 1.
    Xn = np.loadtxt('displacement_solution.txt')
    # State matrix
    A = np.matrix([[0, 1],
                   [-k/m, -c/m]])
    I = np.eye(2)
    Fn = np.array([0, Fn]).reshape(-1, 1)
    Fnp1 = np.array([0, Fnp1]).reshape(-1, 1)
    RHS = (I + A * dt / 2.).dot(Xn.reshape(-1, 1)) + (Fnp1 + Fn) / m * dt / 2.
    Xnp1 = np.linalg.solve(I - A * dt / 2., RHS)
    Xn = Xnp1
    print Fn[1, 0], Fnp1[1, 0]
    with open("displacement_solution.txt", "w") as disp_sol:
        disp_sol.write("{:<10.4E} {:<10.4E}".format(Xnp1[0, 0], Xnp1[1, 0]))
    return Xnp1[0, 0]

def update_surface(file_name="cylinder_body1.dat", dX=0.0, dY=0.0, dZ=0.1):
    print "Reading surface information ..."
    surface = np.loadtxt("cylinder_massoud_body1.dat", skiprows=3)
    print "Updating surface ..."
    surface[:, 2] = surface[:, 2] + dZ
    tecplot_header = """title="surface points and l2g id for massoud"
    variables="x","y","z","id"
    zone t="mdo body 1", i=196, j=98, f=fepoint,  solutiontime= 0.1000000E+01, strandid=0"""
    np.savetxt(file_name, surface, fmt='%-16.5e %-16.5e %-16.5e %-10d', header=tecplot_header)
