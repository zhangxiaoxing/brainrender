from vedo.colors import colorMap as map_color
from brainrender import Scene

from rich import print
from myterial import orange
from pathlib import Path

sens_list=[
        ['TT',0.224,0.206],
        ['EPd',0.193,0.214],
        ['AON',0.175,0.182],
        ['DP',0.144,0.172],
        ['PIR',0.094,0.137],
        ['ILA',0.094,0.167],
        ['ORB',0.086,0.159],
        ['SI',0.059,0.220],
        ['BST',0.058,0.074],
        ['AI',0.047,0.109],
        ['ACB',0.046,0.147],
        ['HIP',0.044,0.146],
        ['CEA',0.040,0.117],
        ['MED',0.039,0.142],
        ['ACA',0.034,0.127],
        ['FRP',0.034,0.108],
        ['LS',0.033,0.143],
        ['PL',0.033,0.142],
        ['RHP',0.029,0.171],
        ['EPI',0.025,0.134],
        ['VENT',0.025,0.079],
        ['CP',0.024,0.111],
        ['GENd',0.016,0.075],
        ['GPe',0.009,0.095],
        ['ILM',0.009,0.164],
        ['LAT',0.008,0.089],
        ['GPi',0.007,0.125],
        ['SS',0.007,0.069],
        ['MO',0.006,0.085],
        ['APN',0.000,0.090],
        ['RSP',0.000,0.080],
        ['RT',0.000,0.066],
        ['VIS',0.000,0.065],
        ['VISC',0.000,0.188]]
# Create a brainrender scene
scene = Scene(title="brain regions")
# Add brain regions
for entry in sens_list:
    scene.add_brain_region(entry[0],alpha=0.2,color="grey", silhouette=False)
    c=map_color(entry[2], name='jet', vmin=0, vmax=0.2)
    scene.get_actors(br_class="brain region", name=entry[0])[
        0
    ].color(c)

# Render!
custom_camera = {
     'pos': (21369, 18996, -55938),
     'viewup': (0, 1, 0),
     'clippingRange': (44058, 84431),
     'focalPoint': (-7830, -4296, -5694),
     'distance': 62606, 
     }

# Render!
scene.render(camera=custom_camera, zoom=1.5, interactive=True)
