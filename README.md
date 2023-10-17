# 3d_render
simple 3D render codes. 

I am following the youtube video from Coder Space at https://www.youtube.com/watch?v=M_Hx0g5vFko
It has a corresponding github with the link given below. 

I finally figured out the camera transformation matrix issue in the original github. The main concept is: if we know the camera transformation matrix — the matrix responsible for rotating and moving the camera in the world, we can take its inverse to get the change of basis matrix which can help us to find the coordinates of points wrt the camera. 



# Acknowledge
- I am mostly following the tutorial at this github https://github.com/StanislavPetrovV/Software_3D_engine
- I also plan to use wavefront loader/saver from James Gregson later https://www.jamesgregson.ca/
- [The blog explaining the camera extrinsic matrix](https://towardsdatascience.com/camera-extrinsic-matrix-with-example-in-python-cfe80acab8dd)