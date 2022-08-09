# ShakeMovie
Create shake movies of seismic waves. 
Written originally for visualizing wavefields computed by the SPECFEM3D_Cartesion package (<https://github.com/geodynamics/specfem3d>). 

## Requirements:
Wavefield data in vtk or vtu format (<https://vtk.org>). 

Python environment (tested on 3.7.10) with modules pyvista (<https://docs.pyvista.org>, tested on version 0.36.1), imageio-ffmpeg (<https://github.com/imageio/imageio-ffmpeg>, tested on version 0.4.7) and matplotlib (<https://matplotlib.org>).

If you use anaconda as the Python environment manager, you can create a environment satisfying the above requirements from the pyvista.yml:

```
conda env create -f pyvista.yml
```

## Usage:
Edit Line "MakeShakeMovie('./data/','gif')" and Run the script make_shake_movie.py.

where './data/' is the path to the folder containing your vtk/vtu files

and 'gif' is the format of the output shake movie. Choose between 'mp4' and 'gif'.

Uncommomet Line 'plotter.camera.position=(11798222,3793317,709988)' to set the camera to the default position. 
