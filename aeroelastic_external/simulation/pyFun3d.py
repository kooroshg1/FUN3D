import os.path
import time
import numpy as np
import matplotlib.pyplot as plt

def check_aero_loads():
    aero_loads_ready = False
    while not os.path.exists('new_airloads_are_ready'):
        time.sleep(0.1)

    current_time = np.loadtxt('new_airloads_are_ready')
    aero_loads_ready = True
    return aero_loads_ready, current_time

def read_ddfdrive(rho_infty = 1.0, V_infty = 1.0, p_infty = 1.0, ddfdrive_path = 'cylinder_ddfdrive_body1.dat'):
    with open(ddfdrive_path, 'r') as ddfdrive:
        line = ddfdrive.readline()
        line = ddfdrive.readline()
        line = ddfdrive.readline()
        foo = line.split(', ')
        i = int(foo[1][2:])
        j = int(foo[2][2:])

    NODE = np.zeros([i, 10])
    ELEMENT = np.zeros([j, 4], dtype=int)

    with open(ddfdrive_path, 'r') as ddfdrive:
        iLine = 0
        for line in ddfdrive:
            iLine = iLine + 1
            if ((iLine - 3) <= i) & (iLine > 3):
                foo = line.split()
                NODE[iLine - 4, 0] = float(foo[0])
                NODE[iLine - 4, 1] = float(foo[1])
                NODE[iLine - 4, 2] = float(foo[2])
                NODE[iLine - 4, 3] = float(foo[3])
                NODE[iLine - 4, 4] = float(foo[4])
                NODE[iLine - 4, 5] = float(foo[5])
                NODE[iLine - 4, 6] = float(foo[6])
                NODE[iLine - 4, 7] = float(foo[7])
                NODE[iLine - 4, 8] = float(foo[8])
                NODE[iLine - 4, 9] = float(foo[9])
            elif ((iLine - i - 3) >= 1) & ((iLine - i - 3) <= j):
                foo = line.split()
                ELEMENT[iLine - i - 3 - 1, 0] = int(foo[0]) - 1
                ELEMENT[iLine - i - 3 - 1, 1] = int(foo[1]) - 1
                ELEMENT[iLine - i - 3 - 1, 2] = int(foo[2]) - 1
                ELEMENT[iLine - i - 3 - 1, 3] = int(foo[3]) - 1

    cp = np.zeros(len(ELEMENT))
    p = np.zeros(len(ELEMENT))
    fx = np.zeros(len(ELEMENT))
    fy = np.zeros(len(ELEMENT))
    fz = np.zeros(len(ELEMENT))
    x = np.zeros(len(ELEMENT))
    y = np.zeros(len(ELEMENT))
    z = np.zeros(len(ELEMENT))
    cfx = np.zeros(len(ELEMENT))
    cfy = np.zeros(len(ELEMENT))
    cfz = np.zeros(len(ELEMENT))
    normal = np.zeros([len(ELEMENT), 3])
    dA = np.zeros(len(ELEMENT))
    ip = 0

    # Calculate cell center quantities
    for element in ELEMENT:
        x[ip] = (NODE[element[0], 0] +
                 NODE[element[1], 0] +
                 NODE[element[2], 0] +
                 NODE[element[3], 0]) / 4.0

        y[ip] = (NODE[element[0], 1] +
                 NODE[element[1], 1] +
                 NODE[element[2], 1] +
                 NODE[element[3], 1]) / 4.0

        z[ip] = (NODE[element[0], 2] +
                 NODE[element[1], 2] +
                 NODE[element[2], 2] +
                 NODE[element[3], 2]) / 4.0

        cp[ip] = (NODE[element[0], 4] +
                  NODE[element[1], 4] +
                  NODE[element[2], 4] +
                  NODE[element[3], 4]) / 4.0

        p[ip] = cp[ip] * 0.5 * rho_infty * V_infty ** 2.0 + p_infty

        cfx[ip] = (NODE[element[0], 5] +
                   NODE[element[1], 5] +
                   NODE[element[2], 5] +
                   NODE[element[3], 5]) / 4.0

        cfy[ip] = (NODE[element[0], 6] +
                   NODE[element[1], 6] +
                   NODE[element[2], 6] +
                   NODE[element[3], 6]) / 4.0

        cfz[ip] = (NODE[element[0], 7] +
                   NODE[element[1], 7] +
                   NODE[element[2], 7] +
                   NODE[element[3], 7]) / 4.0
        # Surface normal
        x1 = NODE[element[0], 0]
        y1 = NODE[element[0], 1]
        z1 = NODE[element[0], 2]

        x2 = NODE[element[1], 0]
        y2 = NODE[element[1], 1]
        z2 = NODE[element[1], 2]

        x3 = NODE[element[2], 0]
        y3 = NODE[element[2], 1]
        z3 = NODE[element[2], 2]

        x4 = NODE[element[3], 0]
        y4 = NODE[element[3], 1]
        z4 = NODE[element[3], 2]
        normal[ip, 0] = (y2 - y1) * (z3 - z2) - (z2 - z1) * (y3 - y2)
        normal[ip, 1] = -((x2 - x1) * (z3 - z2) - (z2 - z1) * (x3 - x2))
        normal[ip, 2] = (x2 - x1) * (y3 - y2) - (y2 - y1) * (x3 - x2)
        dA[ip] = np.linalg.norm(normal[ip, :])
        normal[ip, :] = normal[ip, :] / np.linalg.norm(normal[ip, :])
        if ip > 1:
            if normal[ip, :].dot(normal[ip - 1, :]) < 0:
                normal[ip, :] = -normal[ip, :]

        fx[ip] = -p[ip] * dA[ip] * normal[ip, 0]
        fy[ip] = -p[ip] * dA[ip] * normal[ip, 1]
        fz[ip] = -p[ip] * dA[ip] * normal[ip, 2]

        ip = ip + 1

    return {'x': x, 'y': y, 'z': z, \
            'cp': cp, 'cfz': cfz, 'cfz': cfz, 'cfz': cfz, \
            'p': p, 'fx': fx, 'fy': fy, 'fz': fz, \
            'dA': dA, 'normal': normal}

