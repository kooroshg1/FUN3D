# Flow Over a Circular Cylinder
## Introduction
External flows past objects have been studied extensively because of their many practical applications.  For example, airfoils are made into streamline shapes in order to increase the lifts, and at the same time, reducing the aerodynamic drags exerted on the wings.  On the other hand, flow past a blunt body, such as a circular cylinder, usually experiences boundary layer separation and very strong flow oscillations in the wake region behind the body.  In certain Reynolds number range, a periodic flow motion will develop in the wake as a result of boundary layer vortice being shed alternatively from either side of the cylinder.  This regular pattern of vortices in the wake is called a [Karman vortex street](https://en.wikipedia.org/wiki/K%C3%A1rm%C3%A1n_vortex_street). It creates an oscillating flow at a discrete frequency that is correlated to the Reynolds number of the flow. The periodic nature of the vortex shedding phenomenon can sometimes lead to unwanted structural vibrations, especially when the shedding frequency matches one of the resonant frequencies of the structure. One example is the famous [Tacoma Narrow bridge](https://en.wikipedia.org/wiki/Tacoma_Narrows_Bridge_(1940) incident.

<div style="align: center; text-align:center;">
    <img src="https://github.com/kooroshg1/FUN3D/blob/master/Lid-driven%20cavity/images/u-velocity.png" height="300.0" align="middle"/>
    <div text-align:center>U-velocity contour</div>
</div>

Here, I am going to investigate the flow past a circular cylinder and study the laminar wake flow field using the FUN3D flow solver. The freqeuncy of the shedding will be verified by calculating the [Strouhal number](https://en.wikipedia.org/wiki/Strouhal_number) and comparing it to the literature. The Strouhal number (St) is a dimensionless number describing oscillating flow mechanisms

<div style="align: center; text-align:center;">
    <img src="https://github.com/kooroshg1/FUN3D/blob/master/Lid-driven%20cavity/images/v-velocity.png" height="300.0" align="middle"/>
    <div text-align:center>U-velocity contour</div>
</div>

## Files Description
Here I explain the different files I have in this folder.

#### `FUN3D-MESH-cylinder.py`
This file was written by Dr. Richard Snyder at AFRL. I use this file to generate the Plot3D mesh and the neutral map file associated with my mesh for the flow around cylinder problem. This Plot3D mesh is later converted to AFLR3 mesh (ugrid) using FUN3D convertors. The [neutral map file](https://geolab.larc.nasa.gov/Volume/Doc/nmf.htm) provides a formatted summary of information relating to

* the size and composition of the mesh,
* the topological features of the mesh and
* assigned flow field boundary conditions

which is typically required of any multi-block flow solver. The formatting of this file is "neutral" in that it is not specific to any particular flow solver, thus a reformatting of the data will be required before use.

You can generate a mesh by using the following syntax

```
python FUN3D-MESH-cylinder.py --i 99 --j 76 --spacing 0.01 cylinder
```

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

#### `FUN3D-POSTPROCESS-shedding_frequency.py`
I am using the file to read the force time history and calculate the shedding freqeuncy using Power Spectral Density (PSD) functions. When you run this script, it will plot the PSD function and report the Strouhal number on the terminal. You need to have `numpy` and `matplotlib` packages installed to run this script. You can run this script by typing the following syntax in your terminal

```
python FUN3D-POSTPROCESS-shedding_frequency.py
```

#### `remove-all`
This is bash script to clean the working directory from the files you generated. You may need to first overwrite its access permissions by running the following syntax in your terminal

```
sudo chmod u+x PATH_TO_REMOVE_ALL/remove-all
```

## Case Setup
Cases are setup in FUN3D by editing case files. Users should select an editor of choice with which to do this, such as emacs, vi, gedit, nedit, etc. Editing files is possible in FUN3D because the I/O uses a dictionary format with keywords that convey sufficient meaning to be understood by the users.

You start by running the meshing script. To do this, first open a terminal in `/FUN3D/Flow around a circular cylinder - 2D` direction and type the following in your terminal

```
python FUN3D-MESH-cylinder.py --i 99 --j 76 --spacing 0.01 cylinder
```

Now you should have `cylinder.p3d`, and `cylinder.nmf` generated in your folder. You can view the Plot3D mesh using [gmsh](http://gmsh.info/). The `cylinder.nmf` file defines the boundary conditions on different faces of our single block mesh. You can look up the numbering convention used by the `*.nmf` file on their [website](https://geolab.larc.nasa.gov/Volume/Doc/nmf.htm).

Now we convert the `cylinder.p3d` to the AFLR3 mesh that is used by FUN3D. This is done using `plot3d_to_aflr3` that ships with FUN3D. Please type that into your terminal and follow the instructions. The format for my Plot3D file is *ASCII*, my FUN3D project name is *cylinder* and the output format is *ASCII* as well. After runing this script you should have `cylinder.mapbc` and `cylinder.ugrid` generated in your folder.

Now you can run FUN3D by typing the following syntax in your terminal

```
nodet
```

## Results
You can look at the results by typing `paraview cylinder_volume_timestep1000.vtk` in the terminal. Shown below are the velocity contours from a simulation of the lid-driven cavity for a Reynolds number of one hundred using the FUN3D code.

<div style="align: center; text-align:center;">
    <img src="https://github.com/kooroshg1/FUN3D/blob/master/Lid-driven%20cavity/images/u-velocity.png" height="300.0" align="middle"/>
    <div text-align:center>U-velocity contour</div>
</div>

<div style="align: center; text-align:center;">
    <img src="https://github.com/kooroshg1/FUN3D/blob/master/Lid-driven%20cavity/images/v-velocity.png" height="300.0" align="middle"/>
    <div text-align:center>U-velocity contour</div>
</div>

Lift force time history and the PSD plot are generated by running the `FUN3D-POSTPROCESS-shedding_frequency.py` script. These are shown in the following plots. The Strouhal number is calculated as 0.16 for this case.

<div style="align: center; text-align:center;">
    <img src="https://github.com/kooroshg1/FUN3D/blob/master/Lid-driven%20cavity/images/u-velocity.png" height="300.0" align="middle"/>
    <div text-align:center>U-velocity contour</div>
</div>

<div style="align: center; text-align:center;">
    <img src="https://github.com/kooroshg1/FUN3D/blob/master/Lid-driven%20cavity/images/v-velocity.png" height="300.0" align="middle"/>
    <div text-align:center>U-velocity contour</div>
</div>

## Cleaning Directory
You can clean this directory by typing `./remove-all` in your terminal.

## References
1. Ghia, Ghia, and Shin (1982), "High-Re solutions for incompressible flow using the Navier-Stokes equations and a multigrid method", Journal of Computational Physics, Vol. 48, pp. 387-411.

## Resources
1. https://www.eng.fsu.edu/~shih/succeed/cylinder/cylinder.htm
2. https://confluence.cornell.edu/display/SIMULATION/FLUENT+-+Steady+Flow+Past+a+Cylinder
