This tutorial goes through the node ordering to have an acceptable plot3d mesh. Please look at the python script (generate mesh) undet `plot3d` folder for more details on this. I am running the lid-driven cavity problem for this example.

To generate the mesh and run fun3d type the following syntax in your terminal:
```
gobalk@apollo:~/FUN3D/Plot3D Block Meshing$ cd plot3d
gobalk@apollo:~/FUN3D/Plot3D Block Meshing/plot3d$ python generate-mesh.py
gobalk@apollo:~/FUN3D/Plot3D Block Meshing/plot3d$ plot3d_to_aflr3
0
block
2
gobalk@apollo:~/FUN3D/Plot3D Block Meshing/plot3d$ cp block.mapbc ../
gobalk@apollo:~/FUN3D/Plot3D Block Meshing/plot3d$ cp block.ugrid ../
gobalk@apollo:~/FUN3D/Plot3D Block Meshing/plot3d$ cd ..
gobalk@apollo:~/FUN3D/Plot3D Block Meshing$ nodet
```
