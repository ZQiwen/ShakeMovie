# -*- coding: utf-8 -*-
"""
@author: Qiwen Zhu

Last modified: Mon Aug 8 2022
"""

import pyvista as pv # vtk IO
from glob import glob
import matplotlib.pyplot as plt

def vtk2vtu(filename):
    header='vtk2vtu:'
    mesh=pv.read(filename)
    filename1=filename.replace('.vtk','.vtu')
    print(header,'Save to',filename1)
    mesh.save(filename1)
    print(header,'Done')

def MakeShakeMovie(filefolder,format='mp4'):

    cmap = plt.cm.get_cmap("bwr", 21).reversed()

    header='MSM-'+format+':'

    files=glob(filefolder+'/*.vtu')
    nframes=len(files)
    frame_rate=max(nframes/10.0,1.0)

    if nframes < 1:
        print(header,'No vtu file found in',filefolder,', use vtu file instead')
        files=glob(filefolder+'/*.vtk')
        nframes=len(files)
    if nframes < 1:
        print(header,'Error: No data found in',filefolder)
        exit()

    mesh=pv.read(files[int(nframes/2)])
    fieldname=mesh.array_names[0]
    field_array=mesh.get_array(name=fieldname)
    points=mesh.points
    length1=max(points[:,0])-min(points[:,0])
    length2=max(points[:,1])-min(points[:,1])
    scaler=max(length1,length2)*0.01/max(abs(field_array))

    # Create a plotter object and set the scalars to the Z height
    plotter = pv.Plotter(notebook=False, off_screen=True)

    plotter.add_mesh(
        mesh,
        lighting=True,
        show_edges=False,
        scalar_bar_args={"title": fieldname},
        cmap=cmap
    )

    scalar_range=[-5e-11, 5e-11]
    plotter.update_scalar_bar_range(scalar_range)
    plotter.camera.position=(11798222,3793317,709988)

    if format == 'gif': # Open a gif
        plotter.open_gif(filefolder+"/../wave.gif")
    elif format == 'mp4': # Open a mp4
        # windows-media-player can not play the video with quality 10
        plotter.open_movie(filefolder+"/../wave.mp4",framerate=12,quality=6)
    else:
        print('Error: Unsupported format. ShakeMovie Only support gif and mp4.')

    for iframe in range(nframes):

        mesh=pv.read(files[iframe])

        field_array=mesh.get_array(name=fieldname)

        print(header,fieldname,'in range:',field_array.max(),field_array.min())

        mesh.points[:,2] = mesh.points[:,2] + field_array*scaler

        plotter.update_coordinates(mesh.points, render=False)
        plotter.update_scalars(field_array, render=False)
        plotter.add_text(f"Frame: {iframe}", name='time-label')

        print(header,'Write frame',iframe,'/',nframes)
        plotter.write_frame()

    print(header,'Done')
    # Be sure to close the plotter when finished
    plotter.close()

def tryCameraPosition(filename,position):

    print(filename)
    cmap = plt.cm.get_cmap("bwr", 21).reversed()

    mesh=pv.read(filename)
    # Create a plotter object and set the scalars to the Z height
    p = pv.Plotter(notebook=False, off_screen=True)

    p.add_mesh(
        mesh,
        lighting=True,
        show_edges=False,
        scalar_bar_args={"title": "Displacement_Z"},
        cmap=cmap
    )

    scalar_range=[-5e-11, 5e-11]
    p.update_scalar_bar_range(scalar_range)

    p.camera.position=position

    p.show(screenshot=filename.replace('.vtu','.png'))
    # p.show()

# files=glob(r'./data/*.vtk')
# for fnm in files:
#     print(fnm)
#     vtk2vtu(fnm)

MakeShakeMovie('./data/','gif')
MakeShakeMovie('./data/','mp4')

# current_step=2500
# fnm='./velocity_Z_it%06d.vtu' % current_step
#
# tryCameraPosition(fnm,(11798222,3793317,709988))
