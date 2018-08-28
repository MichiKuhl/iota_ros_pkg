
IOTA ROS implemetation
=====
This is a package for the Robot Operating System framework.
It is supposed to make the implementation of Iota transactions into robotics much easier  .

Please Download and Install the PYOTA Library
https://github.com/iotaledger/iota.lib.py




**How to use:**

To make a transaction you only need to publish an **iota_st.msg** into the **/iota/iota_send Topic**.


Use the following command to start the IOTA Node:

`rosrun iota_ros_pkg iota_ros_main.py`

This package was only tested with ROS Kinetic.
