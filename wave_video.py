import os
import h5py
import numpy as np
from vedo.colors import colorMap as map_color
from brainrender import Scene
from brainrender.video import VideoMaker

from pathlib import Path

def make_frame(scene, frame_number, *args, **kwargs):
    for (idx,r) in enumerate(kwargs['regs']):
        if kwargs['ctype']=='both':
            c=np.array([0.2+kwargs['sens_v'][frame_number,idx]*0.8,0.2,0.2+kwargs['dur_v'][frame_number,idx]*0.8])
        elif kwargs['ctype']=='sens':
            c=np.array([0.2+kwargs['sens_v'][frame_number,idx]*0.8,0.2,0.2])
        elif kwargs['ctype']=='dur':
            c=np.array([0.2,0.2,0.2+kwargs['dur_v'][frame_number,idx]*0.8])
            
        scene.get_actors(br_class="brain region", name=r)[0].color(c)

fpath=os.path.join("..","code","jpsth","wave_movie.hdf5")
with h5py.File(fpath,'r') as f:
    regs=[r.decode('latin-1') for r in f['reg'][0,:]]
    sens_v=np.array(f['sens_v'])
    dur_v=np.array(f['dur_v'])

movie_dur=sens_v.shape[0]/30

custom_camera = {
     'pos': (21369, 18996, -55938),
     'viewup': (0, 1, 0),
     'clippingRange': (44058, 84431),
     'focalPoint': (-7830, -4296, -5694),
     'distance': 62606, 
     }

for ctype in [['Both wave','both'],['Sensory wave','sens'],['Duration wave','dur']]:

    # Create a brainrender scene
    scene = Scene(title=ctype[0])

    # Add brain regions
    for r in regs:
        scene.add_brain_region(r,alpha=0.2,color="grey", silhouette=False)

    vm=VideoMaker(scene,".",f"3d_wave_{ctype[1]}",make_frame_func=make_frame,size='740x480')
    vm.make_video(duration=movie_dur,fps=30,render_kwargs={'camera':custom_camera,'zoom':3},regs=regs,sens_v=sens_v,dur_v=dur_v,ctype=ctype[1])
    


# ffmpeg -i "3d_wave_sens.mp4" -vf "pad=iw:2*ih [top]; movie=k\\:/code/jpsth/sens_dur_wave_sens.mp4 [bottom]; [top][bottom] overlay=0:main_h/2" "TopDown_Sens.mp4" 

# ffmpeg -i "3d_wave_dur.mp4" -vf "pad=iw:2*ih [top]; movie=k\\:/code/jpsth/sens_dur_wave_dur.mp4 [bottom]; [top][bottom] overlay=0:main_h/2" "TopDown_Dur.mp4" 

# ffmpeg -i "3d_wave_both.mp4" -vf "pad=iw:2*ih [top]; movie=k\\:/code/jpsth/sens_dur_wave_both.mp4 [bottom]; [top][bottom] overlay=0:main_h/2" "TopDown_Both.mp4"

# ffmpeg -f concat -i concat.txt -c:v libx264 -g 30 -profile:v main Wave_TopDown.mp4
