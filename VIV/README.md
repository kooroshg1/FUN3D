## Transient Fluid-Structure Analysis with FUN3D
In this tutorial, I looked at the Vortex Induced Vibration (VIV) of a cylinder in cross flow. In fluid dynamics, vortex induced vibrations are motions induced on bodies interacting with an external fluid flow, produced by – or the motion producing – periodical irregularities on this flow. This tutorial is my first attempt on solving the coupled fluid-structure interaction problem by coupled FUN3D with an external FEA solver.

## Finite Element Solver
I am using a simple truss-based FEA solver to get structural displacement for this problem. The time integration is done using the [Crank-Nicholson](https://en.wikipedia.org/wiki/Crank%E2%80%93Nicolson_method) method. FEA solver uses the same time step as the CFD solver; therefore, it cannot handle structures with high natural frequencies at this time. Please note that this is just a prove of concept. This example is not intended to be run for wide variety of structural properties. The structural model is shown in the following Figure.

![VIV Physical Problem][viv_physical_problem]
[viv_physical_problem]: /figure/viv_physical_problem.jpg

## Fluid-Structure Interaction Coupling
Fluid–structure interaction (FSI) is the interaction of some movable or deformable structure with an internal or surrounding fluid flow. Fluid–structure interactions can be stable or oscillatory. Here, I am using the following steps to couple the CFD and FEA solvers:

1. Solve and advance the fluid's equation one time step. Now we have the fluid's solution (pressure and velocity) at times `n` and `n+1`.
2. Integrate pressure on the cylinder surface to calculate the aerodynamic load. For this problem, I am only transferring lift force to the structural solver.
3. Calculate the position of the structure at time step `n+1` based on position at time `n` and loads at `n` and `n+1`. I am using Crank-Nicholson for this step.
4. Update the location of the structure and advance fluid's solution one step.
