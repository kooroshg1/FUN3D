import FUN3D_FSI
import numpy as np
t = float(np.loadtxt("new_airloads_are_ready"))
Xc, Yc, Zc, Fx, Fy, Fz = FUN3D_FSI.calculate_load(plot_surface_loads=False)
dZ = FUN3D_FSI.calculate_displacement(F=Fz, dt=0.1)
with open("fsi_solution_history.txt", "a") as load_history:
    print "Writing solution history to file"
    load_history.write("{:<12.4E} {:<12.4E} {:<12.4E} {:<12.4E} {:<12.4E} {:<12.4E} {:<12.4E}\n".format(t, Xc, Yc, Zc, Fx, Fy, Fz))
with open("last_step_loads.txt", "w") as last_step:
    last_step.write("{:<12.4E} {:<12.4E} {:<12.4E} {:<12.4E} {:<12.4E} {:<12.4E} {:<12.4E}\n".format(t, Xc, Yc, Zc, Fx, Fy, Fz))
print "dt = ", t
FUN3D_FSI.update_surface(dZ=dZ)
