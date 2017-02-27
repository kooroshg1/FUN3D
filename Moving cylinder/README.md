In this tutorial, I looked at motion of cylinder in domain due to some predefined path. To achieve this, I used two different methods defined by the `motion_driver` card in the `moving_body.input` file:

1. `forced_motion` is used to define a motion on a straight line or rotation of the boundary. A perdiodic motion can be also defined using this card. You can find examples on this in the [Forced](https://github.com/kooroshg1/FUN3D/tree/master/Moving%20cylinder/Forced) folder.

2. `motion_from_file` is used to define a motion based on a path defined in a file. The motion is defined at each time step based on a transformation defined in `*.hst` file. You can find examples on this in the [Motion_file](https://github.com/kooroshg1/FUN3D/tree/master/Moving%20cylinder/Motion_file) folder. For more information please refer to the FUN3D's user manual.
