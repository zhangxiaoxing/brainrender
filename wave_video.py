import os
import h5py
import numpy as np
from vedo.colors import colorMap as map_color
from brainrender import Scene
from brainrender.video import VideoMaker

from pathlib import Path

def make_frame(scene, frame_number, *args, **kwargs):
    for (idx,r) in enumerate(kwargs['regs']):
        c=map_color(kwargs['sens_v'][frame_number,idx], name='jet', vmin=0, vmax=0.2)
        scene.get_actors(br_class="brain region", name=r)[0].color(c)

fpath=os.path.join("..","code","jpsth","wave_movie.hdf5")
with h5py.File(fpath,'r') as f:
    regs=[r.decode('latin-1') for r in f['reg'][0,:]]
    sens_v=np.array(f['sens_v'])
    dur_v=np.array(f['dur_v'])

# Create a brainrender scene
scene = Scene(title="brain regions")
# Add brain regions
for r in regs:
    scene.add_brain_region(r,alpha=0.2,color="grey", silhouette=False)

custom_camera = {
     'pos': (21369, 18996, -55938),
     'viewup': (0, 1, 0),
     'clippingRange': (44058, 84431),
     'focalPoint': (-7830, -4296, -5694),
     'distance': 62606, 
     }

vm=VideoMaker(scene,".","3d_wave",make_frame_func=make_frame)
vm.make_video(duration=11,fps=30,render_kwargs={'camera':custom_camera,'zoom':1.5},regs=regs,sens_v=sens_v)

