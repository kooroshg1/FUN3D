# Lid-driven cavity problem
# Introduction

The lid-driven cavity problem has long been used a test or validation case for new codes or new solution methods. The problem geometry is simple and two-dimensional, and the boundary conditions are also simple. The standard case is fluid contained in a square domain with Dirichlet boundary conditions on all sides, with three stationary sides and one moving side (with velocity tangent to the side).

<p align="center">
  <img src="https://github.com/kooroshg1/FUN3D/blob/master/lid-driven-cavity-figure.png", height="145.5">
</p>

Similar simulations have also been done at various aspect ratios, and it can also be done with the lid replaced with a moving fluid. This problem is a somewhat different situation, and is usually referred to as the shear-driven cavity. You may see the two names (lid-driven and shear-driven) used interchangeably in spite of the fact that they are distinct (and different) problems.

This problem has been solved as both a laminar flow and a turbulent flow, and many different numerical techniques have been used to compute these solutions. Since this case has been solved many times, there is a great deal of data to compare with. A good set of data for comparison is the data of [Ghia, Ghia, and Shin (1982)](https://pdfs.semanticscholar.org/211b/45b6a06336a72ca064a6e59b14ebc520211c.pdf), since it includes tabular results for various of Reynolds numbers. These simulation results are obtained using a non-primitive variable approach.

This problem is a nice one for testing for several reasons. First, as mentioned above, there is a great deal of literature to compare with. Second, the (laminar) solution is steady. Third, the boundary conditions are simple and compatible with most numerical approaches. Note that this is not necessarily the case for finite element methods, in which difficulties may arise at the corner intersections of the moving wall and the stationary wall.

# Results

Shown below are a few results from a simulation of the lid-driven cavity (for a Reynolds number of one hundred) using the FUN3D code.

# References
Ghia, Ghia, and Shin (1982), "High-Re solutions for incompressible flow using the Navier-Stokes equations and a multigrid method", Journal of Computational Physics, Vol. 48, pp. 387-411.

# Resources
https://www.cfd-online.com/Wiki/Lid-driven_cavity_problem
http://www.cavityflow.com/
http://web.mit.edu/calculix_v2.7/CalculiX/ccx_2.7/doc/ccx/node14.html