def update_surface(massoud_file_path = 'cylinder_massoud_body1.dat', updated_file_path = 'cylinder_body1.dat', dispx = 0.0, dispy = 0.0, dispz = 1.0):
    with open(massoud_file_path, 'r') as massoud_file:
        file_header = massoud_file.readline()
        file_header = file_header + massoud_file.readline()
        file_header = file_header + massoud_file.readline()

    with open(massoud_file_path, 'r') as massoud_file:
        with open(updated_file_path, 'w') as updated_file:
            updated_file.write(file_header)

            fileContent = massoud_file.readline()
            fileContent = massoud_file.readline()
            fileContent = massoud_file.readline()
            fileContent = fileContent.split(", ")
            number_of_data_points = int(fileContent[1][2:])
            number_of_connectivity_points = int(fileContent[2][2:])

            for iLine in range(0, number_of_data_points):
                fileContent = massoud_file.readline()
                fileContent = fileContent.split()
                updated_file.write("{:>25.16E} {:>25.16E} {:>25.16E} {:>25d}\n".format(float(fileContent[0]) + dispx,
                                                                                       float(fileContent[1]) + dispy,
                                                                                       float(fileContent[2]) + dispz,
                                                                                       int(fileContent[3])))

            for iLine in range(0, number_of_connectivity_points):
                fileContent = massoud_file.readline()
                fileContent = fileContent.split();
                updated_file.write("{:>25d} {:>25d} {:>25d} {:>25d}\n".format(int(fileContent[0]), int(fileContent[1]),
                                                                              int(fileContent[2]), int(fileContent[3])))