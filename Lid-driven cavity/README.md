# Lid-driven Cavity Problem
## Introduction
The lid-driven cavity problem has long been used a test or validation case for new codes or new solution methods. The problem geometry is simple and two-dimensional, and the boundary conditions are also simple. The standard case is fluid contained in a square domain with Dirichlet boundary conditions on all sides, with three stationary sides and one moving side (with velocity tangent to the side).

<p align="center">
  <img src="https://github.com/kooroshg1/FUN3D/blob/master/Lid-driven%20cavity/images/lid-driven-cavity-figure.png", height="300.0">
</p>

Similar simulations have also been done at various aspect ratios, and it can also be done with the lid replaced with a moving fluid. This problem is a somewhat different situation, and is usually referred to as the shear-driven cavity. You may see the two names (lid-driven and shear-driven) used interchangeably in spite of the fact that they are distinct (and different) problems.

This problem has been solved as both a laminar flow and a turbulent flow, and many different numerical techniques have been used to compute these solutions. Since this case has been solved many times, there is a great deal of data to compare with. A good set of data for comparison is the data of [Ghia, Ghia, and Shin (1982)](https://pdfs.semanticscholar.org/211b/45b6a06336a72ca064a6e59b14ebc520211c.pdf), since it includes tabular results for various of Reynolds numbers. These simulation results are obtained using a non-primitive variable approach.

This problem is a nice one for testing for several reasons. First, as mentioned above, there is a great deal of literature to compare with. Second, the (laminar) solution is steady. Third, the boundary conditions are simple and compatible with most numerical approaches. Note that this is not necessarily the case for finite element methods, in which difficulties may arise at the corner intersections of the moving wall and the stationary wall.

## Files Description
Here I explain the different files I have in this folder.

#### `MESH-generate-lidDrivenCavity.py`
I use this file to generate the Plot3D mesh and the neutral map file associated with my mesh for the lid-driven cavity problem. This Plot3D mesh is later converted to AFLR3 mesh (ugrid) using FUN3D convertors. The [neutral map file](https://geolab.larc.nasa.gov/Volume/Doc/nmf.htm) provides a formatted summary of information relating to

* the size and composition of the mesh,
* the topological features of the mesh and
* assigned flow field boundary conditions

which is typically required of any multi-block flow solver. The formatting of this file is "neutral" in that it is not specific to any particular flow solver, thus a reformatting of the data will be required before use.

You can edit the length of the domain and number of mesh cells by editing the first few lines in the `MESH-generate-lidDrivenCavity.py`file. You need to have `numpy` package installed to run this script.

#### `FUN3D-PLOT-solution_hist.py`
I am using this file to plot the convergence history. You need to have `numpy` and `matplotlib` packages installed to run this script.

#### `fun3d.nml`:
This is the main input namelist file and is described in detail in [FUN3D manual](https://fun3d.larc.nasa.gov/papers/FUN3D_Manual-12.9.pdf). This file includes the type of equations I am solving, solution details, output file type, and etc. I am using the `volume_output_variables` namelist to request for the volume variable output in the `VTK` format. Please note that since `VTK` already has `x`, `y`, and `z`, these variables are set as false.
```
&volume_output_variables
   export_to = 'vtk'
   x = .false.
   y = .false.
   z = .false.
/
```

#### `remove-all`
This is bash script to clean the working directory from the files you generated. You may need to first overwrite its access permissions by running the following syntax in your terminal

```
sudo chmod u+x PATH_TO_REMOVE_ALL/remove-all
```

## Case Setup
Cases are setup in FUN3D by editing case files. Users should select an editor of choice with which to do this, such as emacs, vi, gedit, nedit, etc. Editing files is possible in FUN3D because the I/O uses a dictionary format with keywords that convey sufficient meaning to be understood by the users.

You start by running the meshing script. To do this, first open a terminal in `/FUN3D/Lid-driven\ cavity` direction and type the following in your terminal

```
python MESH-generate-lidDrivenCavity.py
```

Now you should have `lidDrivenCavity.p3d`, and `lidDrivenCavity.nmf` generated in your folder. You can view the Plot3D mesh using [gmsh](http://gmsh.info/). The `lidDrivenCavity.nmf` file defines the boundary conditions on different faces of our single block mesh. You can look up the numbering convention used by the `*.nmf` file on their [website](https://geolab.larc.nasa.gov/Volume/Doc/nmf.htm).

In the `lidDrivenCavity.nmf` file, all the walls are defined as `viscous_solid` and hence they have the `no_slip` condition. To give the top wall a tangential velocity, I add the following line to my `fun3d.nml` file. This means that I am setting the velocity on `1` direction of wall `6` equal to one.

```
&boundary_conditions
    wall_velocity(6,1) = 1.0
/
```

Now we convert the `lidDrivenCavity.p3d` to the AFLR3 mesh that is used by FUN3D. This is done using `plot3d_to_aflr3` that ships with FUN3D. Please type that into your terminal and follow the instructions. The format for my Plot3D file is *ASCII*, my FUN3D project name is *lidDrivenCavity* and the output format is *ASCII* as well. After runing this script you should have `lidDrivenCavity.mapbc` and `lidDrivenCavity.ugrid` generated in your folder.

Now you can run FUN3D by typing the following syntax in your terminal

```
nodet
```

## Results
You can look at the results by typing `paraview lidDrivenCavity_volume_timestep1000.vtk` in the terminal. Shown below are the velocity contours from a simulation of the lid-driven cavity for a Reynolds number of one hundred using the FUN3D code.

<div style="align: center; text-align:center;">
    <img src="https://github.com/kooroshg1/FUN3D/blob/master/Lid-driven%20cavity/images/u-velocity.png" height="300.0" align="middle"/>
    <div text-align:center>U-velocity contour</div>
</div>

<div style="align: center; text-align:center;">
    <img src="https://github.com/kooroshg1/FUN3D/blob/master/Lid-driven%20cavity/images/v-velocity.png" height="300.0" align="middle"/>
    <div text-align:center>V-velocity contour</div>
</div>

## Cleaning Directory
You can clean this directory by typing `./remove-all` in your terminal.

## References
1. Ghia, Ghia, and Shin (1982), "High-Re solutions for incompressible flow using the Navier-Stokes equations and a multigrid method", Journal of Computational Physics, Vol. 48, pp. 387-411.

## Resources
1. https://www.cfd-online.com/Wiki/Lid-driven_cavity_problem
2. http://www.cavityflow.com/
3. http://web.mit.edu/calculix_v2.7/CalculiX/ccx_2.7/doc/ccx/node14.html
