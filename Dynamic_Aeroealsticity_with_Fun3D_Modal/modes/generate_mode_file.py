import numpy as np

with open('cylinder_massoud_body1.dat', 'r') as massoud_file:
    with open('cylinder_body1_mode1.dat', 'w') as modal_file:
        massoud_line = massoud_file.readline()
        modal_file.write(massoud_line)

        massoud_line = massoud_file.readline()
        modal_file.write(massoud_line)

        massoud_line = massoud_file.readline()
        modal_file.write(massoud_line)
        foo = massoud_line.split(', ')

        number_of_points = int(foo[1][2:])
        number_of_connectivity = int(foo[2][2:])
        for iLine in range(0, number_of_points):
            massoud_line = massoud_file.readline()
            modal_file.write(massoud_line[:-1])
            modal_file.write('\t{:<16.6E} {:<16.6E} {:<16.6E}\n'.format(0, 0, 1))
        for iLine in range(0, number_of_connectivity):
            massoud_line = massoud_file.readline()
            modal_file.write(massoud_line)

